# MacDevIcons
Beautiful developer file-type icons for macOS Finder — powered by https://devicon.dev

# Motivation
On a fresh macOS install, developer file icons don’t just look bad — they don’t exist. Unless you install a heavyweight IDE, macOS happily assigns the same mystery-generic-blank-document icon to everything: JavaScript, TypeScript, JSON, Python, Go, Rust, C++, Markdown et al.

For developers who prefer lightweight editors like Zed, Neovim, Helix, or anything that isn’t a 2-GB IDE, the result is a Finder window where every file looks identical — a digital version of guessing which identical twin is which. MacDevIcons fixes this.

It gives you clean, dev-friendly icons for your file types without requiring a giant IDE ... Just run the app, open files through it, and Finder immediately becomes visually meaningful again.

![Screenshot of my test folder](./Screenshot.png)

PS1: You are never going to see all these file types together in one folder unless you are testing icons.

PS2: The docker icons looks so good that I’m considering renaming every Dockerfile to something.docker just to admire that little ship.

## How It Works
MacDevIcons repackages a tiny Automator-based app that claims ownership of selected file types through its Info.plist. When you open a file using the MacDevIcons app, macOS associates that extension with the app’s custom icons, making Finder display the correct DevIcon artwork. The app then forwards the file path to your chosen editor (currently Zed, later configurable). 

A Python build script regenerates icons, updates plist claims, and bundles everything so the app behaves like a lightweight, system-level file-type decorator plus launcher.

## Usage
- Modify the /config/config.json
- Run build.sh
- Make 'MacDevIcons' default app to open the files types with

## Supported File Types
- The supported icons are at /vendor/devicon/icons
- Select the icon and modify the config.json @ /config/config.json

## Roadmap
- Can configure the editor, right now Zed
- Make it slimmer/faster ?

## Acknowledgements
https://github.com/devicons/devicon