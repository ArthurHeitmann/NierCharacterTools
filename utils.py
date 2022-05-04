import bpy
import re

def getWmbColl():
	if "WMB" in bpy.data.collections:
		return bpy.data.collections["WMB"].children[0]
	else:
		return bpy.data.collections[0]

def getCharacterName():
	if "pl000d" in bpy.data.collections or "pl0000" in bpy.data.collections:
		return "2B"
	else:
		return None

def getObjName(obj):
	name = re.match(r"^\d+-(.+)-\d+(\.\d{3,})?$", obj.name)
	return name.group(1) if name else None
