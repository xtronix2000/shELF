# shELF

Static interpreter detection tool for ELF binaries.

Traces the build process of Debian packages using `strace` and analyzes 
syscall logs to detect statically linked interpreter libraries (Lua, Python, Perl).

## How it works
```
Source archive → Docker sandbox → strace logs → Analysis → interpreters.json
```

The tool intercepts linker calls during compilation and looks for interpreter 
signatures in arguments — linker flags (`-llua5.3`), static archives (`liblua.a`), 
and direct file opens (`openat` on `.a` files).

## Usage
```bash
python main.py sources/<project>/
```

That's it. The tool will:
1. Build the Docker image (once, cached on subsequent runs)
2. Run the build inside a sandbox and collect strace logs
3. Analyze logs and write results to `sources/<project>/interpreters.json`

To force rebuild the Docker image:
```bash
python main.py sources/<project>/ --rebuild
```

## Project structure
```
shELF/
├── main.py              # Entry point
├── core/
│   ├── models.py        # BuildEvent, DetectionHit dataclasses
│   ├── signatures.py    # Interpreter signatures dictionary
│   ├── log_parser.py    # strace line → BuildEvent
│   └── analyzer.py      # BuildEvent → DetectionHit
├── sandbox/
│   ├── Dockerfile       # Debian 12 build environment
│   ├── tracer.sh        # Runs dpkg-buildpackage under strace
│   └── runner.py        # Docker SDK wrapper
└── sources/             # Place project archives here
    └── <project>/
        └── <source>.tar.gz
```

## Preparing source archives

Download Debian source packages:
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