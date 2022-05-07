import bpy
from bpy_extras.io_utils import ImportHelper
import os
from .utils import *

class ImportOtherModel(bpy.types.Operator, ImportHelper):
	bl_idname = "nct.import_other_model"
	bl_label = "Import Other Model"
	bl_options = {"UNDO"}
	
	filename_ext = ".dtt"
	filter_glob: bpy.props.StringProperty(default="*.dtt", options={"HIDDEN"})
	
	def execute(self, context):
		filepath = self.filepath

		# only allow importing same model
		selectedFile = os.path.basename(filepath).split(".")[0]
		currentModelName = getWmbColl().name
		if currentModelName != selectedFile:
			self.report({'ERROR'}, f"Selected model does not match current model ({currentModelName} != {selectedFile})")
			return {'CANCELLED'}

		# prepare original, so that it doesn't get overriden
		mainColl = getWmbColl()
		origName = mainColl.name
		mainColl.name = "tmpColl"
		allCollections = list(bpy.data.collections)
		for obj in mainColl.objects:
			obj.name += "_tmp"

		# import new model
		bpy.ops.import_scene.dtt_data(filepath=filepath, reset_blend=False)
		newColl = [coll for coll in bpy.data.collections if coll not in allCollections][-1]
		newColl.name = f"{os.path.basename(filepath)}_EXTERNAL_{context.scene.otherModelsCollectionIndex}"
		getWmbParentColl().children.unlink(newColl)
		context.scene.collection.children.link(newColl)
		context.scene.otherModelsCollectionIndex += 1
		context.scene.otherModelsCollectionNames.add().str = newColl.name

		# restore original
		mainColl.name = origName
		for obj in mainColl.objects:
			obj.name = obj.name.replace("_tmp", "")

		return {"FINISHED"}

class DeleteOtherModels(bpy.types.Operator):
	bl_idname = "nct.delete_other_models"
	bl_label = "Delete Other Models"
	bl_options = {"UNDO"}

	def execute(self, context):
		removedObjs = 0
		removedColls = 0
		removedMaterials = 0
		removedImages = 0
		remainingMaterials = []
		
		for collName in context.scene.otherModelsCollectionNames:
			coll = bpy.data.collections[collName.str]
			for obj in coll.objects:
				objData = obj.data
				objType = obj.type
				bpy.data.objects.remove(obj)
				if objType == "MESH":
					remainingMaterials.extend(objData.materials)
					bpy.data.meshes.remove(objData)
				if objType == "ARMATURE":
					bpy.data.armatures.remove(objData)
				removedObjs += 1
			bpy.data.collections.remove(coll)
			removedColls += 1

		remainingMaterials = list(set(remainingMaterials))
		for material in remainingMaterials:
			if material.users == 0:
				bpy.data.materials.remove(material)
				removedMaterials += 1
		
		for img in bpy.data.images:
			if img.users == 0:
				bpy.data.images.remove(img)
				removedImages += 1
		
		print(f"Removed {removedObjs} objects, {removedColls} collections, {removedMaterials} materials, {removedImages} images")

		return {"FINISHED"}

def getAllModelCollectionsAsEnum(scene, context):
	enums = [(getWmbColl().name, "Main", "")]
	for coll in context.scene.otherModelsCollectionNames:
		enums.append((coll.str, coll.str, ""))
	return enums

def checkIfCollectionStillExists(_, __):
	i = 0
	while i < len(bpy.context.scene.otherModelsCollectionNames):
		coll = bpy.context.scene.otherModelsCollectionNames[i].str
		if coll not in bpy.data.collections:
			bpy.context.scene.otherModelsCollectionNames.remove(i)
			outfitOptions = bpy.context.scene.outfitCombinerOptions
			if not outfitOptions.sourceCollection or outfitOptions.sourceCollection == coll:
				outfitOptions.sourceCollection = getWmbColl().name
		else:
			i += 1

class StrPropWrapper(bpy.types.PropertyGroup):
	str: bpy.props.StringProperty(name="String")

def register():
	bpy.utils.register_class(ImportOtherModel)
	bpy.utils.register_class(DeleteOtherModels)
	bpy.utils.register_class(StrPropWrapper)

	bpy.types.Scene.otherModelsCollectionNames = bpy.props.CollectionProperty(type=StrPropWrapper)
	bpy.types.Scene.otherModelsCollectionIndex = bpy.props.IntProperty(default=0)

	bpy.app.handlers.depsgraph_update_pre.append(checkIfCollectionStillExists)

def unregister():
	bpy.utils.unregister_class(ImportOtherModel)
	bpy.utils.unregister_class(DeleteOtherModels)
	bpy.utils.unregister_class(StrPropWrapper)

	del bpy.types.Scene.otherModelsCollectionNames
	del bpy.types.Scene.otherModelsCollectionIndex

	if checkIfCollectionStillExists in bpy.app.handlers.depsgraph_update_pre:
		bpy.app.handlers.depsgraph_update_pre.remove(checkIfCollectionStillExists)
