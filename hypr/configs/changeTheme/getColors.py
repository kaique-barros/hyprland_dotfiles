import colorgram
import argparse
import sys
import os
from pathlib import Path
import matplotlib.colors as mcolors


def get_colors(image_file, numcolors=3): #Get the dominant colors of the wallpaper
    colors = colorgram.extract(image_file, numcolors)
    colorsbase = []
    colorsinv = []

    for color in colors: 
            red = color.rgb.r
            green = color.rgb.g
            blue = color.rgb.b
    
            rgb = (red/256, green/256, green/256)                                                       #Matplotlib needs the values between 0 and 1
            rgb_inv = (((red - 255) * -1 / 256), ((green - 255) * -1 / 256), ((blue - 255) * -1 / 256)) #The color but inverted

            hex_color = mcolors.to_hex(rgb, keep_alpha=False)[1:7]
            hex_inv_color = mcolors.to_hex(rgb_inv, keep_alpha=False)[1:7]

            colorsbase.append(hex_color)
            colorsinv.append(hex_inv_color)

    colorslist = [colorsbase, colorsinv]

    return colorslist


HOME = os.environ['HOME']

def write_hypr_conf(colors, wallpaperName): #Write the selected colors in /hyprPath/changeTheme/color-themes/WALLPAPERNAME-colors archive
    pathHypr = f"{HOME}/.config/hypr/configs/changeTheme/color-themes"  #Directory for saving the color schemes in hyprland configs  
    output = f"{wallpaperName}-colors"                                #Name of the color scheme for that wallpaper

    #Check the path 
    if not Path(f"{pathHypr}/{output}").exists():
        open(f"{pathHypr}/{output}", "x")

    with open(f"{pathHypr}/{output}", "w") as hypr:
        for color in colors: 
            index = colors.index(color)
            
            HyprConfFormat = f"$cor{index} = rgba({color}ee)"

            print(HyprConfFormat, file=hypr)

    hypr.close()

def write_waybar_conf(colors, colorsinv, wallpaperName): #
    pathWaybar = f"{HOME}/.config/waybar/changeTheme/color-themes"      #Directory for saving the color schemes in waybar configs 
    output = f"{wallpaperName}-colors"                                #Name of the color scheme for that wallpaper
    
    #Check the path
    if not Path(f"{pathWaybar}/{output}").exists():
        open(f"{pathWaybar}/{output}", "x")

    #Write the colors in both config directories
    with open(f"{pathWaybar}/{output}", "w") as waybar:
        for color in colors: 
            index = colors.index(color)
            
            WaybarConfFormat = f"@define-color cor{index} #{color};"
            WaybarConfFormat_inv = f"@define-color cor-inv{index} #{colorsinv[index]};"
    
            print(WaybarConfFormat, file=waybar)
            print(WaybarConfFormat_inv, file=waybar)
   
    waybar.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: getColors.py [wallpaperName] [options]")
        sys.exit()

    wallpaper = sys.argv[1]
    wallpaper_Full = f"{HOME}/wallpapers/{wallpaper}"   #Wallpapers Directory
    wallpaper_clean = wallpaper.split('.')[0]           #Wallpaper without the archive extension

    colorslist = get_colors(wallpaper_Full)
    colors = colorslist[0]
    colorsinv = colorslist[1]

    if len(sys.argv) == 3:
        match sys.argv[2]:
            case "--hypr":
                write_hypr_conf(colors, wallpaper_clean)
            case "--waybar":
                print("unable to use in moment")
                #write_waybar_conf(colors, colorsinv, wallpaper_clean)
            case _:
                print(f"'{sys.argv[2]}' is not a valid option.")
    else:
        write_hypr_conf(colors, wallpaper_clean)
        write_waybar_conf(colors, colorsinv, wallpaper_clean)
