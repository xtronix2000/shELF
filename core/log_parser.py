import re
from core.models import BuildEvent

# execve("/usr/bin/ld", ["/usr/bin/ld", "-o", "nmap", "main.o", "-llua5.3"], ...)  = 0
EXECVE_RE = re.compile(r'execve\("([^"]+)",\s*\[([^\]]+)\].*=\s*(-?\d+)')

# openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/liblua5.3.a", O_RDONLY) = 3
OPENAT_RE = re.compile(r'openat\([^,]+,\s*"([^"]+)".*=\s*(-?\d+)')


def parse_execve(line: str, source_log: str) -> BuildEvent | None:
    match = EXECVE_RE.search(line)
    if not match:
        return None

    path = match.group(1)
    args_raw = match.group(2)
    status = int(match.group(3))

    # аргументы в логе выглядят так: "/usr/bin/ld", "-o", "nmap", "-llua5.3"
    args = re.findall(r'"([^"]*)"', args_raw)

    return BuildEvent(
        event_type="execve",
        path=path,
        args=args,
        status=status,
        source_log=source_log,
    )


def parse_openat(line: str, source_log: str) -> BuildEvent | None:
    match = OPENAT_RE.search(line)
    if not match:
        return None

    path = match.group(1)
    status = int(match.group(2))

    # интересуют только успешно открытые .a файлы
    if not path.endswith(".a") or status < 0:
        return None

    return BuildEvent(
        event_type="openat",
        path=path,
        args=[],
        status=status,
        source_log=source_log,
    )


def parse_line(line: str, source_log: str) -> BuildEvent | None:
    if "execve(" in line:
        return parse_execve(line, source_log)
    if "openat(" in line:
        return parse_openat(line, source_log)
    return None