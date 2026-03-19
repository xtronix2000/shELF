import sys
import json
import docker
from pathlib import Path

from core.log_parser import parse_line
from core.analyzer import analyze
from sandbox.runner import build_image, run_build


def run_analysis(project_path: Path) -> None:
    result_dir = project_path / "result"

    if not result_dir.exists():
        print(f"[-] Отсутствует директория с результатами: {result_dir}")
        return

    hits = []

    for log_file in result_dir.iterdir():
        if not log_file.name.startswith("build_trace."):
            continue

        with open(log_file, "r", errors="ignore") as f:
            for line in f:
                event = parse_line(line, log_file.name)
                if event is None:
                    continue
                hit = analyze(event)
                if hit is None:
                    continue
                hits.append({
                    "interpreter": hit.interpreter,
                    "evidence_type": hit.evidence_type,
                    "indicator": hit.indicator,
                    "source_log": hit.event.source_log,
                    "path": hit.event.path,
                    "args": hit.event.args,
                })

    output = project_path / "interpreters.json"
    with open(output, "w") as f:
        json.dump(hits, f, indent=4)

    print(f"[+] АНализ завершен: {len(hits)} hits → {output}")


def main():
    rebuild = "--rebuild" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if len(args) != 1:
        print("Использование: python main.py <path_to_project> [--rebuild]")
        sys.exit(1)

    project_path = Path(args[0])

    if not project_path.exists():
        print(f"[-] Путь не найден: {project_path}")
        sys.exit(1)

    client = docker.from_env()

    build_image(client, force=rebuild)
    success = run_build(client, project_path)

    if not success:
        sys.exit(1)

    run_analysis(project_path)


if __name__ == "__main__":
    main()