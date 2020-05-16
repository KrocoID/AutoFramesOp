# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Auto Frames options",
    "author": "David Savini",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "Proprieties > scene > Automatic Frames Options" ,
    "description": "Choose the numbre of frames to skip between two keyframe",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy


bpy.types.WindowManager.Set_Frame = bpy.props.IntProperty(name="Set_Frame",  description= "Number of frames you want to skip. Last frame is moving", default = 10, min=0)
bpy.types.WindowManager.Set_Last_Frame = bpy.props.IntProperty(name="Setting",  description= "Number of frames you want between the cursor and the last frame", default = 10, min=0)
bpy.types.WindowManager.Move_Frame = bpy.props.IntProperty(name="Setting",  description= "Number of frames you want to skip", default = 10, min=0)





def lastFrame():
    last_frame = bpy.context.window_manager.Set_Last_Frame
    bpy.context.scene.frame_end = bpy.context.scene.frame_current + last_frame



def moveframe() :
        set_frame = bpy.context.window_manager.Set_Frame
        bpy.context.scene.frame_start = 0    
        bpy.context.scene.frame_current = bpy.context.scene.frame_current + set_frame
        bpy.context.scene.frame_end = bpy.context.scene.frame_current + set_frame
        
def currentframe() :
        set_frame = bpy.context.window_manager.Move_Frame
        last_frame = bpy.context.window_manager.Set_Last_Frame
        
        bpy.context.scene.frame_current = bpy.context.scene.frame_current + set_frame
        
        if  bpy.context.scene.frame_end < bpy.context.scene.frame_current :
            bpy.context.scene.frame_end = bpy.context.scene.frame_current
            return
           
       
#Bouton pour se déplacer à la dernière keyframe
class Jump_Last_Frame(bpy.types.Operator):
    '''Play n Stop'''
    bl_idname = "jump.lastframe"
    bl_label = "last keyFrame"
    


    def execute(self, context):
       
        bpy.ops.screen.frame_jump(end=True)
        bpy.ops.screen.keyframe_jump(next=False )
       

        return {'FINISHED'}       
        


#Ajoute un bouton qui fera avancer automatiquement le curseur d'un nombre défini de frame ainsi que la dernière
class ADDFRAME_OT(bpy.types.Operator):
    """OPEN"""
    bl_label = "Move Frame with Last frame"
    bl_idname = "addframe.ot"

    def execute(self, context):
        moveframe() 
        lastFrame()    
        return {'FINISHED'}

#Ajoute un bouton qui fera avancer automatiquement le curseur d'un nombre défini de frame
class ADDFRAME_OT_2(bpy.types.Operator):
    """OPEN"""
    bl_label = "Move Current Frame"
    bl_idname = "addframe.ot_2"

    def execute(self, context):
        currentframe()
        return {'FINISHED'}



class AFO_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Automatic Frame Option"
    bl_idname = "SCENE_PT_AFO_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon= "ARROW_LEFTRIGHT")
    
    def draw(self, context):
        layout = self.layout
        
        obj = context.object
        scene = context.scene
        
        layout.label(text="Move the cursor and the last frame")
        row = layout.row()
        row.operator("addframe.ot", text="", icon="MOUSE_LMB")
        row.prop(context.window_manager, "Set_Frame", text="Current Frame")
        row.prop(context.window_manager, "Set_Last_Frame", text="Last Frame")
        layout.label(text="Move the cursor only")
        row = layout.row()
        row.operator("addframe.ot_2", text="", icon="MOUSE_LMB")
        row.prop(context.window_manager, "Move_Frame", text="To next frame")
        row = layout.row()
        row.operator("jump.lastframe")






addon_keymaps = []




def register():
    bpy.utils.register_class(ADDFRAME_OT)
    bpy.utils.register_class(ADDFRAME_OT_2)
    bpy.utils.register_class(Jump_Last_Frame)
    bpy.utils.register_class(AFO_Panel)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("addframe.ot", type='F', value='PRESS', ctrl=True)
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("addframe.ot_2", type='F', value='PRESS', alt=True)
        
        addon_keymaps.append((km, kmi))
    
    
    
    
def unregister():
    for km,kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    
    bpy.utils.unregister_class(ADDFRAME_OT)
    bpy.utils.unregister_class(ADDFRAME_OT_2)
    bpy.utils.unregister_class(Jump_Last_Frame)
    bpy.utils.unregister_class(AFO_Panel)
    
if __name__ == "__main__":
    register()
    
    