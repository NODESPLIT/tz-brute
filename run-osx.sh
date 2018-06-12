#!/bin/bash

echo
echo INSTALLING TOOLS:

if command -v brew &>/dev/null; then
	echo - homebrew is installed
else
    echo - installing homebrew...
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

if brew ls --versions libsodium > /dev/null; then
	echo - libsodium is installed
else
	echo - installing libsodium...
	brew install libsodium
fi

if command -v python3 &>/dev/null; then
	echo - python3 is installed
else
    echo - installing python3...
    brew install python3
fi

if command -v pip3 &>/dev/null; then
	echo - pip3 is already installed
else
    echo - pip3 is not installed!
    exit 1
fi

if ! python3 -c "import bitcoin, pysodium, pyblake2" &> /dev/null; then
	echo
	echo INSTALLING DEPENDENCIES:
	pip3 install -r requirements.txt
fi

echo
echo STARTING TZ-BRUTE

echo
python3 main.py