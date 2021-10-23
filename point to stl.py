import open3d as o3d
from stl import mesh


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

poisson_mesh.compute_vertex_normals() #Przygotowanie do zapisu
print(poisson_mesh)
o3d.io.write_triangle_mesh("tymczasowy.stl", poisson_mesh) #Zapis pliku w formacie STL

your_mesh = mesh.Mesh.from_file("tymczasowy.stl") #Zaczytanie danych STL

volume, cog, inertia = your_mesh.get_mass_properties()
print("Objetosc                                  = {0}".format(volume)) #wyswietlenie wyniku
