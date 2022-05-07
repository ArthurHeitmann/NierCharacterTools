from email.policy import default
from enum import Enum
import bpy
from .otherModelsManager import getAllModelCollectionsAsEnum
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
	sourceCollection: bpy.props.EnumProperty(items=getAllModelCollectionsAsEnum)
	source: bpy.props.StringProperty(name="Source")
	target: bpy.props.StringProperty(name="Target")
	keepOriginals: bpy.props.BoolProperty(name="Keep Originals", default=False)

class OutfitCombinerUi(bpy.types.Panel):
	bl_label = "Outfit Combiner"
	bl_idname = "B2N_PT_OUTFIT_COMBINER"
	bl_parent_id = "B2N_PT_NIER_CHRACTER_TOOLS"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout
		options = context.scene.outfitCombinerOptions

		sourceCollections = getAllModelCollectionsAsEnum(None, context)
		layout.operator("nct.import_other_model")
		if len(sourceCollections) > 1:
			layout.operator("nct.delete_other_models")
		
		# source
		layout.label(text="Source:")
		if len(sourceCollections) > 1:
			row = layout.row()
			row.prop(options, "sourceCollection", text="Collection")
		row = layout.row()
		row.prop(options, "outfitSourceFilter", text="Filter")
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
		layout.label(text="Target:")
		row = layout.row()
		row.prop(options, "outfitTargetFilter", text="Filter")
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
		row = layout.row(align=True)
		row.operator("nct.move_outfit_parts", text="Move").srcCollName = options.sourceCollection
		row.operator("nct.swap_outfit_parts", text="Swap").srcCollName = options.sourceCollection
		row.operator("nct.override_outfit_parts", text="Override").srcCollName = options.sourceCollection
		layout.prop(options, "keepOriginals")

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

def moveObjToColl(obj, newColl):
	for coll in obj.users_collection:
		coll.objects.unlink(obj)
	newColl.objects.link(obj)

class CombineOperationType(Enum):
	MOVE = "MOVE"
	SWAP = "SWAP"
	OVERRIDE = "OVERRIDE"

def duplicateObj(obj, dupData = True):
	newObj = obj.copy()
	if dupData:
		newObj.data = obj.data.copy()
	else:
		newObj.data = bpy.data.meshes.new(name=obj.data.name)
	obj.users_collection[0].objects.link(newObj)
	return newObj

def duplicateObjAsPreset(obj):
	newObj = duplicateObj(obj, False)
	newObj.name = obj.name + "_preset"
	newObj.data.materials.clear()
	return newObj

def newObjFromPreset(oldObj, presetObj):
	newObj = duplicateObj(presetObj)
	cxt = bpy.context.copy()
	cxt["selected_editable_objects"] = [newObj, oldObj]
	cxt["active_object"] = newObj
	bpy.ops.object.join(cxt)
	bpy.data.objects.remove(presetObj)
	return newObj

def combineOutfits(context, srcCollName: str, operationType: CombineOperationType):
	options = context.scene.outfitCombinerOptions
	character = getCharacterName()
	if not character:
		return {"FINISHED"}

	sourceObjects = [obj for obj in bpy.data.collections[srcCollName].objects if getObjName(obj) == options.source]
	targetObjects = [obj for obj in getWmbColl().objects if getObjName(obj) == options.target]
	lastSourceObj = [obj for obj in bpy.data.collections[srcCollName].objects if getObjName(obj) == options.source][-1]
	lastTargetObj = [obj for obj in getWmbColl().objects if getObjName(obj) == options.target][-1]
	presetSourceObj = duplicateObjAsPreset(lastSourceObj)
	presetTargetObj = duplicateObjAsPreset(lastTargetObj)
	sourceName = lastSourceObj.name
	targetName = lastTargetObj.name

	if (operationType == CombineOperationType.MOVE or operationType == CombineOperationType.OVERRIDE) and not options.keepOriginals:
		# keep 1 placeholder object with 0 size triangle
		placeholderObj = duplicateObj(lastSourceObj)
		# ensure object is visible
		hide, hideViewport = placeholderObj.hide_get(), placeholderObj.hide_viewport
		placeholderObj.hide_set(False)
		placeholderObj.hide_viewport = False
		context.view_layer.objects.active = placeholderObj
		# delete all vertices
		bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.select_all(action="SELECT")
		bpy.ops.mesh.delete(type="VERT")
		bpy.ops.object.editmode_toggle()
		# reset visibility
		placeholderObj.hide_set(hide)
		placeholderObj.hide_viewport = hideViewport
		# make 0 size triangle
		placeholderObj.data.from_pydata([(0, 0, 0), (0, 0, 0), (0, 0.001, 0), ], [], [(0, 1, 2)])

	# move source to target
	for sourceObject in sourceObjects:
		if options.keepOriginals:
			sourceObject = duplicateObj(sourceObject)
		newObj = newObjFromPreset(sourceObject, duplicateObj(presetTargetObj))
		newObj.name = targetName
	# move target to source
	if operationType == CombineOperationType.SWAP:
		for targetObject in targetObjects:
			if options.keepOriginals:
				targetObject = duplicateObj(targetObject)
			newObj = newObjFromPreset(targetObject, duplicateObj(presetSourceObj))
			newObj.name = sourceName
	# remove original targets
	if operationType == CombineOperationType.OVERRIDE:
		for targetObject in targetObjects:
			bpy.data.objects.remove(targetObject)
	
	# remove preset objects
	bpy.data.objects.remove(presetSourceObj, do_unlink=True)
	bpy.data.objects.remove(presetTargetObj, do_unlink=True)
			
	bpy.ops.b2n.recalculateobjectindices()
	
	return {"FINISHED"}

class MoveOutfitParts(bpy.types.Operator):
	bl_idname = "nct.move_outfit_parts"
	bl_label = "Move Outfit Parts"
	bl_options = {"UNDO"}

	srcCollName: bpy.props.StringProperty()
	
	def execute(self, context):
		return combineOutfits(context, self.srcCollName, CombineOperationType.MOVE)

class SwapOutfitParts(bpy.types.Operator):
	bl_idname = "nct.swap_outfit_parts"
	bl_label = "Swap Outfit Parts"
	bl_options = {"UNDO"}

	srcCollName: bpy.props.StringProperty()
	
	def execute(self, context):
		return combineOutfits(context, self.srcCollName, CombineOperationType.SWAP)

class OverrideOutfitParts(bpy.types.Operator):
	bl_idname = "nct.override_outfit_parts"
	bl_label = "Override Outfit Parts"
	bl_options = {"UNDO"}

	srcCollName: bpy.props.StringProperty()
	
	def execute(self, context):
		return combineOutfits(context, self.srcCollName, CombineOperationType.OVERRIDE)

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
