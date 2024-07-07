#! /usr/bin/bash

# Apply a patch to a PKGBUILD

# Usage example: applypatch.sh <patch file> 

script_dir=$(realpath $(dirname "$0"))

patch  -p1 < "$script_dir/patches/$1.patch"