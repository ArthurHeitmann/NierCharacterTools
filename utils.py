import bpy
import re

def getWmbColl():
	if "WMB" in bpy.data.collections:
		return bpy.data.collections["WMB"].children[0]
	else:
		for col in bpy.data.collections:
			if len(col.name) == 6:
				return col
		return bpy.data.collections[0]

def getWmbParentColl():
	if "WMB" in bpy.data.collections:
		return bpy.data.collections["WMB"]
	else:
		return bpy.context.scene.collection

def getCharacterName():
	if "pl000d" in bpy.data.collections or "pl0000" in bpy.data.collections:
		return "2B"
	if "pl020d" in bpy.data.collections or "pl0200" in bpy.data.collections:
		return "9S"
	if "pl010d" in bpy.data.collections or "pl0100" in bpy.data.collections:
		return "A2"
	else:
		return None

def getObjName(obj):
	name = re.match(r"^\d+-(.+)-\d+(\.\d{3,})?$", obj.name)
	return name.group(1) if name else None
