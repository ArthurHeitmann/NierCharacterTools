from . import mainUi

bl_info = {
    "name" : "NierCharacterTools",
    "author" : "RaiderB",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

def register():
    mainUi.register()

def unregister():
    mainUi.unregister()
