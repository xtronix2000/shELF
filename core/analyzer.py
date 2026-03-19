from core.models import BuildEvent, DetectionHit
from core.signatures import INTERPRETERS, LINKER_TOOLS


def check_execve(event: BuildEvent) -> DetectionHit | None:
    # проверяем что это вызов линкера/компилятора
    tool = event.path.split("/")[-1]  # /usr/bin/gcc → gcc
    if tool not in LINKER_TOOLS:
        return None

    for interp, sigs in INTERPRETERS.items():
        for arg in event.args:
            # проверяем флаги: -llua5.3
            for flag in sigs["linker_flags"]:
                if arg == flag:
                    return DetectionHit(
                        interpreter=interp,
                        evidence_type="linker_flag",
                        indicator=arg,
                        event=event,
                    )
            # проверяем .a файлы в аргументах: liblua.a, ./liblua/liblua.a
            for lib in sigs["static_libs"]:
                if arg.endswith(lib):
                    return DetectionHit(
                        interpreter=interp,
                        evidence_type="static_lib",
                        indicator=arg,
                        event=event,
                    )

    return None


def check_openat(event: BuildEvent) -> DetectionHit | None:
    for interp, sigs in INTERPRETERS.items():
        for prefix in sigs["lib_paths"]:
            if event.path.startswith(prefix):
                return DetectionHit(
                    interpreter=interp,
                    evidence_type="openat_archive",
                    indicator=event.path,
                    event=event,
                )

    return None


def analyze(event: BuildEvent) -> DetectionHit | None:
    if event.event_type == "execve":
        return check_execve(event)
    if event.event_type == "openat":
        return check_openat(event)
    return None