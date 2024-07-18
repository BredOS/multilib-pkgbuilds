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
