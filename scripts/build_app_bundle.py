#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
import plistlib


BUNDLE_NAME = "MacDevIcons"

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_FILE = BASE_DIR / "config" / "config.json"
INPUT_RESOURCES_DIR = BASE_DIR / "Resource"
BACKUP_APP = INPUT_RESOURCES_DIR / "MacDevIcons.app"
INPUT_INFO_PLIST = BACKUP_APP / "Contents" / "info.plist"


ICNS_DIR = BASE_DIR / "build" / "icns"
DIST_DIR = BASE_DIR / "build"
APP_BUNDLE = DIST_DIR / f"{BUNDLE_NAME}.app"

CONTENTS_DIR = APP_BUNDLE / "Contents"
MACOS_DIR = CONTENTS_DIR / "MacOS"
RESOURCES_DIR = CONTENTS_DIR / "Resources"
OUPTUT_INFO_PLIST = CONTENTS_DIR / "Info.plist"

def get_available_file_ext():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)

    # TODO: make keys value and values as keys
    # WHY: multiple extensions html, htm can be same type HTML
    return data.get("extensions", {})

def clean_bundle():
    if APP_BUNDLE.exists():
        shutil.rmtree(APP_BUNDLE)

def copy_icns_files():
    if not ICNS_DIR.is_dir():
        raise SystemExit(f"ICNS directory not found: {ICNS_DIR}")

    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)

    icns_files = list(ICNS_DIR.glob("*.icns"))
    if not icns_files:
        raise SystemExit(f"No .icns files found in {ICNS_DIR}")

    for f in icns_files:
        shutil.copy2(f, RESOURCES_DIR / f.name)


def make_executable_stub():
    MACOS_DIR.mkdir(parents=True, exist_ok=True)

def make_entry(ext: str, type_name: str):
    return {
        "CFBundleTypeName": type_name,
        "CFBundleTypeExtensions": [ext],
        "CFBundleTypeRole":"Editor",
        "CFBundleTypeIconFile": ext,        # icon file name
        "LSHandlerRank": "Owner"         # strongest claim
    }
    
def build_plist():
    fileExt = get_available_file_ext()

    with open(INPUT_INFO_PLIST, 'rb') as f:
        data = plistlib.load(f)

    doc_types = data.get("CFBundleDocumentTypes")
    if doc_types is None:
        doc_types = []
        data["CFBundleDocumentTypes"] = doc_types
    
    for ext, name in fileExt.items():
        doc_types.append(make_entry(ext, name))
    
    with open(OUPTUT_INFO_PLIST, "wb") as f:
        plistlib.dump(data, f, sort_keys=False)

def copy_app_icns():
    src = Path(INPUT_RESOURCES_DIR / "MacDevIcon.icns")
    dst = Path(RESOURCES_DIR / "MacDevIcon.icns")
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)   # preserves metadata
    pass
    
def copy_fresh_bundle():
    src = Path(BACKUP_APP)          # path to your source file
    dst = Path(DIST_DIR / "MacDevIcons.app")
    
    print (src)
    print(dst)
    if dst.exists():
        shutil.rmtree(dst)     

    shutil.copytree(src, dst)



def main():
    print(f"Building app bundle at: {APP_BUNDLE}")
    clean_bundle()
    copy_fresh_bundle()
    copy_icns_files()
    build_plist()

    print(f"Created app bundle: {APP_BUNDLE}")

if __name__ == "__main__":
    main()