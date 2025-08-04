#!/bin/bash

# Обновим списки пакетов, потому что в runtime они могут быть устаревшими
apt update

# Файл трассироки сборки
TRACE_DIR=/src/result
mkdir $TRACE_DIR

# Распакуем архив с исходниками в source_code директорию
ARCHIVE=$(find /src -maxdepth 1 -name "*.tar.*" | head -n 1)
mkdir -p source_code
tar -xf $ARCHIVE -C source_code --strip-components=1

# Установка зависимостей
apt build-dep -y ./source_code

# Заходим в директорию с исходниками
cd source_code || exit 1

# Отслеживание сборки deb пакета
strace -ff -s 65535 -v -yy -e trace=openat,execve,file -o $TRACE_DIR/build_trace dpkg-buildpackage -b -uc -us

# Удаление собранных пакетов и исходного кода
cd ..
rm -rf source_code
find /src -mindepth 1 ! -path "$ARCHIVE" ! -path "$TRACE_DIR*" -exec rm -rf {} +

# Сессия
#bash
exit 0
