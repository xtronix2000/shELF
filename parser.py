import os
import json
import re

BASE_DIR = 'sources'
OUTPUT_JSON = "interpreters.json"

interpreters = {
    "lua": [
        "-llua", "-llua5.1", "-llua5.2", "-llua5.3", "-llua5.4",
        "liblua.a", "liblua5.1.a", "liblua5.2.a", "liblua5.3.a", "liblua5.4.a",
        "/usr/lib/liblua", "/usr/lib/x86_64-linux-gnu/liblua"
    ],
    "python": [
        "-lpython", "-lpython2.7", "-lpython3", "-lpython3.5", "-lpython3.6", "-lpython3.7",
        "-lpython3.8", "-lpython3.9", "-lpython3.10", "-lpython3.11", "-lpython3.12",
        "libpython.a", "libpython2.7.a", "libpython3.5.a", "libpython3.6.a",
        "libpython3.7.a", "libpython3.8.a", "libpython3.9.a", "libpython3.10.a",
        "libpython3.11.a", "libpython3.12.a",
        "/usr/lib/libpython", "/usr/lib/x86_64-linux-gnu/libpython",
    ],
    "perl": [
        "-lperl", "-lperl5", "-lperl5.28", "-lperl5.30", "-lperl5.32", "-lperl5.34",
        "libperl.a", "libperl5.a", "libperl5.28.a", "libperl5.30.a", "libperl5.32.a", "libperl5.34.a",
        "/usr/lib/libperl", "/usr/lib/x86_64-linux-gnu/libperl",
    ]
}


def parse_log_contents(content):
    entries = []
    for line in content.split('\n'):
        if 'execve(' in line:
            args = re.findall(r'([^,]+)', line)
            command = [arg.strip() for arg in args if arg.strip()]
            status = 0 if '= 0)' in line else -1
            error = re.search(r'E([\w]+) \(([^)]+)\)', line)
            entries.append({
                "command": command,
                "output": {"status": status, "error": error.group(2) if error else None}
            })
    return entries


hits = {}

for project in os.listdir(BASE_DIR):
    project_path = os.path.join(BASE_DIR, project)
    result_dir = os.path.join(project_path, 'result')
    interesting_json = os.path.join(project_path, 'interesting.json')

    if not os.path.isfile(interesting_json):
        print(f"В {project} отсутствует interesting.json")
        continue

    with open(interesting_json, 'r') as rfile:
        json_data = json.load(rfile)

    for entry in json_data:
        log_path = os.path.join(result_dir, entry["filename"])
        try:
            with open(log_path, "r", errors="ignore") as log_file:
                content = log_file.read().lower()
                for interp, indicators in interpreters.items():
                    for indicator in indicators:
                        if indicator.lower() in content:
                            if project not in hits:
                                hits[project] = []
                            project_hits = hits[project]
                            project_hit = next((hit for hit in project_hits if hit['interpreter'] == interp), None)

                            if not project_hit:
                                project_hit = {
                                    "interpreter": interp,
                                    "indicators": [indicator],
                                    "files": {entry["filename"]: parse_log_contents(content)}
                                }
                                project_hits.append(project_hit)
                            else:
                                if entry["filename"] not in project_hit['files']:
                                    project_hit['files'][entry["filename"]] = parse_log_contents(content)
                                else:
                                    project_hit['files'][entry["filename"]].extend(parse_log_contents(content))

                            project_hit["indicators"] = list(set(project_hit["indicators"]) | {indicator})
                            break
        except Exception as e:
            print(f"Ошибка при обработке {log_path}: {e}")

with open(OUTPUT_JSON, 'w') as wfile:
    json.dump({"projects": hits}, wfile, indent=4, ensure_ascii=False)


total_interpreters = sum(len(project) for project in hits.values())
print(f"Анализ завершён. Обнаружено {total_interpreters} интерпретаторов, сохранено в {OUTPUT_JSON}")
