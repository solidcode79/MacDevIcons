#!/usr/bin/env bash
set -e  

# run with --debug if required!
DEBUG=0
APP_NAME="MacDevIcons.app"
APP_PATH="/Applications/$APP_NAME"
BUILD_OUTPUT="./build/$APP_NAME"
LSREGISTER="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister"


for arg in "$@"; do
    if [ "$arg" = "--debug" ]; then
        DEBUG=1
    fi
done

echo "Removing ./build folder..."
rm -rf ./build

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

echo "Running build scripts..."
python3 ./scripts/build_icons.py
echo ""
python3 ./scripts/build_app_bundle.py
echo ""

if [ ! -d "$BUILD_OUTPUT" ]; then
    echo "ERROR: Expected app bundle $BUILD_OUTPUT not found!"
    exit 1
fi

# Sign the application and clear the wierdo flags!
touch /Applications/MacDevIcons.app
xattr -cr "$BUILD_OUTPUT"
codesign --force --sign - "$BUILD_OUTPUT/Contents/document.wflow"
codesign --force --sign - "$BUILD_OUTPUT"
codesign --verify --verbose "$BUILD_OUTPUT"
 
echo "Copying $APP_NAME to /Applications/ ..."
rm -rf "/Applications/$APP_NAME"
cp -R "$BUILD_OUTPUT" /Applications/

echo "Refreshing LaunchServices registration..."
$LSREGISTER -v -lint -R -f "/Applications/$APP_NAME"

echo "Restarting Finder and Dock to refresh icons..."
killall Finder || true
killall Dock || true

echo "Done!"