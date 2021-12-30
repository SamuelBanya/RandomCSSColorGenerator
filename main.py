import os, random, requests, math
from pathlib import Path
from pathlib import PurePath
from pathlib import PosixPath
import itertools


# Taken from here:
# https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
def determine_light_or_dark_color(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb_color = tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))
    # Taken from here:
    # https://stackoverflow.com/questions/22603510/is-this-possible-to-detect-a-colour-is-a-light-or-dark-colour
    [r,g,b]=rgb_color
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if (hsp>127.5):
        return 'light'
    else:
        return 'dark'


def grab_lospec_palette():
    response = requests.get("https://lospec.com/palette-list/load?colorNumberFilterType=max&colorNumber=8&page=1&tag=&sortingType=default")
    palette_length = len(response.json()['palettes'])
    palette_list = []
    for i in range(palette_length):
        palette_list.append((response.json()['palettes'][i]['colorsArray']))
    random_palette = random.choice(palette_list)

    return random_palette


def create_css_sheet_with_lospec_palette(random_palette):
    print('Now entering create_css_sheet_with_lospec_palette() function...')
    print('Checking random_palette to make sure it has at least 4 colors...')
    if len(random_palette) < 4:
        print('random_palette doesn\'t have 4 colors... Skipping')

    else:
        print('random_palette DOES have at least 4 colors. Proceeding...')
        content = str('#page_background {')
        content += str('position: fixed;')
        content += str('top: 0; left: 0; width: 100%; height: 100%;')
        # content = str('body { background-color: #')
        # content += str(random_palette[0])
        # content += str('; ')
        content += str('background-image: url("')
        # Borrowed code from 'Art Gallery Creator' project:
        art_gallery_path = '/var/www/musimatic/images/ArtGallery'
        os.chdir(art_gallery_path)
        picture_directories = sorted(filter(os.path.isdir, os.listdir(art_gallery_path)))
        print('\npicture_directories: ' + str(picture_directories))
        directory = random.choice(picture_directories)
        print('\ndirectory: ' + str(directory))
        picture_paths_jpg = (x.resolve() for x in Path(directory).glob("*.jpg"))
        picture_paths_png = (x.resolve() for x in Path(directory).glob("*.png"))
        picture_paths = itertools.chain(picture_paths_jpg, picture_paths_png)
        picture_paths_strings = [str(p) for p in picture_paths]
        print('\npicture_paths_strings: ' + str(picture_paths_strings))
        picture_path = random.choice(picture_paths_strings)
        print('\npicture_path: ' + str(picture_path))
        regular_image_version = str(picture_path).replace('/var/www/musimatic/', 'https://musimatic.xyz/')
        content += str(regular_image_version)
        content += str('");')
        content += str('background-repeat: no-repeat; background-attachment: fixed;')
        content += str('background-size: 100%;')
        content += str('opacity: 0.4; filter:alpha(opacity=40); z-index: -1; }')
        content += str('#top_banner_div { border-top: 3px solid #')
        content += str(random_palette[0])
        content += str('; border-bottom: 3px solid #')
        content += str(random_palette[0])
        content += str('; background-color: #')
        content += str(random_palette[1])
        content += str(';')
        # Determine if 'random_palette[1]' color is dark or light:
        print('random_palette[1] hexcode: ' + str(random_palette[1]))
        dark_or_light_palette_1 = determine_light_or_dark_color(random_palette[1])
        print('dark_or_light_palette_1: ' + str(dark_or_light_palette_1))
        if dark_or_light_palette_1 == 'dark':
            content += str('color: white; text-align: center; }')
        if dark_or_light_palette_1 == 'light':
            content += str('color: black; text-align: center; }')
        content += str('#left_menu_div { font-size: 15px; width: 134px; float: left; clear: both;')
        content += str('font-family: Arial, Helvetica, sans-serif; }')
        content += str('#left_menu_div a { color: white; }')
        content += str('#left_menu_div a:hover { text-decoration:none;')
        content += str('text-shadow:-1px 0 red,0 1px red,1px 0 red,0 -1px red,-1px -1px red,1px 1px red,-1px 1px red,1px -1px red;')
        content += str('transition: 0.3s }')
        content += str('.left_menu_section { border-radius: 5px; overflow: hidden; box-shadow: 4px 4px 10px -5px rgba(0,0,0,0.75);')
        content += str('margin: 0 auto 15px 0; }')
        content += str('.left_menu_section p { margin: 0; }')

        content += str('.left_menu_top_bar { text-align:center; ')
        # Determine if 'random_palette_2' is dark or light:
        print('random_palette[2] hexcode: ' + str(random_palette[2]))
        dark_or_light_palette_2 = determine_light_or_dark_color(random_palette[2])
        print('dark_or_light_palette_2: ' + str(dark_or_light_palette_2))
        if dark_or_light_palette_2 == 'dark':
            content += str('color: white')
        if dark_or_light_palette_2 == 'light':
            content += str('color: black')
        content += str('; box-shadow: 0 16px 20px rgba(255,255,255,.15) inset;')
        content += str('background-color: #')
        content += str(random_palette[2])
        content += str('; margin-bottom: 0px; }')
        content += str('.left_menu_bottom_section { padding: 4px; background-color: #')
        content += str(random_palette[3])
        content += str(';')

        # Determine if 'random_palette[3]' color is dark or light:
        print('random_palette[3] hexcode: ' + str(random_palette[3]))
        dark_or_light_palette_3 = determine_light_or_dark_color(random_palette[3])
        print('dark_or_light_palette_3: ' + str(dark_or_light_palette_3))
        if dark_or_light_palette_3 == 'dark':
            content += str('color: white; }')
        if dark_or_light_palette_3 == 'light':
            content += str('color: black; }')
        
        # Place css sheet in '/var/www/musimatic/css' directory:
        with open('/var/www/musimatic/css/index.css', 'w') as f:
            f.write(content)
        f.close()


