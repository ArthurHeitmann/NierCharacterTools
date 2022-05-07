import bpy

class FileCleanupOptions(bpy.types.PropertyGroup):
	cleanupObjects: bpy.props.BoolProperty(name="Cleanup Objects", default=True)
	cleanupMeshes: bpy.props.BoolProperty(name="Cleanup Meshs", default=True)
	cleanupMaterials: bpy.props.BoolProperty(name="Cleanup Materials", default=True)
	cleanupTextures: bpy.props.BoolProperty(name="Cleanup Images", default=True)

class CleanupBlendFile(bpy.types.Operator):
	bl_idname = "nct.cleanup_blend_file"
	bl_label = "Cleanup Blend File"
	bl_options = {"UNDO"}

	cleanupObjects: bpy.props.BoolProperty()
	cleanupMeshes: bpy.props.BoolProperty()
	cleanupMaterials: bpy.props.BoolProperty()
	cleanupTextures: bpy.props.BoolProperty()

	def execute(self, context):
		objectsToDelete = []
		meshesToDelete = []
		armaturesToDelete = []
		materialsToMaybeDelete = []
		objectsDeleted = 0
		meshesDeleted = 0
		armaturesDeleted = 0
		materialsDeleted = 0
		texturesDeleted = 0

		for obj in bpy.data.objects:
			if obj.users == 0 or len(obj.users_collection) == 0:
				if self.cleanupObjects:
					objectsToDelete.append(obj)

				if obj.type == "MESH":
					if self.cleanupMeshes:
						meshesToDelete.append(obj.data)
					if self.cleanupMaterials:
						materialsToMaybeDelete.extend(obj.data.materials)
				if obj.type == "ARMATURE":
					if self.cleanupMeshes:
						armaturesToDelete.append(obj.data)
		for mesh in bpy.data.meshes:
			if mesh.users == 0 and self.cleanupMeshes:
				meshesToDelete.append(mesh)
		for armature in bpy.data.armatures:
			if armature.users == 0 and self.cleanupMeshes:
				armaturesToDelete.append(armature)
		
		for obj in objectsToDelete:
			bpy.data.objects.remove(obj)
			objectsDeleted += 1
		for mesh in meshesToDelete:
			bpy.data.meshes.remove(mesh)
			meshesDeleted += 1
		for armature in armaturesToDelete:
			bpy.data.armatures.remove(armature)
			armaturesDeleted += 1
		if self.cleanupMaterials:
			for material in materialsToMaybeDelete:
				if material.users == 0:
					bpy.data.materials.remove(material)
					materialsDeleted += 1
			for material in bpy.data.materials:
				if material.users == 0:
					bpy.data.materials.remove(material)
					materialsDeleted += 1
		if self.cleanupTextures:
			for img in bpy.data.images:
				if img.users == 0:
					bpy.data.images.remove(img)
					texturesDeleted += 1
		
		statusMsg = []
		if objectsDeleted > 0:
			statusMsg.append(f"{objectsDeleted} objects deleted")
		if meshesDeleted > 0:
			statusMsg.append(f"{meshesDeleted} meshes deleted")
		if armaturesDeleted > 0:
			statusMsg.append(f"{armaturesDeleted} armatures deleted")
		if materialsDeleted > 0:
			statusMsg.append(f"{materialsDeleted} materials deleted")
		if texturesDeleted > 0:
			statusMsg.append(f"{texturesDeleted} textures deleted")
		if len(statusMsg) == 0:
			statusMsg.append("Nothing deleted")
		statusMsg = ", ".join(statusMsg)
		self.report({"INFO"}, statusMsg)

		return {"FINISHED"}
		

class FileCleanupPanel(bpy.types.Panel):
	bl_idname = "nct.file_cleanup_panel"
	bl_label = "File Cleanup"
	bl_parent_id = "B2N_PT_NIER_CHRACTER_TOOLS"
	bl_space_type = "VIEW_3D"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"

	def draw(self, context):
		layout = self.layout
		options = context.scene.fileCleanupOptions

		layout.label(text="Purge Options:")
		
		row = layout.row(align=True)
		row.prop(options, "cleanupObjects", text="Objects", icon="PANEL_CLOSE" if options.cleanupObjects else "ADD")
		row.prop(options, "cleanupMeshes", text="Meshes", icon="PANEL_CLOSE" if options.cleanupMeshes else "ADD")
		row = layout.row(align=True)
		row.prop(options, "cleanupMaterials", text="Materials", icon="PANEL_CLOSE" if options.cleanupMaterials else "ADD")
		row.prop(options, "cleanupTextures", text="Textures", icon="PANEL_CLOSE" if options.cleanupTextures else "ADD")

		cleanupOp = layout.operator("nct.cleanup_blend_file", text="Cleanup")
		cleanupOp.cleanupObjects = options.cleanupObjects
		cleanupOp.cleanupMeshes = options.cleanupMeshes
		cleanupOp.cleanupMaterials = options.cleanupMaterials
		cleanupOp.cleanupTextures = options.cleanupTextures

def register():
	bpy.utils.register_class(FileCleanupOptions)
	bpy.utils.register_class(CleanupBlendFile)
	bpy.utils.register_class(FileCleanupPanel)

	bpy.types.Scene.fileCleanupOptions = bpy.props.PointerProperty(type=FileCleanupOptions)

def unregister():
	bpy.utils.unregister_class(FileCleanupOptions)
	bpy.utils.unregister_class(CleanupBlendFile)
	bpy.utils.unregister_class(FileCleanupPanel)

	del bpy.types.Scene.fileCleanupOptions
