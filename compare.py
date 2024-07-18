import concurrent.futures
from subprocess import check_output
from time import sleep
import urllib.request
from tarfile import open as topen
from os import mkdir, listdir
from shutil import rmtree
import pyalpm

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
    except Exception:
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
    except Exception:
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


def preprocess_repo(repo_index):
    repo_data = {}
    for pkg_dir in listdir(f"{repo_index}-repo"):
        desc_path = f"./{repo_index}-repo/{pkg_dir}/desc"
        pkgname = pkname(desc_path)
        pkgver = pkver(desc_path)
        if pkgname and pkgver:
            repo_data[pkgname] = pkgver
    return repo_data


def lists() -> list:
    """
    Use this function to generate a list of updatable packages.
    A log is also always generated at ./lists.log
    """
    res = list()
    with open("lists.log", "w") as logf:
        try:
            clean()
            download()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(preprocess_repo, i) for i in range(len(conf.repos))]
                repo_data_list = [future.result() for future in concurrent.futures.as_completed(futures)]
                
            main_repo_data = repo_data_list[0]
            other_repos_data = repo_data_list[1:]

            for pkgname, repover in main_repo_data.items():
                found_anywhr = False
                if pkgname not in conf.ignore:
                    for j, other_repo_data in enumerate(other_repos_data, start=1):
                        aurver = None
                        if pkgname in conf.alias:
                            if conf.debug:
                                print(f'Package "{pkgname}" is aliased.')
                                logf.write(f'Package "{pkgname}" is aliased.\n')
                            unalias = pkgname
                            pkgname = conf.alias[pkgname]
                        else:
                            unalias = pkgname

                        aurver = other_repo_data.get(pkgname, None)
                        found_anywhr = found_anywhr or aurver is not None
                        pkgname = unalias 

                        if aurver is not None:
                            compare = pyalpm.vercmp(aurver, repover)
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
