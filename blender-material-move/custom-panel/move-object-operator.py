bl_info={
  "name": "Move Selected Object",
  "blender": (2, 80, 0),
  "category": "Object",
  "author": "BettyCheng",
}

import bpy

class MoveSelectedObject(bpy.types.Operator):
  bl_idname = "object.move_selected"
  bl_label = "Move Selected Object by specific displacement"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self,context):
    # scene = context.scene
    obj = bpy.context.object
    displacementPlaceholder = bpy.context.scene.placeholder
    obj.location.x += displacementPlaceholder.inc_dec_int_x
    obj.location.y += displacementPlaceholder.inc_dec_int_y
    obj.location.z += displacementPlaceholder.inc_dec_int_z
    
    return {'FINISHED'}
  
def menu_func(self, context):
    self.layout.operator(MoveSelectedObject.bl_idname)
def register():
    bpy.utils.register_class(MoveSelectedObject)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(MoveSelectedObject)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()