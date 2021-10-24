import open3d as o3d
from stl import mesh
import numpy as np



input_path="C:/Users/Tomek/PycharmProjects/objetosc/" ##Droga do pliku
output_path="C:/Users/Tomek/PycharmProjects/objetosc/render/" #Gdzie zapisywac (Nie wykorzystane w tej wersji)
dataname=("sphere_spiral_700.xyz")


pcd = o3d.io.read_point_cloud(dataname) ##zaczytanie pliku
downpcd = pcd.voxel_down_sample(voxel_size=0.05) #zmniejszanie rozmiaru, mniejsza liczba = wieksza precyzja)


downpcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.3, max_nn=300)) #Kalkulacja normalnych

downpcd.orient_normals_consistent_tangent_plane(10) #Poprawka noramlanych

#o3d.visualization.draw_geometries([downpcd], point_show_normal=True) #Wizualizacja normalnych



poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(downpcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]
#Jedna z opcji znajdowania i rekonstrukcji ścian. Wymaga normalnych wyliczonych wcześniej

#o3d.visualization.draw_geometries([poisson_mesh]) #prezentacja pełnej bryły



#filtrowanie odizolowanych bryl --------------------------------------------------------
mesh_0 = poisson_mesh
vert = np.asarray(mesh_0.vertices)
min_vert, max_vert = vert.min(axis=0), vert.max(axis=0)
for _ in range(30):
    cube = o3d.geometry.TriangleMesh.create_box()
    cube.scale(0.005, center=cube.get_center())
    cube.translate(
        (
            np.random.uniform(min_vert[0], max_vert[0]),
            np.random.uniform(min_vert[1], max_vert[1]),
            np.random.uniform(min_vert[2], max_vert[2]),
        ),
        relative=False,
    )
    mesh_0 += cube
mesh_0.compute_vertex_normals()
##o3d.visualization.draw_geometries([mesh_0])

with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    triangle_clusters, cluster_n_triangles, cluster_area = (
        mesh_0.cluster_connected_triangles())
triangle_clusters = np.asarray(triangle_clusters)
cluster_n_triangles = np.asarray(cluster_n_triangles)
cluster_area = np.asarray(cluster_area)

mesh_1 = mesh_0
triangles_to_remove = cluster_n_triangles[triangle_clusters] < 100
mesh_1.remove_triangles_by_mask(triangles_to_remove)
##o3d.visualization.draw_geometries([mesh_0])
#koniec_filtrowania ---------------------------------------------------------


mesh_1.compute_vertex_normals() #Przygotowanie do zapisu
print(mesh_1)
o3d.io.write_triangle_mesh("tymczasowy.stl", mesh_1) #Zapis pliku w formacie STL

mesh_odczyt = mesh.Mesh.from_file("tymczasowy.stl") #Zaczytanie danych STL

volume, cog, inertia = mesh_odczyt.get_mass_properties()
print("Objetosc                                  = {0}".format(volume)) #wyswietlenie wyniku
