LINKER_TOOLS = [
    "gcc", "cc", "g++", "c++",   # компиляторы которые могут вызывать линкер
    "ld", "ld.lld", "ld.gold",   # линкеры
    "cc1",                       # внутренний фронтенд gcc
]

INTERPRETERS = {
    "lua": {
        "linker_flags": [
            "-llua", "-llua5.1", "-llua5.2", "-llua5.3", "-llua5.4",
        ],
        "static_libs": [
            "liblua.a", "liblua5.1.a", "liblua5.2.a", "liblua5.3.a", "liblua5.4.a",
        ],
        "lib_paths": [
            "/usr/lib/liblua",
            "/usr/lib/x86_64-linux-gnu/liblua",
            "/usr/local/lib/liblua",
        ],
    },
    "python": {
        "linker_flags": [
            "-lpython", "-lpython2.7",
            "-lpython3", "-lpython3.8", "-lpython3.9",
            "-lpython3.10", "-lpython3.11", "-lpython3.12",
        ],
        "static_libs": [
            "libpython2.7.a",
            "libpython3.8.a", "libpython3.9.a", "libpython3.10.a",
            "libpython3.11.a", "libpython3.12.a",
        ],
        "lib_paths": [
            "/usr/lib/libpython",
            "/usr/lib/x86_64-linux-gnu/libpython",
            "/usr/local/lib/libpython",
        ],
    },
    "perl": {
        "linker_flags": [
            "-lperl", "-lperl5",
            "-lperl5.32", "-lperl5.34", "-lperl5.36",
        ],
        "static_libs": [
            "libperl.a", "libperl5.a",
            "libperl5.32.a", "libperl5.34.a", "libperl5.36.a",
        ],
        "lib_paths": [
            "/usr/lib/libperl",
            "/usr/lib/x86_64-linux-gnu/libperl",
            "/usr/local/lib/libperl",
        ],
    },
}