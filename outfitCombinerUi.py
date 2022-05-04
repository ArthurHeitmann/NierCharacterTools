from email.policy import default
import bpy
from .utils import *
from . import outfitTypes

def getCharacterOutfitsAsEnum(scene, context):
	character = getCharacterName()
	if not character:
		return []
	enum = []
	for outfit in outfitTypes.outfits[character]:
		enum.append((outfit, outfit, ""))
	return enum

class OutfitCombinerOptions(bpy.types.PropertyGroup):
	outfitSourceFilter: bpy.props.EnumProperty(items=getCharacterOutfitsAsEnum, name="Source Filter")
	outfitTargetFilter: bpy.props.EnumProperty(items=getCharacterOutfitsAsEnum, name="Target Filter")
	source: bpy.props.StringProperty(name="Source")
	target: bpy.props.StringProperty(name="Target")

class OutfitCombinerUi(bpy.types.Panel):
	bl_label = "Outfit Combiner"
	bl_idname = "B2N_PT_OUTFIT_COMBINER"
	bl_parent_id = "B2N_PT_NIER_CHRACTER_TOOLS"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout
		options = context.scene.outfitCombinerOptions

		# source
		row = layout.row()
		row.prop(options, "outfitSourceFilter", text="Filter")
		layout.label(text="Source:")
		character = getCharacterName()
		if character:
			sources = outfitTypes.outfitParts[character]
			box = layout.box()
			for source in sources:
				if options.outfitSourceFilter and source not in outfitTypes.outfitToParts[character][options.outfitSourceFilter]:
					continue
				row = box.row()
				row.alert = source == options.source
				row.label(text=source)
				row.operator("nct.select_outfit_source", text="", icon="RESTRICT_SELECT_OFF").source = source

		else:
			layout.label(text="No supported character in scene")
		
		# target
		row = layout.row()
		row.prop(options, "outfitTargetFilter", text="Filter")
		layout.label(text="Target:")
		if character:
			targets = outfitTypes.outfitParts[character]
			box = layout.box()
			for target in targets:
				if options.outfitTargetFilter and target not in outfitTypes.outfitToParts[character][options.outfitTargetFilter]:
					continue
				row = box.row()
				row.alert = target == options.target
				row.label(text=target)
				row.operator("nct.select_outfit_target", text="", icon="RESTRICT_SELECT_OFF").target = target
		else:
			layout.label(text="No supported character in scene")

		# actions
		row = layout.row()
		row.operator("nct.move_outfit_parts", text="Move")
		row.operator("nct.swap_outfit_parts", text="Swap")
		row.operator("nct.swap_outfit_parts", text="Override")

class SelectOutfitSource(bpy.types.Operator):
	bl_idname = "nct.select_outfit_source"
	bl_label = "Select Outfit Source"
	bl_options = {"UNDO"}

	source: bpy.props.StringProperty(name="Source")
	
	def execute(self, context):
		options = context.scene.outfitCombinerOptions
		options.source = self.source
		return {"FINISHED"}

class SelectOutfitTarget(bpy.types.Operator):
	bl_idname = "nct.select_outfit_target"
	bl_label = "Select Outfit Target"
	bl_options = {"UNDO"}

	target: bpy.props.StringProperty(name="Target")
	
	def execute(self, context):
		options = context.scene.outfitCombinerOptions
		options.target = self.target
		return {"FINISHED"}

class MoveOutfitParts(bpy.types.Operator):
	bl_idname = "nct.move_outfit_parts"
	bl_label = "Move Outfit Parts"
	bl_options = {"UNDO"}
	
	def execute(self, context):
		options = context.scene.outfitCombinerOptions
		character = getCharacterName()
		if not character:
			return {"FINISHED"}

		sourceObjects = [obj for obj in getWmbColl().objects if getObjName(obj) == options.source]
		firstTargetObj = [obj for obj in getWmbColl().objects if getObjName(obj) == options.target][-1]
		targetName = firstTargetObj.name
		targetVisibility = firstTargetObj.hide_get()

		for sourceObject in sourceObjects:
			sourceObject.name = targetName
			sourceObject.parent = firstTargetObj.parent
			sourceObject.matrix_parent_inverse  = firstTargetObj.matrix_world.inverted()
			sourceObject.hide_set(targetVisibility)
			sourceObject.hide_viewport = targetVisibility
			sourceObject.hide_render = targetVisibility
		
		return {"FINISHED"}

