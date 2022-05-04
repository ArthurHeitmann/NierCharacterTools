import bpy
from . import outfitVisibilityUi
from . import outfitCombinerUi

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
	outfitVisibilityUi.register()
	outfitCombinerUi.register()

def unregister():
	bpy.utils.unregister_class(MainPanel)
	outfitVisibilityUi.unregister()
	outfitCombinerUi.unregister()
