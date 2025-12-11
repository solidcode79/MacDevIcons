# MacDevIcons
Beautiful developer file-type icons for macOS Finder — powered by https://devicon.dev


## Pull
``` Shell
git clone https://github.com/solidcode79/MacDevIcons
cd MacDevIcons
git submodule update --init --recursive
```

## Setup Python ENV
MacDevIcons uses pinned versions of Pillow to ensure reproducible builds: Pillow==10.3.0

Dependencies are isolated inside .venv so the user’s global Python installation is never modified.