class SwapOutfitParts(bpy.types.Operator):
	bl_idname = "nct.swap_outfit_parts"
	bl_label = "Swap Outfit Parts"
	bl_options = {"UNDO"}
	
	def execute(self, context):
		options = context.scene.outfitCombinerOptions
		character = getCharacterName()
		if not character:
			return {"FINISHED"}

		sourceObjects = [obj for obj in getWmbColl().objects if getObjName(obj) == options.source]
		targetObjects = [obj for obj in getWmbColl().objects if getObjName(obj) == options.target]
		firstSourceObj = [obj for obj in getWmbColl().objects if getObjName(obj) == options.source][-1]
		firstTargetObj = [obj for obj in getWmbColl().objects if getObjName(obj) == options.target][-1]
		sourceName = firstSourceObj.name
		targetName = firstTargetObj.name
		sourceVisibility = firstSourceObj.hide_get()
		targetVisibility = firstTargetObj.hide_get()
		sourceParent = firstSourceObj.parent
		targetParent = firstTargetObj.parent
		sourceMatrixWorldInv = firstSourceObj.matrix_world.inverted()
		targetMatrixWorldInv = firstTargetObj.matrix_world.inverted()

		for sourceObject in sourceObjects:
			sourceObject.name = targetName
			sourceObject.parent = targetParent
			sourceObject.matrix_parent_inverse  = targetMatrixWorldInv
			sourceObject.hide_set(targetVisibility)
			sourceObject.hide_viewport = targetVisibility
			sourceObject.hide_render = targetVisibility
		for targetObject in targetObjects:
			targetObject.name = sourceName
			targetObject.parent = sourceParent
			targetObject.matrix_parent_inverse  = sourceMatrixWorldInv
			targetObject.hide_set(sourceVisibility)
			targetObject.hide_viewport = sourceVisibility
			targetObject.hide_render = sourceVisibility
		
		return {"FINISHED"}

class OverrideOutfitParts(bpy.types.Operator):
	bl_idname = "nct.override_outfit_parts"
	bl_label = "Override Outfit Parts"
	bl_options = {"UNDO"}
	
	def execute(self, context):
		options = context.scene.outfitCombinerOptions
		character = getCharacterName()
		if not character:
			return {"FINISHED"}
		
		sourceObjects = [obj for obj in getWmbColl().objects if getObjName(obj) == options.source]
		targetObjects = [obj for obj in getWmbColl().objects if getObjName(obj) == options.target]
		firstTargetObj = [obj for obj in getWmbColl().objects if getObjName(obj) == options.target][-1]
		targetName = firstTargetObj.name
		targetVisibility = firstTargetObj.hide_get()

		for sourceObject in sourceObjects:
			sourceObject.name = targetName
			sourceObject.parent = firstTargetObj.parent
			sourceObject.matrix_parent_inverse  = firstTargetObj.matrix_world.inverted()
			sourceObject.hide_set(targetVisibility)
			sourceObject.hide_viewport = targetVisibility
			sourceObject.hide_render = targetVisibility
		for targetObject in targetObjects:
			bpy.data.objects.remove(targetObject)
		
		return {"FINISHED"}

def register():
	bpy.utils.register_class(SelectOutfitSource)
	bpy.utils.register_class(SelectOutfitTarget)
	bpy.utils.register_class(MoveOutfitParts)
	bpy.utils.register_class(SwapOutfitParts)
	bpy.utils.register_class(OverrideOutfitParts)
	bpy.utils.register_class(OutfitCombinerOptions)
	bpy.utils.register_class(OutfitCombinerUi)

	bpy.types.Scene.outfitCombinerOptions = bpy.props.PointerProperty(type=OutfitCombinerOptions)

def unregister():
	bpy.utils.unregister_class(SelectOutfitSource)
	bpy.utils.unregister_class(SelectOutfitTarget)
	bpy.utils.unregister_class(MoveOutfitParts)
	bpy.utils.unregister_class(SwapOutfitParts)
	bpy.utils.unregister_class(OverrideOutfitParts)
	bpy.utils.unregister_class(OutfitCombinerOptions)
	bpy.utils.unregister_class(OutfitCombinerUi)

	del bpy.types.Scene.outfitCombinerOptions
