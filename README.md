# BredOS multilib repository

![Outdated Packages](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/rippanda12/b5759b3d8a067b7e96f73934f43bf2ce/raw/outdated-packages-multilib.json)

## Adding the repository
```ini
[BredOS-multilib]
Include = /etc/pacman.d/bredos-mirrorlist
```

## Building a package

First set `PKGDEST=` in `makepkg.conf` to the directory where you want the packages to be stored.

Then run:

```sh
./buildpkg.sh <package>
```

## Contributing

Remember to run `pre-commit install` after cloning.

If you want to add a package that exists in archlinux's multilib repo, you need to pull the PKGBUILD using './pullpkg.sh <package>'.
Then modify it so it compiles for ARM32 heres some tips when doing that:

- `CC` `CXX` should be set to the folowing in the `PKGBUILD`:

```sh
export CC="armv7h-linux-gnueabihf-gcc"
export CXX="armv7h-linux-gnueabihf-g++"
```

- Remove any `cflags` or `cxxflags` that are `-m32` or `-mstackrealign`.

- `PKGCONFIG` should be set to the folowing in the `PKGBUILD`:

```sh
export PKG_CONFIG="armv7h-linux-gnueabihf-pkg-config"
````

- You need to add `--includedir=/usr/include32` to the `./configure` line in the `PKGBUILD` or if it uses `cmake` you need to add `-DCMAKE_INSTALL_INCLUDEDIR=include32` to the `cmake` line.

- You need to add `--libdir=/usr/lib32` to the `./configure` line in the `PKGBUILD` or if it uses `cmake` you need to add `-DCMAKE_INSTALL_LIBDIR=lib32` to the `cmake` line.

- If package uses `meson` or `arch-meson` you can use `--cross-file arm-lib32` to set `CC`, `CXX`, `PKG_CONFIG`, `libdir` and `includedir` to the correct values.