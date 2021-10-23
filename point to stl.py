from stl import mesh
num_triangles=len(fin_list)
data = np.zeros(num_triangles, dtype=mesh.Mesh.dtype)
for i in range(num_triangles):
    #I did not know how to use numpy-arrays in this case. This was the major roadblock
    # assign vertex co-ordinates to variables to write into mesh
    data["vectors"][i] = np.array([[v1x, v1y, v1z],[v2x, v2y, v2z],[v3x, v3y, v3z]])
m=mesh.Mesh(data)
m.save('filename.stl')