#!/bin/bash

set -e

TRACE_DIR=/src/result
mkdir -p $TRACE_DIR

ARCHIVE=$(find /src -maxdepth 1 -name "*.tar.*" | head -n 1)
if [ -z "$ARCHIVE" ]; then
    echo "ERROR: archive not found in /src"
    exit 1
fi

echo "Found archive: $ARCHIVE"
mkdir -p source_code
tar -xf $ARCHIVE -C source_code --strip-components=1

apt-get update -qq
apt build-dep -y ./source_code

cd source_code || exit 1

strace -ff -s 65535 -v -yy \
    -e trace=openat,execve,stat,lstat \
    -o $TRACE_DIR/build_trace \
    dpkg-buildpackage -b -uc -us

cd ..
rm -rf source_code
find /src -mindepth 1 \
    ! -path "$ARCHIVE" \
    ! -path "$TRACE_DIR*" \
    -exec rm -rf {} + 2>/dev/null || true

echo "Done. Traces saved to $TRACE_DIR"
exit 0
