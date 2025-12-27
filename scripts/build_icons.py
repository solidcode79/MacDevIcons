#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from PIL import Image
from PIL.Image import Resampling


# ----------------------------------------
# CONFIG
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]
DEVICON_DIR = BASE_DIR / "vendor" / "devicon" / "icons"
BUILD_DIR = BASE_DIR / "build"
PNG_1024_DIR = BUILD_DIR / "png_1024"
ICONSET_DIR = BUILD_DIR / "iconsets"
ICNS_DIR = BUILD_DIR / "icns"

# Required macOS icon sizes
ICON_SIZES = [
    (16, "icon_16x16.png"),
    (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"),
    (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"),
    (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"),
    (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"),
    (1024, "icon_512x512@2x.png"),
]


# ----------------------------------------
# Helpers
# ----------------------------------------

def ensure_dirs():
    PNG_1024_DIR.mkdir(parents=True, exist_ok=True)
    ICONSET_DIR.mkdir(parents=True, exist_ok=True)
    ICNS_DIR.mkdir(parents=True, exist_ok=True)

def pick_svg_icon(devicon_name: str) -> Path:
    """
    Look for *-original.svg or fallback to *-plain.svg
    """
    icon_folder = DEVICON_DIR / devicon_name

    if not icon_folder.exists():
        raise FileNotFoundError(f"❌ Devicon folder not found: {icon_folder}")

    # Prefer original.svg
    for candidate in [f"{devicon_name}-original.svg"]:
        path = icon_folder / candidate
        if path.exists():
            return path

    # Otherwise fallback to plain.svg
    for candidate in [f"{devicon_name}-plain.svg"]:
        path = icon_folder / candidate
        if path.exists():
            return path

    raise FileNotFoundError(
        f"No usable SVG in {icon_folder}. Expected *original.svg or *plain.svg"
    )

def convert_svg_to_1024_png(svg_path: Path, filetype: str) -> Path:
    # Actually NOT 1024  but of original size
    out_path = PNG_1024_DIR / f"{filetype}.png"

    import resvg_py.resvg_py as resvg
    
    svg_string = svg_path.read_text(encoding="utf-8")
    
    png_bytes = resvg.svg_to_bytes(svg_string)
   
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(png_bytes)

    #print(f"Created PNG 1024: {out_path}")
    return out_path    

def create_iconset(png_1024: Path, filetype: str) -> Path:
    iconset_path = ICONSET_DIR / f"{filetype}.iconset"
    iconset_path.mkdir(parents=True, exist_ok=True)

    base_img = Image.open(png_1024)

    # Generate all required sizes
    for size, filename in ICON_SIZES:
        resized = base_img.resize((size, size), Resampling.LANCZOS)
        out_file = iconset_path / filename
        resized.save(out_file)
    
    #print(f"Created iconset: {iconset_path}")
    return iconset_path


def convert_iconset_to_icns(iconset_path: Path, filetype: str) -> Path:
    out_icns = ICNS_DIR / f"{filetype}.icns"
    subprocess.run(
        ["iconutil", "-c", "icns", str(iconset_path), "-o", str(out_icns)],
        check=True
    )
    # print(f"Created ICNS: {out_icns}")
    return out_icns


def process_all(filetype: str, devicon_name: str):
    print(f"Processing: {filetype} -> {devicon_name}")

    svg_path = pick_svg_icon(devicon_name)
    png_1024 = convert_svg_to_1024_png(svg_path, devicon_name)
    iconset_path = create_iconset(png_1024, devicon_name)
    convert_iconset_to_icns(iconset_path, devicon_name)


def build_icons_all(mapping_ext, mapping_uti):
    ensure_dirs()
    mapping = mapping_ext | mapping_uti

    for filetype, devicon_name in mapping.items():
        try:
            process_all(filetype, devicon_name)
        except Exception as e:
            print(f"❌ Skipping {filetype}: {e}")
            