def create_css_sheet_with_grey_purple_scheme():
    print('Now entering create_css_sheet_with_grey_purple_scheme() function...')
    content = str('body { background-color: grey; }')
    content += str('#top_banner_div { border-top: 3px solid blue; border-bottom: 3px solid blue; background-color: purple; ')
    content += str('color: white; text-align: center; }')
    content += str('#left_menu_div { font-size: 15px; width: 134px; float: left; clear: both; ')
    content += str('font-family: Arial, Helvetica, sans-serif; }')
    content += str('#left_menu_div a { color: white; }')
    content += str('#left_menu_div a:hover { text-decoration:none;')
    content += str('text-shadow:-1px 0 red,0 1px red,1px 0 red,0 -1px red,-1px -1px red,1px 1px red,-1px 1px red,1px -1px red;')
    content += str('transition:0.3s }')
    content += str('.left_menu_section { border-radius: 5px; overflow: hidden; box-shadow: 4px 4px 10px -5px rgba(0,0,0,0.75);')
    content += str('margin: 0 auto 15px 0; }')
    content += str('.left_menu_section p { margin: 0; }')
    content += str('.left_menu_top_bar { color: lightblue; box-shadow: 0 16px 20px rgba(255,255,255,.15) inset; text-align: center;')
    content += str('margin-bottom: 0px; }')
    content += str('.left_menu_bottom_section { padding: 4px; background-color: black; }')

    # Place css sheet in '/var/www/musimatic/css' directory:
    with open('/var/www/musimatic/css/index.css', 'w') as f:
        f.write(content)
    f.close()


def main():
    random_number = random.randint(1, 100)
    if random_number < 50:
        print('HEADS! Revert back to the grey purple color scheme!')
        create_css_sheet_with_grey_purple_scheme()
    elif random_number > 50:
        print('TAILS! Let\'s change the color palette!')
        random_palette = grab_lospec_palette()
        create_css_sheet_with_lospec_palette(random_palette)


if __name__ == "__main__":
    main()
