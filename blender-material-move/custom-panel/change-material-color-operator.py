bl_info = {
    "name": "Change material Color",
    "blender": (2, 80, 0),
    "category": "Material",
}

import bpy


class ChangeMaterialColor(bpy.types.Operator):
    """My material adding test"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "material.change_color"    # Unique identifier for buttons and menu items to reference.
    bl_label = "Change color of a material"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def create_material(self,name):
        # create a new material
        material = bpy.data.materials[name]
        # material = bpy.data.materials.new(name=name)

        # enable creating a material via nodes
        material.use_nodes = True

        # get a reference to the Principled BSDF shader node
        principled_bsdf_node = material.node_tree.nodes["Principled BSDF"]
        
        # get scene placeholder
        colorPlaceholder = bpy.context.scene.placeholder

        # set the base color of the material
        principled_bsdf_node.inputs["Base Color"].default_value = (colorPlaceholder.inc_dec_int_red/255, colorPlaceholder.inc_dec_int_green/255, colorPlaceholder.inc_dec_int_blue/255, 1)
        # inputs[0] can be written as inputs["Base Color"]

        # set the metallic value of the material
        principled_bsdf_node.inputs["Metallic"].default_value = 1.0

        # set the roughness value of the material
        principled_bsdf_node.inputs["Roughness"].default_value = 0.5
        
        return material

    def add_mesh(self):
        
        # create an ico sphere
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5)

        # shade smooth
        bpy.ops.object.shade_smooth()

        # get reference to mesh object
        mesh_obj = bpy.context.active_object
        
        return mesh_obj
    

    

    def execute(self, context):
#        self.partially_clean()
        # read name from placeholder
        name = bpy.context.scene.placeholder.dropdown_box
        material = self.create_material(name)
        
#        mesh_obj = self.add_mesh() 
        # apply the material to the mesh object
#        mesh_obj.data.materials.append(material)
        return {'FINISHED'}
        # def execute(self, context):        # execute() is called when running the operator.

        #     # The original script
        #     scene = context.scene
        #     for obj in scene.objects:
        #         obj.location.x += 1.0

        #     return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def menu_func(self, context):
    self.layout.operator(ChangeMaterialColor.bl_idname)

def register():
    bpy.utils.register_class(ChangeMaterialColor)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(ChangeMaterialColor)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()