
outfitParts = {
    "2B": [
        "Armor_Body",
        "Armor_Head",
        "Body",
        "Broken",
        "DLC_Body",
        "DLC_Broken",
        "DLC_Skirt",
        "Eyelash",
        "Eyemask",
        "facial_normal",
        "facial_serious",
        "Feather",
        "Hair",
        "Skirt",
    ]
}

outfits = {
    "2B": [
        "All",
        "Normal",
        "Normal Broken",
        "Base",
        "Armor",
        "DLC",
        "DLC Broken",
    ]
}

outfitToParts = {
    "2B": {
        "All": ["Armor_Body", "Armor_Head", "Body", "Broken", "DLC_Body", "DLC_Broken", "DLC_Skirt", "Eyelash", "Eyemask", "facial_normal", "facial_serious", "Feather", "Hair", "Skirt"],
        "Normal": ["Body", "Eyelash", "Eyemask", "facial_normal", "facial_serious", "Feather", "Hair", "Skirt"],
        "Normal Broken": ["Broken", "Body", "Eyelash", "Eyemask", "facial_normal", "facial_serious", "Feather", "Hair"],
        "Base": ["Body", "Eyelash", "Eyemask", "facial_normal", "facial_serious", "Hair"],
        "Armor": ["Armor_Body", "Armor_Head"],
        "DLC": ["DLC_Body", "DLC_Skirt", "Eyelash", "facial_normal", "facial_serious", "Hair"],
        "DLC Broken": ["DLC_Body", "DLC_Broken", "Eyelash", "facial_normal", "facial_serious", "Hair"],
    }
}

outfitPartsEnum = {
    character: [
        (part, part, "")
        for part in charParts
    ]
    for character, charParts in outfitParts.items()
}

outfitsEnum = {
    character: [
        (outfit, outfit, "")
        for outfit in charOutfits
    ]
    for character, charOutfits in outfits.items()
}
