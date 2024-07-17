# Configure the repos in here

debug = True

repos = [
    "https://geo.mirror.pkgbuild.com/multilib/os/x86_64/multilib.db.tar.gz",
    "https://repo.bredos.org/repo/BredOS-multilib/aarch64/BredOS-multilib.db.tar.gz",
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
}
