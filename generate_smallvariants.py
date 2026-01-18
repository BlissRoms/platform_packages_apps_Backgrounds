#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import os
from PIL import Image

path = os.path.dirname(os.path.realpath(__file__))

resources = ["res/drawable-nodpi"]

def generate_smallvariants(resource):
    global path
    wallpapers_path = os.path.join(path, resource)
    clean(wallpapers_path)
    wallpapers = os.listdir(wallpapers_path)

    for wallpaper in wallpapers:
        # Skip existing small variants to avoid reprocessing
        if wallpaper.endswith("_small.jpg"):
            continue

        wallpaper_small = os.path.splitext(wallpaper)[0] + "_small.jpg"
        wallpaper_small_path = os.path.join(wallpapers_path, wallpaper_small)

        try:
            with Image.open(os.path.join(wallpapers_path, wallpaper)) as img:
                size = int(img.width / 4), int(img.height / 4)
                img_small = img.resize(size, Image.Resampling.LANCZOS)

                # Convert RGBA to RGB if needed (JPEG doesn't support transparency)
                if img_small.mode == 'RGBA':
                    img_small = img_small.convert('RGB')

                img_small.save(wallpaper_small_path, "JPEG", quality=90)
        except Exception as e:
            print(f"Error processing {wallpaper}: {e}")

def clean(wallpapers_path):
    wallpapers = os.listdir(wallpapers_path)

    for wallpaper in wallpapers:
        # Remove existing small variants
        if wallpaper.endswith("_small.jpg"):
            try:
                os.remove(os.path.join(wallpapers_path, wallpaper))
            except Exception as e:
                print(f"Error deleting {wallpaper}: {e}")

for resource in resources:
    generate_smallvariants(resource)
