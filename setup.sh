#!/bin/bash
source venv/bin/activate

echo "Checking for a valid python installation....."
echo "Your python version is"
python -V
found=`python -V |& grep -c Python`

if [ $found -ne 1 ]; then
	echo "Please install python and restart script"
	exit 1
fi

echo "Installing dependencies"
pip install -r requirements.txt

echo "Checking System Configuration"
uname -s


echo "Running scraping script"

if [ "$(uname)" == "Darwin" ]; then
	echo "Mac 32"
    python scrape.py m32        
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    if [ "$(expr substr $(uname -m) 1 3)" == "x86" ]; then
    	echo "Linux 64"
    	python scrape.py l64        
	elif [ "$(expr substr $(uname -m) 1 4)" == "i686" ]; then
    	echo "Linux 32"
    	python scrape.py l32     
	fi
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    echo "Microsoft 32"
    python scrape.py win32.exe
fi

deactivate