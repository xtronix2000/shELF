# shELF

Static interpreter detection tool for ELF binaries.

Traces the build process of Debian packages using `strace` and analyzes 
syscall logs to detect statically linked interpreter libraries (Lua, Python, Perl).

## How it works
```
Source archive → Docker sandbox → strace logs → Analysis → results
```

The tool intercepts linker calls during compilation and looks for interpreter 
signatures in arguments — linker flags (`-llua5.3`), static archives (`liblua.a`), 
and direct file opens (`openat` on `.a` files).

## Usage

**Web interface**
```bash
flask --app web/app.py run
```
Open `http://localhost:5000`, upload a source archive and get results in the browser.

**CLI**
```bash
python main.py sources/<project>/
```
Results are written to `sources/<project>/interpreters.json`.

To force rebuild the Docker image:
```bash
python main.py sources/<project>/ --rebuild
```

## Preparing source archives
```bash
docker run --rm -v "./sources/<project>:/out" debian:12 bash -c \
  "echo 'deb-src http://deb.debian.org/debian bookworm main' >> /etc/apt/sources.list \
  && apt-get update -qq && apt-get install -y dpkg-dev \
  && cd /out && apt-get source <package>"

cd sources/<project>
tar -czf source.tar.gz <unpacked-dir>/
rm -rf <unpacked-dir>/ *.dsc *.xz
```

## Requirements
```bash
pip install -r requirements.txt
```

Docker must be running.