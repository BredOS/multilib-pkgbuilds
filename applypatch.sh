#! /usr/bin/bash

# Apply a patch to a PKGBUILD

# Usage example: applypatch.sh <patch file> 

patch  -p1 < "$1"