import os
import json

BUILD_KEYWORDS = ["gcc", "ld", "cc", "clang", "make", "cc1"]  # "rustc", "go", "as", "cmake", "configure"

BASE_DIR = 'sources'

for project in os.listdir(BASE_DIR):
    project_path = os.path.join(BASE_DIR, project)
    result_dir = os.path.join(project_path, 'result')
    output_path = os.path.join(project_path, 'interesting.json')

    if not os.path.isdir(result_dir):
        print(f"В {project} отсутствует результат трассировки, возможны ошибки при сборке")
        continue

    project_results = []

    for filename in os.listdir(result_dir):
        if not filename.startswith("build_trace."):
            continue

        filepath = os.path.join(result_dir, filename)

        try:
            with open(filepath, 'r', errors='ignore') as rfile:
                for line in rfile:
                    if 'execve(' not in line:
                        continue

                    for keyword in BUILD_KEYWORDS:
                        if f'/{keyword}' in line or f'"{keyword}' in line:
                            project_results.append({
                                'filename': filename,
                                'exec_path': line.split('execve("')[1].split('"')[0],
                                'match_line': line.strip()
                            })
                            break  # остановиться после первого совпадения
        except Exception as e:
            print(f"Ошибка при обработке {filepath}: {e}")

    if project_results:
        with open(output_path, 'w') as out:
            json.dump(project_results, out, indent=4)
        print(f"В {project} найдено {len(project_results)} интересных процессов")
    else:
        print(f"В {project} не найдено интересных процессов")
