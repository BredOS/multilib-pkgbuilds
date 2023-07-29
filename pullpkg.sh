#! /usr/bin/bash
set -x
# Pulls PKGBUILD from the Arch Repo and places it in the current directory
# Use -a (aur) to pull from the Arch User Repository
# Usage example: pullpkg.sh 

# Usage function
usage() {
    echo "Usage: $0 [-a] <package>"
}

# Check for aur flag
while getopts ":a" opt; do
    case $opt in
        a)
            aur=true
            ;;
        \?)
            echo "Error: Invalid option: -$OPTARG" >&2
            usage
            exit 1
            ;;
    esac
done

# Shift the parsed options out of the argument list
shift $((OPTIND - 1))

# Get the package name
package="$1"

# Check if the package name is empty
if [ -z "$package" ]; then
    echo "Error: Package name is missing."
    usage
    exit 1
fi

# Pull the PKGBUILD function

get_pkgbuild()
{
    if [ $aur = true ] ; then 
        paru -G "$package"
    else
        pkgctl repo clone "$package"
    fi
}



echo "Pulling PKGBUILD for $package ..."
get_pkgbuild
rm -rf "$package/.git"
echo "Done."