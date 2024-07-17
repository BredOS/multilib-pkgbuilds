#! /usr/bin/python
from subprocess import check_output
from time import sleep
import urllib.request
from tarfile import open as topen
from os import mkdir, listdir
from shutil import rmtree

import conf


def pkname(fp):
    """
    Find the pkgname off of a desc file.
    """
    res = None
    try:
        with open(fp) as f:
            lines = f.readlines()
            inc = 0
            while lines[inc] != "%NAME%\n":
                inc += 1
            res = lines[inc + 1][:-1]
    except:
        pass
    return res


def pkver(fp):
    """
    Find the pkgversion off of a desc file.
    """
    res = None
    try:
        with open(fp) as f:
            lines = f.readlines()
            inc = 0
            while lines[inc] != "%VERSION%\n":
                inc += 1
            res = lines[inc + 1][:-1]
    except:
        pass
    return res


def download() -> None:
    # Download all package lists
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
    # Remove all local lists
    for i in listdir():
        if i.endswith("-repo"):
            if conf.debug:
                print(f"Removing ./{i}/")
            rmtree(i)


def lists() -> list:
    """
    Use this function to generate a list of updatable packages.
    A log is also always generated at ./lists.log
    """
    res = list()
    with open("lists.log", "w") as logf:
        try:
            clean()
            listlen = download()
            drs = []
            for i in range(len(conf.repos)):
                drs.append(listdir(str(i) + "-repo"))
            for i in drs[0]:
                pkgname = pkname(f"./0-repo/{i}/desc")
                repover = pkver(f"./0-repo/{i}/desc")
                found_anywhr = False
                if pkgname is None or repover is None:
                    raise RuntimeError("Package unparsable!!")
                if pkgname not in conf.ignore:
                    for j in range(1, len(drs)):
                        aurver = None # May remain None
                        for k in drs[j]:
                            if k[:2] == i[:2]: # Speedup
                                aurname = pkname(f"./1-repo/{k}/desc")
                                if aurname == pkgname or (
                                    pkgname in conf.alias
                                    and (
                                        (
                                            isinstance(conf.alias[pkgname], list)
                                            and aurname in conf.alias[pkgname]
                                        )
                                        or (
                                            isinstance(conf.alias[pkgname], str)
                                            and aurname == conf.alias[pkgname]
                                        )
                                    )
                                ):
                                    aurver = pkver(f"./1-repo/{k}/desc")
                                    found_anywhr = True
                                    break

                        if aurver is not None:
                            compare = (
                                check_output(["/usr/bin/vercmp", aurver, repover])
                                .decode()
                                .strip(" ")
                            )
                            if int(compare) < 0:
                                if conf.debug:
                                    print(
                                        f'\033[31mPackage \033[0m"{pkgname}" \033[31mis outdated in comparisson with repo #{j}!\033[0m "{repover}" > "{aurver}"'
                                    )
                                    logf.write(
                                        f'Package "{pkgname}" is outdated! "{repover}" > "{aurver}"\n'
                                    )
                                    res.append(pkgname)
                            elif int(compare) > 0:
                                if conf.debug:
                                    print(
                                        f'\033[36mPackage \033[0m"{pkgname}" \033[36mis ahead of repo #{j}! \033[0m"{repover}" < "{aurver}"'
                                    )
                                    logf.write(
                                        f'Package "{pkgname}" is ahead of repo! "{repover}" < "{aurver}"\n'
                                    )
                            elif int(compare) == 0:
                                if conf.debug:
                                    print(
                                        f'\033[32mPackage \033[0m"{pkgname}" \033[32mis up-to-date with repo #{j}.\033[0m'
                                    )
                                    logf.write(
                                        f'Package "{pkgname}" is up-to-date!\n'
                                    )
                    if (not found_anywhr) and conf.debug:
                        print(
                            f'\033[93mPackage \033[0m"{pkgname}" \033[93mCould not be matched.\033[0m'
                        )
                        logf.write(
                            f'Package "{pkgname}" Could not be matched.\n'
                        )
                elif conf.debug:
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


if __name__ == "__main__":
    print(lists())
