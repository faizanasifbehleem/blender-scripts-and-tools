import bpy, time

for i in range(8):
    for j in range(10):
        if i == 0:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(j, j, j))
        elif i == 1:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(-j, -j, -j))
        elif i == 2:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(-j, j, j))
        elif i == 3:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(-j, -j, j))
        elif i == 4:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(j, -j, j))
        elif i == 5:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(j, j, -j))
        elif i == 6:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(-j, j, -j))
        elif i == 7:
            bpy.ops.mesh.primitive_uv_sphere_add(location=(j, -j, -j))
        #time.sleep(0.1)
