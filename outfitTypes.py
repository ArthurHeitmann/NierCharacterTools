
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
    ],
    "9S": [
        "Body",
        "DLC_Body",
        "DLC_Leg",
        "DLC_Pants",
        "DLC_mesh_es0200",
        "DLC_mesh_es0201",
        "DLC_mesh_es0202",
        "DLC_mesh_es0206",
        "DLC_mesh_pl0200",
        "Eyelash",
        "Eyelash_serious",
        "Eyemask",
        "Leg",
        "Pants",
        "facial_normal",
        "facial_serious",
        "mesh_es0200",
        "mesh_es0201",
        "mesh_es0202",
        "mesh_es0206",
        "mesh_pl0200",
    ],
    "A2": [
        "Body",
        "Cloth",
        "DLC_Body",
        "DLC_Cloth",
        "Hair",
        "facial_normal",
        "facial_serious",
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
    ],
    "9S": [
        "All",
        "Normal",
        "Self Destruct",
        "Normal Broken Left",   # es0200
        "Normal Broken Right",  # es0206
        "Normal Broken Holes",  # es0201
        "Normal Broken 2B Hand",# es0202
        "DLC",                  # pl0200
        "DLC Broken Left",      # es0200
        "DLC Broken Right",     # es0206
        "DLC Broken Holes",     # es0201
        "DLC Broken 2B Hand",   # es0202
    ],
    "A2": [
        "All",
        "Normal",
        "Beserk",
        "DLC"
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
    },
    "9S": {
        "All": ["Body", "DLC_Body", "DLC_Leg", "DLC_Pants", "DLC_mesh_es0200", "DLC_mesh_es0201", "DLC_mesh_es0202", "DLC_mesh_es0206", "DLC_mesh_pl0200", "Eyelash", "Eyelash_serious", "Eyemask", "Leg", "Pants", "facial_normal", "facial_serious", "mesh_es0200", "mesh_es0201", "mesh_es0202", "mesh_es0206", "mesh_pl0200"],
        "Normal": ["Body", "Eyelash", "Eyelash_serious", "Eyemask", "Leg", "Pants", "facial_normal", "facial_serious", "mesh_pl0200"],
        "Self Destruct": ["Body", "Eyelash", "Eyelash_serious", "Eyemask", "Leg", "facial_normal", "facial_serious", "mesh_pl0200"],
        "Normal Broken Left": ["Body", "Eyelash", "Eyelash_serious", "Eyemask", "Leg", "facial_normal", "facial_serious", "mesh_es0200"],
        "Normal Broken Right": ["Body", "Eyelash", "Eyelash_serious", "Eyemask", "Leg", "Pants", "facial_normal", "facial_serious", "mesh_es0206"],
        "Normal Broken Holes": ["Body", "Eyelash", "Eyelash_serious", "Eyemask", "Leg", "Pants", "facial_normal", "facial_serious", "mesh_es0201"],
        "Normal Broken 2B Hand": ["Body", "Eyelash", "Eyelash_serious", "Eyemask", "Leg", "Pants", "facial_normal", "facial_serious", "mesh_es0202"],
        "DLC": ["DLC_Body", "DLC_Leg", "DLC_Pants", "DLC_mesh_pl0200", "Eyelash", "Eyelash_serious", "Eyemask", "facial_normal", "facial_serious"],
        "DLC Broken Left": ["DLC_Body", "DLC_Leg", "DLC_mesh_es0200", "Eyelash", "Eyelash_serious", "Eyemask", "facial_normal", "facial_serious"],
        "DLC Broken Right": ["DLC_Body", "DLC_Leg", "DLC_Pants", "DLC_mesh_es0206", "Eyelash", "Eyelash_serious", "Eyemask", "facial_normal", "facial_serious"],
        "DLC Broken Holes": ["DLC_Body", "DLC_Leg", "DLC_Pants", "DLC_mesh_es0201", "Eyelash", "Eyelash_serious", "Eyemask", "facial_normal", "facial_serious"],
        "DLC Broken 2B Hand": ["DLC_Body", "DLC_Leg", "DLC_Pants", "DLC_mesh_es0202", "Eyelash", "Eyelash_serious", "Eyemask", "facial_normal", "facial_serious"],
    },
    "A2": {
        "All": ["Body", "Cloth", "DLC_Body", "DLC_Cloth", "Hair", "facial_normal", "facial_serious"],
        "Normal": ["Body", "Cloth", "Hair", "facial_normal", "facial_serious"],
        "Beserk": ["Body", "Hair", "facial_normal", "facial_serious"],
        "DLC": ["DLC_Body", "DLC_Cloth", "Hair", "facial_normal", "facial_serious"],
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
