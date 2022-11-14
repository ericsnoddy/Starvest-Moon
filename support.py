# std lib
from os import walk

# reqs
import pygame as pg


def import_folder(path):
    surf_list = []
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            img_surf = pg.image.load(full_path).convert_alpha()
            surf_list.append(img_surf)

    return surf_list


def import_folder_dict(path):
    # key = folder name, value = list of img surfs within
    surf_dict = {}
    for _, __, img_files in walk(path):
        for img in img_files:
            full_path = path + '/' + img
            key = img.rsplit('.')[0]
            img_surf = pg.image.load(full_path).convert_alpha()            
            surf_dict[key] = img_surf
    return surf_dict
        
