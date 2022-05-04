from ctypes import util
import bpy
import re
from . import outfitTypes
from .utils import *

class OutfitVisibilityPanel(bpy.types.Panel):
	bl_label = "Outfit Visibility"
	bl_idname = "B2N_PT_NIER_OUTFIT_VISIBILITY"
	bl_parent_id = "B2N_PT_NIER_CHRACTER_TOOLS"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	def draw(self, context):
		layout = self.layout

class IndividualOutfitPartsVisibilityPanel(bpy.types.Panel):
	bl_label = "Individual Outfit Parts Visibility"
	bl_idname = "B2N_PT_NIER_INDIVIDUAL_OUTFIT_PARTS_VISIBILITY"
	bl_parent_id = "B2N_PT_NIER_OUTFIT_VISIBILITY"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_options = {'DEFAULT_CLOSED'}
	
	def draw(self, context):
		layout = self.layout

		character = getCharacterName()

		if character:
			for part in outfitTypes.outfitParts[character]:
				row = layout.row(align=True)
				row.label(text=part)
				row.operator("nct.show_outfit_part", text="", icon="HIDE_OFF").part = part
				row.operator("nct.hide_outfit_part", text="", icon="HIDE_ON").part = part
		else:
			layout.label(text="No supported character in scene")

class FullOutfitVisibilityPanel(bpy.types.Panel):
	bl_label = "Full Outfit Visibility"
	bl_idname = "B2N_PT_NIER_FULL_OUTFIT_VISIBILITY"
	bl_parent_id = "B2N_PT_NIER_OUTFIT_VISIBILITY"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	def draw(self, context):
		layout = self.layout

		character = getCharacterName()

		if character:
			for outfit in outfitTypes.outfits[character]:
				row = layout.row(align=True)
				row.label(text=outfit)
				row.operator("nct.focus_outfit", text="", icon="HIDE_OFF").outfit = outfit
		else:
			layout.label(text="No supported character in scene")

def setObjectsVisibility(searchName: str, newVisibility: bool):
	newVisibility = not newVisibility
	for obj in getWmbColl().objects:
		if obj.type != "MESH":
			continue
		trueName = getObjName(obj)
		if not trueName:
			continue
		if trueName == searchName:
			obj.hide_viewport = newVisibility
			obj.hide_render = newVisibility
			obj.hide_set(newVisibility)

class ShowOutfitPart(bpy.types.Operator):
	bl_idname = "nct.show_outfit_part"
	bl_label = "Show Outfit Part"
	bl_options = {'REGISTER', 'UNDO'}
	
	part: bpy.props.StringProperty(name="Part")
	
	def execute(self, context):
		setObjectsVisibility(self.part, True)
		return {'FINISHED'}

class HideOutfitPart(bpy.types.Operator):
	bl_idname = "nct.hide_outfit_part"
	bl_label = "Hide Outfit Part"
	bl_options = {'REGISTER', 'UNDO'}
	
	part: bpy.props.StringProperty(name="Part")
	
	def execute(self, context):
		setObjectsVisibility(self.part, False)
		return {'FINISHED'}

class FocusOutfit(bpy.types.Operator):
	bl_idname = "nct.focus_outfit"
	bl_label = "Focus Outfit"
	bl_options = {'REGISTER', 'UNDO'}
	
	outfit: bpy.props.StringProperty(name="Outfit")
	
	def execute(self, context):
		character = getCharacterName()
		if not character:
			self.report({'ERROR'}, "No supported character in scene")
			return {'CANCELLED'}
		
		showParts = outfitTypes.outfitToParts[character][self.outfit]
		hideParts = [part for part in outfitTypes.outfitParts[character] if part not in showParts]
		for part in hideParts:
			setObjectsVisibility(part, False)
		for part in showParts:
			setObjectsVisibility(part, True)
		
		return {'FINISHED'}

def register():
	# Operators
	bpy.utils.register_class(ShowOutfitPart)
	bpy.utils.register_class(HideOutfitPart)
	bpy.utils.register_class(FocusOutfit)
	# UI Panels
	bpy.utils.register_class(OutfitVisibilityPanel)
	bpy.utils.register_class(IndividualOutfitPartsVisibilityPanel)
	bpy.utils.register_class(FullOutfitVisibilityPanel)

def unregister():
	# Operators
	bpy.utils.unregister_class(ShowOutfitPart)
	bpy.utils.unregister_class(HideOutfitPart)
	bpy.utils.unregister_class(FocusOutfit)
	# UI Panels
	bpy.utils.unregister_class(OutfitVisibilityPanel)
	bpy.utils.unregister_class(IndividualOutfitPartsVisibilityPanel)
	bpy.utils.unregister_class(FullOutfitVisibilityPanel)

