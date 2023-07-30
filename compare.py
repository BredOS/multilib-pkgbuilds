from subprocess import check_output
from time import sleep
import urllib.request
from tarfile import open as topen
from os import mkdir, listdir
from shutil import rmtree

import conf


def pkname(fp):
    res = None
    with open(fp) as f:
        lines = f.readlines()
        inc = 0
        while lines[inc] != "%NAME%\n":
            inc += 1
        res = lines[inc + 1][:-1]
    return res


def pkver(fp):
    res = None
    with open(fp) as f:
        lines = f.readlines()
        inc = 0
        while lines[inc] != "%VERSION%\n":
            inc += 1
        res = lines[inc + 1][:-1]
    return res


def download() -> None:
    foldern = 0
    for i in conf.repos:
        mkdir(str(foldern) + "-repo")
        if conf.debug:
            print(f"Downloading {i} into ./{foldern}-repo/")
        stream = urllib.request.urlopen(i)
        with topen(fileobj=stream, mode="r|gz") as f:
            f.extractall(path=f"./{foldern}-repo/")
        if conf.debug:
            print(f"Downloaded package list into ./{foldern}-repo/")
        foldern += 1


def clean() -> None:
    for i in listdir():
        if i.endswith("-repo"):
            if conf.debug:
                print(f"Removing ./{i}/")
            rmtree(i)


def lists() -> list:
    res = list()
    with open("lists.log", "w") as logf:
        try:
            clean()
            download()
            dr0 = listdir("0-repo")
            dr1 = listdir("1-repo")
            # sleep(1)
            for i in dr0:
                if i not in dr1:
                    pkgname = pkname(f"./0-repo/{i}/desc")
                    repover = pkver(f"./0-repo/{i}/desc")
                    aurver = None  # Can remain None
                    if pkgname not in conf.ignore:
                        for j in dr1:
                            if j[:2] == i[:2]:
                                aurname = pkname(f"./1-repo/{j}/desc")
                                if aurname == pkgname or (
                                    pkgname in conf.alias
                                    and aurname in conf.alias[pkgname]
                                ):
                                    aurver = pkver(f"./1-repo/{j}/desc")
                                    break
                        if aurver is not None:
                            compare = (
                                check_output(["/usr/bin/vercmp", aurver, repover])
                                .decode()
                                .strip(" ")
                            )
                            if int(compare) < int(0):
                                if conf.debug:
                                    print(
                                        f'\033[31mPackage \033[0m"{pkgname}" \033[31mis outdated!\033[0m "{repover}" > "{aurver}"'
                                    )
                                    logf.write(
                                        f'Package "{pkgname}" is outdated! "{repover}" > "{aurver}"\n'
                                    )
                                    res.append(pkgname)
                            elif int(compare) > int(0):
                                if conf.debug:
                                    print(
                                        f'\033[36mPackage \033[0m"{pkgname}" \033[36mis ahead of repo! \033[0m"{repover}" < "{aurver}"'
                                    )
                                    logf.write(
                                        f'Package "{pkgname}" is ahead of repo! "{repover}" < "{aurver}"\n'
                                    )
                        else:
                            if conf.debug:
                                print(
                                    f'\033[93mPackage \033[0m"{pkgname}" \033[93mCould not be matched.\033[0m'
                                )
                                logf.write(
                                    f'Package "{pkgname}" Could not be matched.\n'
                                )
                    else:
                        if conf.debug:
                            print(f'Package "{pkgname}" ignored.')
                            logf.write(f'Package "{pkgname}" ignored.\n')

        except Exception as err:
            print("Failed to complete! Error:")
            logf.write("Failed to complete! Error:\n")
            from traceback import print_exception

            print_exception(err)
        except KeyboardInterrupt:
            print("\nAbort.")
    clean()
    if conf.debug:
        print(f"Updates result table: {res}")
    return res
