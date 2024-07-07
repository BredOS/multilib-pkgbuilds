#! /bin/bash
set -x
# Script for building packages with BredOS patches

# Make temp dir
# Get the pkg using pullpkg.sh pkgname
# patch it using /patches/pkgname.patch
# build it using makepkg

# Usage function
usage() {
    echo "Usage: $0 <package>"
}

# Check if the package name is empty
if [ -z "$1" ]; then
    echo "Error: Package name is missing."
    usage
    exit 1
fi

# Script dir (expand it to full path)
script_dir=$(realpath $(dirname "$0"))
localpkgs="arm32-binutils|arm32-gcc|arm32-linux-api-headers|arm32-gcc-bootstrap|arm32-filesystem|lib32-glibc"
# Get the package name
package="$1"

# Make temp dir
tempdir=$(mktemp -d)
cd "$tempdir"

# Pull the PKGBUILD
if [[ $package =~ $localpkgs ]]; then
    cp -r "$script_dir"/"$package" .
    cd "$package"
else
    "$script_dir"/pullpkg.sh "$package"
    cd "$package"
    "$script_dir"/applypatch.sh "$package"
fi

echo "Building $package ..."

makepkg -srAfi --nocheck --noconfirm --skippgpcheck --config="$script_dir/makepkg.conf"

echo "Done."

pacman -Ql "$package"