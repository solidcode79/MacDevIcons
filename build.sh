#!/usr/bin/env bash
set -e  

# run with --debug if required!
DEBUG=0
LSREGISTER="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"
APP_NAME="MacDevIcons.app"
BUILD_NAME="./build/MacDevIcons.app"


if [ ! -d ".venv" ]; then
    echo "No .venv folder found. Recreating virtual environment..."
    rm -rf .venv
    python3 -m venv .venv
    echo "Virtual environment created."
    source .venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo ".venv exists. Activating existing virtual environment..."
    source .venv/bin/activate
fi

python3 start.py

echo "Moving APP to /Applications/ ..."
rm -rf "/Applications/$APP_NAME"
mv -f "$BUILD_NAME" /Applications/

echo "Refreshing LaunchServices registration..."
$LSREGISTER -R -f "/Applications/$APP_NAME"

echo "Restarting Finder to refresh icons..."
killall Finder || true

echo "Done!"