# Configure the repos in here

debug = False

repos = [
    "https://repo.bredos.org/repo/BredOS-multilib/aarch64/BredOS-multilib.db.tar.gz",
    "https://geo.mirror.pkgbuild.com/multilib/os/x86_64/multilib.db.tar.gz",
    "http://dk.mirror.archlinuxarm.org/armv7h/extra/extra.db.tar.gz",
]

ignore = [
    "lib32-libxcrypt-compat",
    "lib32-libcurl-compat",
    "lib32-libcurl-gnutls",
    "lib32-libxkbcommon-x11",
    "lib32-libpipewire",
    "lib32-pipewire-jack",
    "lib32-pipewire-v4l2",
    "lib32-jack2",
    "lib32-libva-mesa-driver",
    "lib32-mesa",
    "lib32-mesa-vdpau",
    "lib32-opencl-clover-mesa",
    "lib32-nss",
    "lib32-openal",
    "lib32-spirv-llvm-translator",
    "lib32-harfbuzz-cairo",
    "lib32-harfbuzz-icu",
]

alias = {
    #    "packagename": ["alternative", "package", "names"],
    #    "packagename": "also supported",
    "lib32-valgrind": "valgrind",
    "lib32-xorgproto": "xorgproto",
    "lib32-xtrans": "xtrans",
    "lib32-libmysofa": "libmysofa",
    "lib32-libomxil-bellagio": "libomxil-bellagio",
    "lib32-directx-headers": "directx-headers",
    "lib32-cunit": "cunit",
}

localpkgs = [
    "lib32-glibc",
    "lib32-xtrans",
    "lib32-xorgproto",
    "lib32-vulkan-headers",
    "lib32-mesa-panfork-git",
    "lib32-valgrind",
    "lib32-nss",
    "lib32-libmysofa",
    "lib32-cunit",
    "lib32-directx-headers",
    "lib32-libomxil-bellagio",
    "box86-git",
    "box86-rk3588-git",
    "lib32-gl4es-git",
]
localpkgs_without_makepkg_conf = [
    "arm32-binutils",
    "arm32-gcc",
    "arm32-linux-api-headers",
    "arm32-gcc-bootstrap",
    "arm32-filesystem",
    "box64-git",
    "box64-rk3588-git",
    "gl4es-git",
    "steam-libs",
]
