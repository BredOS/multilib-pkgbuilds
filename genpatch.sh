#! /usr/bin/bash 
set -x
# Generate a patch between the original PKGBUILD/folder and the new one
# Usage example: genpatch.sh <new PKGBUILD folder>

working_dir=$(pwd)
#get pkgname
pkgname=$(basename "$1")
#expand full path new PKGBUILD folder
newpkgbuild=$(realpath "$1")

generate_patch()
{
    tempdir=$(mktemp -d -p "$working_dir")
    cd "$tempdir"
    pkgctl repo clone "$pkgname"
    rm -rf "$pkgname/.git"
    diff -Naur "./$pkgname" "../$pkgname" > "$working_dir/patches/$pkgname.patch"
    rm -rf "$tempdir"
}

generate_patch "$newpkgbuild"