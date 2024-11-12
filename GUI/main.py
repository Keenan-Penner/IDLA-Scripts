from interface import *
import os

if __name__ == "__main__":
    #create a folder with the correct names
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    parent_folder = 'sim'
    child_folder2D = '2D'
    child_folder3D = '3D'
    child_child_classical = 'classical'
    child_child_multi = 'multisource'
    if not os.path.exists(parent_folder):
        os.makedirs(f"{parent_folder}\\{child_folder2D}\\{child_child_classical}")
        os.makedirs(f"{parent_folder}\\{child_folder2D}\\{child_child_multi}")
        os.makedirs(f"{parent_folder}\\{child_folder3D}\\{child_child_classical}")
        os.makedirs(f"{parent_folder}\\{child_folder3D}\\{child_child_multi}")
    gui = MyGUI()