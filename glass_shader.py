import bpy

# json data for the sake of an example
glass_type = "Imperfect"

# Checks the render engine
renderEngine = bpy.context.scene.render.engine.lower() # Get the current render engine. i.e. blender_eevee or cycles
isCycles = bool(renderEngine == 'cycles')
isEEVEE = bool(renderEngine == 'blender_eevee')

# Test whether the material exists, if it doesn't, then create it.
mat_name = "M_Glass_Shader"
mat = (bpy.data.materials.get(mat_name) or bpy.data.materials.new(mat_name))

# Sets this material as the active material
obj = bpy.context.active_object
obj.active_material = mat

# Enable 'Use nodes':
mat.use_nodes = True
nodes = mat.node_tree.nodes

# Set the parent node
parent_node = nodes.get("Principled BSDF")

# Functions for nodes operations
def ConnectTwoNodes(firstNode, secondNode, firstNodeOutputName, secondNodeInputName):
    mat.node_tree.links.new(firstNode.outputs[firstNodeOutputName], secondNode.inputs[secondNodeInputName])
    
def CreateGenericNode(nodeName, PosX, PosY):
    genericNode = nodes.new(nodeName)
    genericNode.location = (PosX, PosY)
    return genericNode

'''Sets the glass shader properties'''

# Sets the color to pure white
parent_node.inputs["Base Color"].default_value = (1, 1, 1, 1)

# Set the roughness value to 0
parent_node.inputs["Roughness"].default_value = 0.0

# Sets IOR of glass to 1.50
parent_node.inputs["IOR"].default_value = 1.50

# Sets the Transmission to 1
parent_node.inputs["Transmission"].default_value = 1.0

