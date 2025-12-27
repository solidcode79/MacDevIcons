import plistlib

PRIVACY_KEEP = {
    "NSAppleEventsUsageDescription",
}

def make_ext_entry(ext: str, icon_name: str):
    return {
        "CFBundleTypeName": icon_name,
        "CFBundleTypeExtensions": [ext],
        "CFBundleTypeRole":"Editor",
        "CFBundleTypeIconFile": icon_name,       
        "LSHandlerRank": "Owner"
    }

def make_uti_entry(uti: str, icon_name: str):
    return {
        "CFBundleTypeName": icon_name,
        "CFBundleTypeUTIs": [uti],
        "CFBundleTypeRole": "Editor",
        "CFBundleTypeIconFile": icon_name,
        "LSHandlerRank": "Owner"
    }
    
def update_plist(APP_PATH, ext_mapping, uti_mapping):
    info_plist = APP_PATH / "Contents" / "Info.plist"
    with open(info_plist, 'rb') as f:
        data = plistlib.load(f)

    doc_types = data.get("CFBundleDocumentTypes")
    if doc_types is None:
        doc_types = []
        data["CFBundleDocumentTypes"] = doc_types
    
    for ext, icon_name in ext_mapping.items():
        doc_types.append(make_ext_entry(ext, icon_name))

    for uti, icon_name in uti_mapping.items():
        doc_types.append(make_uti_entry(uti, icon_name))        
    
    removed_keys = []
    for key in list(data.keys()):
        if key.startswith("NS") and key.endswith("UsageDescription"):
            if key not in PRIVACY_KEEP:
                removed_keys.append(key)
                data.pop(key)
                
    print("Removed keys:", removed_keys)

    with open(info_plist, "wb") as f:
        plistlib.dump(data, f, sort_keys=False)
