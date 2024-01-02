bl_info = {
    "name": "Material Custom Panel",
    "author": "Betty Cheng",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Mateiral >",
    "description": "This is a test UI addon w/ integer button and add material button",
    "warning": "",
    "doc_url": "",
    "category": "Material",
}


import bpy
from bpy.types import Panel, PropertyGroup, Scene, WindowManager
from bpy.props import (
    IntProperty,
    EnumProperty,
    StringProperty,
    PointerProperty,
)

RGB = ["red", "green", "blue"]
DIRECTION = ["x", "y", "z"]

class MYTEST_PT_Panel(Panel):
    bl_idname = "MYTEST_MATERIAL_PT_Panel"
    bl_label = "Add New Light Dance Material"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
#    bl_space_type = "VIEW_3D"
#    bl_region_type = "UI"
#    bl_category = "MY TEST"
#    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        placeholder = context.scene.placeholder
        col = layout.column()

        # col.prop(placeholder, "inc_dec_int_red", text="Red")
        col.prop(placeholder, "selected_material", text="Selected Material")
        col.prop(placeholder, "color_name", text="New Color Name")
        row = layout.row()
        for color in RGB:
          whichVariable = "inc_dec_int_" + color
          row.prop(placeholder, whichVariable, text = color)
        row = layout.row()
        row.operator("material.add_green_sphere", text="Add a material")
        row.operator("material.change_color")
        col = layout.column()
        col.operator("material.change_object_material")
        
        row = layout.row()
        for dir in DIRECTION:
            whichVariable = "inc_dec_int_" + dir
            row.prop(placeholder, whichVariable, text = dir)
        row = layout.row()
        row.operator("object.move_selected")



class PlaceholderProperties(PropertyGroup):
    inc_dec_int_red: IntProperty(
        name="Incr-Decr-r", min=0, default=255,max=255, description="RGB value for red"
    )
    inc_dec_int_green: IntProperty(
        name="Incr-Decr-g", min=0, default=255,max=255, description="RGB value for green"
    )
    inc_dec_int_blue: IntProperty(
        name="Incr-Decr-b", min=0, default=255,max=255, description="RGB value for blue"
    )
    inc_dec_int_x: IntProperty(
        name="Incr-Decr-x", min=-100, default=0,max=100, description="x displacement"
    )
    inc_dec_int_y: IntProperty(
        name="Incr-Decr-y", min=-100, default=0,max=100, description="y displacement"
    )
    inc_dec_int_z: IntProperty(
        name="Incr-Decr-z", min=-100, default=0,max=100, description="z displacement"
    )
    
    
        
    def get_items_callback(self, context):
        
        def by_script(m):
            return m.get('createdByScript') is not None
        
        materialsByScript = filter(by_script, bpy.data.materials)
#        materialsByScript = bpy.data.materials
        # print("materialsByScript = ", materialsByScript)
        allMaterials = [m.name for m in materialsByScript]

        dropDownItems = []

        for m in allMaterials:
            tmpItem = (m, m, "tooltip for a",)
            dropDownItems.append(tmpItem)
#        print(dropDownItems)    
#        dropDownItems = [
#            ("A", "Ahh", "Tooltip for A"),
#            ("B", "Be", "Tooltip for B"),
#            ("C", "Ce", "Tooltip for C")
#        ]
        
        return dropDownItems
    
#    my_item = get_items()
#    if(len(my_item)!=0):
#        print(my_item[0][0])
    selected_material: EnumProperty(
        items=get_items_callback,
        name="Description for the Elements",
        description="Tooltip for the Dropdownbox",
    )
    color_name: StringProperty(
        name="New-Color-Name",
        default="new color",
        description="Wanted File",
        maxlen=100,
    )

        
        
        
classes = (
    PlaceholderProperties,
    MYTEST_PT_Panel,
)

def register():
    #the usual registration...
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    Scene.placeholder = PointerProperty(type=PlaceholderProperties)

def unregister():
    #the usual unregistration in reverse order ...

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

    del Scene.placeholder

if __name__ == "__main__":
    register()