if glass_type == "Imperfect":
    
    '''Adds and makes network of all the nodes needed for the smudges imperfections'''
    
    # Adds a clamp node and connects it to the parent node
    clamp_node = CreateGenericNode("ShaderNodeClamp", -180, 70)
    clamp_node.inputs["Value"].default_value = 0
    clamp_node.inputs["Min"].default_value = 0
    clamp_node.inputs["Max"].default_value = 1
    ConnectTwoNodes(clamp_node, parent_node, "Result", "Roughness")
    
    # Adds a color ramp node and connects it to the clamp node
    color_ramp_node = CreateGenericNode("ShaderNodeValToRGB", -470, 70)
    color_ramp_node.color_ramp.elements[0].position = 0.522
    color_ramp_node.color_ramp.elements[1].position = 0.873
    ConnectTwoNodes(color_ramp_node, clamp_node, "Color", "Value")
    
    # Adds a MixRGB node and connects it to the color ramp node
    mix_rgb_node_01 = CreateGenericNode("ShaderNodeMixRGB", -660, 60)
    mix_rgb_node_01.blend_type = 'MIX'
    mix_rgb_node_01.inputs["Fac"].default_value = 0.273
    ConnectTwoNodes(mix_rgb_node_01, color_ramp_node, "Color", "Fac")
    
    '''Small Smudges Setup'''
    
    # Adds a MixRGB node and connects it to first input of mix_rgb_node_01
    mix_rgb_node_02 = CreateGenericNode("ShaderNodeMixRGB", -950, 280)
    mix_rgb_node_02.blend_type = 'MIX'
    mix_rgb_node_02.inputs["Fac"].default_value = 0.240
    ConnectTwoNodes(mix_rgb_node_02, mix_rgb_node_01, "Color", "Color1")
    
    # Adds a noise texture node and connects it to the mix node
    noise_tex_node_01 = CreateGenericNode("ShaderNodeTexNoise", -1150, 380)
    noise_tex_node_01.inputs["Scale"].default_value = 34.0
    noise_tex_node_01.inputs["Detail"].default_value = 10.20
    noise_tex_node_01.inputs["Roughness"].default_value = 0.213
    noise_tex_node_01.inputs["Distortion"].default_value = 3.0
    ConnectTwoNodes(noise_tex_node_01, mix_rgb_node_02, "Color", "Color1")
    
    # Adds a musgrave texture node and connects it to the mix node
    musgrave_tex_node_01 = CreateGenericNode("ShaderNodeTexMusgrave", -1150, 150)
    musgrave_tex_node_01.inputs["Scale"].default_value = 64.10
    musgrave_tex_node_01.inputs["Detail"].default_value = 6.10
    musgrave_tex_node_01.inputs["Dimension"].default_value = 0.50
    musgrave_tex_node_01.inputs["Lacunarity"].default_value = 1.50
    ConnectTwoNodes(musgrave_tex_node_01, mix_rgb_node_02, "Fac", "Color2")
    
    # Frames all of the small smudges setup nodes
    frame_node_01 = CreateGenericNode("NodeFrame", 0, 0)
    frame_node_01.label = "Small Smudges"
    mix_rgb_node_02.parent = frame_node_01
    noise_tex_node_01.parent = frame_node_01
    musgrave_tex_node_01.parent = frame_node_01
    
    '''Big Smudges Setup'''
    
    # Adds a MixRGB node and connects it to second input of mix_rgb_node_01
    mix_rgb_node_03 = CreateGenericNode("ShaderNodeMixRGB", -950, -230)
    mix_rgb_node_03.blend_type = 'MIX'
    mix_rgb_node_03.inputs["Fac"].default_value = 0.3470
    ConnectTwoNodes(mix_rgb_node_03, mix_rgb_node_01, "Color", "Color2")
    
    # Adds a noise texture node and connects it to the mix node
    noise_tex_node_02 = CreateGenericNode("ShaderNodeTexNoise", -1150, -150)
    noise_tex_node_02.inputs["Scale"].default_value = 10.10
    noise_tex_node_02.inputs["Detail"].default_value = 13.0
    noise_tex_node_02.inputs["Roughness"].default_value = 0.213
    noise_tex_node_02.inputs["Distortion"].default_value = 0.40
    ConnectTwoNodes(noise_tex_node_02, mix_rgb_node_03, "Color", "Color1")
    
    # Adds a musgrave texture node and connects it to the mix node
    musgrave_tex_node_02 = CreateGenericNode("ShaderNodeTexMusgrave", -1150, -375)
    musgrave_tex_node_02.inputs["Scale"].default_value = 9.20
    musgrave_tex_node_02.inputs["Detail"].default_value = 16.0
    musgrave_tex_node_02.inputs["Dimension"].default_value = 0.20
    musgrave_tex_node_02.inputs["Lacunarity"].default_value = 1.30
    ConnectTwoNodes(musgrave_tex_node_02, mix_rgb_node_03, "Fac", "Color2")
    
    # Frames all of the big smudges setup nodes
    frame_node_02 = CreateGenericNode("NodeFrame", 0, 0)
    frame_node_02.label = "Big Smudges"
    mix_rgb_node_03.parent = frame_node_02
    noise_tex_node_02.parent = frame_node_02
    musgrave_tex_node_02.parent = frame_node_02
    
    # Adds a mapping node and connects it to all the texture nodes
    mapping_node = CreateGenericNode("ShaderNodeMapping", -1650, 280)
    mapping_node.vector_type = 'TEXTURE'
    ConnectTwoNodes(mapping_node, noise_tex_node_01, "Vector", "Vector")
    ConnectTwoNodes(mapping_node, musgrave_tex_node_01, "Vector", "Vector")
    ConnectTwoNodes(mapping_node, noise_tex_node_02, "Vector", "Vector")
    ConnectTwoNodes(mapping_node, musgrave_tex_node_02, "Vector", "Vector")

    # Adds a texture coordinates node and connects it to the mapping node
    tex_coord_node = CreateGenericNode("ShaderNodeTexCoord", -1830, 280)
    ConnectTwoNodes(tex_coord_node, mapping_node, "Object", "Vector")
    
else:
    pass # If no imperfections are needed on the glass, then don't add smudges to the glass



