from pathlib import Path
import shutil
import subprocess

# Internal
from scripts import settings
from scripts import applescript
from scripts import build_icons
from scripts import update_plist


APP_PATH = Path("build/MacDevIcons.app")
APP_RESOURCES = APP_PATH / "Contents" / "Resources"
APPLESCRIPT_PATH = Path("build/tmp/main.applescript")
ICNS_DIR = Path("build/icns/")

def copy_icns_files():
    if not ICNS_DIR.is_dir():
        raise SystemExit(f"ICNS directory not found: {ICNS_DIR}")


    icns_files = list(ICNS_DIR.glob("*.icns"))
    if not icns_files:
        raise SystemExit(f"No .icns files found in {ICNS_DIR}")

    for f in icns_files:
        shutil.copy2(f, APP_RESOURCES / f.name)


def main():
    # Read the settings
    print("Building the MacDevIcons app ... ")
    config = settings.load_config(Path("./config/config.json"))

    # print("Command:", config.command)
    # print("File Associations:", config.file_associations)
    # print("UTI Associations:", config.uti_associations)

    # Compile new app bundle 
    shutil.rmtree("./build/", ignore_errors=True)
    try: 
        Path("build/tmp").mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        raise SystemExit("Somehow the build dir could NOT be cleaned quiting!")
    
    APPLESCRIPT_PATH.write_text(applescript.generate_applescript(config.command))
    subprocess.run([
        "osacompile",
        "-o", str(APP_PATH),
        str(APPLESCRIPT_PATH),
    ], check=True)
    Path(APP_RESOURCES / "droplet.icns").unlink()
    Path(APP_RESOURCES / "assets.car").unlink()
    shutil.copy2("./Resources/droplet.icns", APP_RESOURCES)
    APP_PATH.touch()
    
    
    # Generate the icons
    print("Base app bundle is ready ... generating the icons")
    build_icons.build_icons_all(config.file_associations, config.uti_associations)
    copy_icns_files()
    print("Icons are ready ... updating the plist")
    update_plist.update_plist(APP_PATH, config.file_associations, config.uti_associations)
    APP_PATH.touch()
    
    
    print("Done building the MacDevIcons app!")
    
if __name__ == "__main__":
    main()