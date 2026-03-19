import docker
import sys
import os
from pathlib import Path

IMAGE_NAME = "strace-hunter"
DOCKERFILE_DIR = Path(__file__).parent  # там где лежит main.py


def build_image(client: docker.DockerClient, force: bool = False) -> None:
    if not force:
        try:
            client.images.get(IMAGE_NAME)
            print("[+] Image already exists, skipping build")
            return
        except docker.errors.ImageNotFound:
            pass

    print("[*] Building Docker image...")
    client.images.build(path=str(DOCKERFILE_DIR), tag=IMAGE_NAME, rm=True)
    print("[+] Image ready")


def run_build(client: docker.DockerClient, project_path: Path) -> bool:
    print(f"[*] Running build for: {project_path.name}")

    container = client.containers.run(
        image=IMAGE_NAME,
        volumes={str(project_path.resolve()): {"bind": "/src", "mode": "rw"}},
        remove=True,
        detach=True,
    )

    # Стримим логи контейнера в реальном времени
    for log in container.logs(stream=True):
        print(log.decode().strip())

    result = container.wait()
    exit_code = result["StatusCode"]

    if exit_code != 0:
        print(f"[-] Build failed with exit code {exit_code}")
        return False

    print("[+] Build complete")
    return True
