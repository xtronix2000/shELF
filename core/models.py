from dataclasses import dataclass, field


@dataclass
class BuildEvent:
    event_type: str      # "execve" или "openat"
    path: str            # путь к исполняемому файлу или открываемому файлу
    args: list[str]      # аргументы (для execve — argv, для openat — пустой список)
    status: int          # 0 = успех, -1 = ошибка
    source_log: str      # имя файла лога откуда событие (build_trace.123)


@dataclass
class DetectionHit:
    interpreter: str     # "lua", "python", "perl"
    evidence_type: str   # "linker_flag", "static_lib", "openat_archive"
    indicator: str       # конкретная строка-улика: "-llua5.3", "liblua.a"
    event: BuildEvent    # исходное событие целиком