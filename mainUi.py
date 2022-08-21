import bpy
from . import outfitVisibilityUi
from . import outfitCombinerUi
from . import otherModelsManager
from . import fileCleanup

class MainPanel(bpy.types.Panel):
	bl_label = "Nier Character Tools"
	bl_idname = "B2N_PT_NIER_CHRACTER_TOOLS"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Character Tools"

	def draw(self, context):
		layout = self.layout
		

def register():
	bpy.utils.register_class(MainPanel)
	otherModelsManager.register()
	# outfitVisibilityUi.register()
	outfitCombinerUi.register()
	fileCleanup.register()

def unregister():
	bpy.utils.unregister_class(MainPanel)
	otherModelsManager.unregister()
	# outfitVisibilityUi.unregister()
	outfitCombinerUi.unregister()
	fileCleanup.unregister()
