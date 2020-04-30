import os, sys
from pathlib import Path, PurePosixPath

BANNER = """
    8 8888888888   8 8888                  .8.           ,o888888o.
    8 8888         8 8888                 .888.         8888     `88.
    8 8888         8 8888                :88888.     ,8 8888       `8.
    8 8888         8 8888               . `88888.    88 8888
    8 888888888888 8 8888              .8. `88888.   88 8888
    8 8888         8 8888             .8`8. `88888.  88 8888
    8 8888         8 8888            .8' `8. `88888. 88 8888   8888888
    8 8888         8 8888           .8'   `8. `88888.`8 8888       .8'
    8 8888         8 8888          .888888888. `88888.  8888     ,88'
    8 8888         8 888888888888 .8'       `8. `88888.  `8888888P'
    
"""
NAME = 'FLAG - Flag List, Advanced Generator'
VERSION = 'v0.1'

FLAG_FILE_EXTENSION = '.png'
DEST_FILE_EXTENSION = '.png'

DEFAULT_TITLE = 'Extra Flags'

MARGIN_TITLE_TOP = 5
MARGIN_TITLE_BOTTOM = 2

MARGIN_TOP = 1
MARGIN_FLAG_RIGHT = 1
MARGIN_TEXT_LEFT = 1
MARGIN_COLUMN_LEFT = 3

UPPER_MARGIN = 5
#BIG_TITLE_BAND_HEIGHT = 30
#BIG_TITLE_TEXT_HEIGHT = 24

MAX_COLUMN_WIDTH = 400
MAX_HEIGHT = 3500
MAX_WIDTH = 12000

TAMPA_SEPARATOR = '|'
TAMPA_FILENAME = 'listofcoordinates.txt'

FONT_FILENAME = 'DejaVuSansMono.ttf'

# enough chit chat
print(BANNER)
print(NAME, VERSION, sep=' - ')
print('')

try:
    import PIL
    from PIL import Image, ImageDraw
except:
    print('Error: Couldn''t import Pillow library (https://pillow.readthedocs.io/). Please install Pillow.')
    sys.exit(-1)

try:
    import image_utils # adapted from https://gist.github.com/turicas/1455973/8ca2c5fc823b611ea1a0f631fe2fbfef4c9591d7
except:
    print('Error: Couldn''t import Image Utils. Please make sure image_utils has been downloaded with this tool.')
    sys.exit(-1)


# UTILITIES
def validate_input_bool(prompt, true_values, false_values):
    while True:
        user_response = input(prompt)
        if user_response in true_values:
            return True
        if user_response in false_values:
            return False
        print('Invalid input, retry.')


def validate_input_dir_exists(prompt):
    while True:
        user_response = input(prompt)
        if os.path.exists(user_response):
            return user_response
        print('Invalid input, retry.')


def validate_input_rel_dir_exists(prompt, base):
    while True:
        user_response = input(prompt)
        if os.path.exists(os.path.join(base,user_response)):
            return user_response
        print('Invalid input, retry.')


def validate_input_positive_integer_or_empty(prompt):
    while True:
        user_response = input(prompt)
        if user_response == '':
            return -1
        try:
            converted_response = int(user_response)
            if converted_response >= 0:
                return converted_response
        except:
            pass
        print('Invalid input, retry')


def validate_input_positive_integer(prompt):
    while True:
        user_response = input(prompt)
        if user_response == '':
            return 0
        try:
            converted_response = int(user_response)
            if converted_response >= 0:
                return converted_response
        except:
            pass
        print('Invalid input, retry')


def validate_input_file_name(prompt, valid_extension):
    while True:
        user_response = input(prompt)
        (given_root, given_extension) = os.path.splitext(user_response)
        if str.lower(given_extension) == str.lower(valid_extension):
            return user_response
        elif given_extension == '':
            return given_root + valid_extension
        print('Invalid extension. %s expected' % valid_extension)


def validate_input_string_or_default(prompt, default_text):
    user_response = input(prompt)
    if user_response == '':
        return default_text
    return user_response


def walk_level(starting_dir, starting_depth=0, max_level=None):
    some_dir = starting_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for (root, dirs, files) in os.walk(some_dir):
        num_sep_this = root.count(os.path.sep)
        cur_level = num_sep_this - num_sep
        if cur_level < starting_depth:
            continue
        yield root, dirs, files, cur_level
        if max_level is not None:
            if num_sep + max_level <= num_sep_this:
                del dirs[:]


class Flag(object):
    def __init__(self, flag_name, rel_path, full_path, cur_level, has_image, flag_size=(16, 11), is_header=False):
        self.flag_name = flag_name
        self.rel_path = rel_path
        self.full_path = full_path
        self.level = cur_level
        self.has_image = has_image
        self.flag_size = flag_size
        self.is_header = is_header
        self.flag_position = None

    def get_image_rectangle_size(self):
        if self.has_image:
            return tuple((x + 2 for x in self.flag_size))
        else:
            return (0, 0)

    def has_tampa_string(self):
        return self.has_image and self.flag_position is not None

    def get_tampa_string(self):
        return TAMPA_SEPARATOR.join([str(self.rel_path), ','.join([str(x) for x in self.flag_position])])


def get_flags(src, flags_folder, min_depth, max_depth):
    print('Gathering the flags...')
    flags = []
    for (flags_folder, dirs, files, level) in walk_level(src, min_depth, max_depth):
        relative_dir = PurePosixPath(Path(os.path.relpath(flags_folder, flags_folder)))
        full_dir = flags_folder
        valid_files = [f for f in files if os.path.splitext(f)[1] == FLAG_FILE_EXTENSION]

        if len(valid_files) == 0:
            continue

        flags.append(Flag(os.path.basename(os.path.normpath(full_dir)), PurePosixPath(Path(relative_dir)), '', level,
                          has_image=False, is_header=True))
        for file in valid_files:
            flag_name, extension = os.path.splitext(file)
            rel_path = PurePosixPath(Path(relative_dir).joinpath(file))
            full_path = os.path.join(full_dir, file)
            the_flag = None
            try:
                image_file = Image.open(full_path)
                flag_size = image_file.size
                the_flag = Flag(flag_name, rel_path, full_path, level, has_image=True, flag_size=flag_size)
            except:
                the_flag = Flag(flag_name, rel_path, full_path, level, has_image=False)
            finally:
                flags.append(the_flag)
    return flags


def generate_tampa(flagzz):
    print('Generating TAMPA file...')
    with open(TAMPA_FILENAME, 'w', encoding='utf8') as f:
        for flag in flagzz:
            if flag.has_tampa_string():
                f.write('%s\n' % flag.get_tampa_string())


def get_max_flag_width(flagzz):
    max_flag_rectangle_width = max(
        [list(flagz.get_image_rectangle_size())[0] for flagz in flagzz if flagz.has_image])
    return max_flag_rectangle_width


def give_valid_position(x, y, h, c):
    if y + h >= MAX_HEIGHT:
        y = UPPER_MARGIN
        x = x + c + 5
        c = 0
    return (x, y, c)


# INPUT
FLAGS_FOLDER = validate_input_dir_exists('Path to flags/ folder: ')
REL_FOLDER = validate_input_rel_dir_exists('Relative path to root folder to parse: ', FLAGS_FOLDER)

MAX_FOLDER_DEPTH = validate_input_positive_integer_or_empty('Maximum folder recursion depth from given root (default no limit):')

MIN_FOLDER_DEPTH = validate_input_positive_integer('Initial folder recursion depth from given root (default 0):')
MIN_FOLDER_DEPTH = min(MIN_FOLDER_DEPTH, max(MAX_FOLDER_DEPTH, 0))
if MAX_FOLDER_DEPTH == -1:
    MAX_FOLDER_DEPTH = None

DEST_FILE_NAME = validate_input_file_name('Insert output file name: ', DEST_FILE_EXTENSION)

#TITLE = validate_input_string_or_default('Insert title (default %s):' % DEFAULT_TITLE, DEFAULT_TITLE)

GENERATE_TAMPA = validate_input_bool('Generate also TAMPA file? y/n: ', ['y', 'Y'], ['n', 'N'])
# end of user input


# MAIN BODY
SRC_FOLDER = str(Path.joinpath(Path(FLAGS_FOLDER), Path(REL_FOLDER)))

flags = get_flags(SRC_FOLDER, FLAGS_FOLDER, MIN_FOLDER_DEPTH, MAX_FOLDER_DEPTH)
max_flag_width = get_max_flag_width(flags)
(currentX, currentY, column_width) = give_valid_position(0, MAX_HEIGHT, 0, 0)

base_img = PIL.Image.new('RGBA', (MAX_WIDTH, MAX_HEIGHT), color=(255, 255, 255, 255))

print('Parsing the flags...')
for idx, flag in enumerate(flags):
    if flag.is_header:
        print('Current folder: %s' % flag.flag_name)
        img = image_utils.ImageText((800, 600), background=(255, 255, 255, 255))
        text_size = img.write_text_box((0, 0), flag.flag_name, MAX_COLUMN_WIDTH, FONT_FILENAME,
                                 font_size=14, color=(0, 0, 0), place='left',
                                 justify_last_line=False)

        row_height = text_size[1] + MARGIN_TITLE_TOP + MARGIN_TITLE_BOTTOM

        # go to a new column if needed
        (currentX, currentY, column_width) = give_valid_position(currentX, currentY, row_height, column_width)

        delta_text = MARGIN_COLUMN_LEFT
        x_pos_text = currentX + delta_text
        y_pos_text = currentY + MARGIN_TITLE_TOP

        cropped_text = img.image.crop((0, 0, *text_size))
        base_img.paste(cropped_text, (x_pos_text, y_pos_text, x_pos_text + text_size[0], y_pos_text + text_size[1]))

        column_width = max([column_width, delta_text + text_size[0]])

        currentY += row_height
    else:
        # test write
        img = image_utils.ImageText((800, 600), background=(255, 255, 255, 255))

        delta_text = MARGIN_COLUMN_LEFT + max_flag_width + MARGIN_FLAG_RIGHT + MARGIN_TEXT_LEFT # position of text from column

        text_size = img.write_text_box((delta_text, 0), flag.flag_name, MAX_COLUMN_WIDTH - delta_text, FONT_FILENAME,
                            font_size=10, color=(0, 0, 0), place='left',
                            justify_last_line=False)

        flag_rect = flag.get_image_rectangle_size()
        max_element_height = max([flag_rect[1], text_size[1]])
        row_height = max_element_height + MARGIN_TOP

        # go to a new column if needed
        (currentX, currentY, column_width) = give_valid_position(currentX, currentY, row_height, column_width)

        x_temp = currentX + MARGIN_COLUMN_LEFT
        y_temp = currentY + MARGIN_TOP

        x_pos_flag_rect = x_temp
        x_pos_text = x_temp + max_flag_width + MARGIN_FLAG_RIGHT + MARGIN_TEXT_LEFT

        rel_y_pos_flag_rect = int((max_element_height - flag_rect[1]) / 2)
        rel_y_pos_text = int((max_element_height - text_size[1]) / 2)

        y_pos_text = currentY + rel_y_pos_text
        y_pos_flag_rect = currentY + rel_y_pos_flag_rect

        x_pos_flag = x_pos_flag_rect + 1
        y_pos_flag = y_pos_flag_rect + 1
        flag.flag_position = (x_pos_flag, y_pos_flag) # save the flag position. needed for TAMPA coordinates export

        # draw the flag rectangle
        ImageDraw.Draw(base_img).rectangle((x_pos_flag_rect, y_pos_flag_rect, x_pos_flag_rect + flag.flag_size[0], y_pos_flag_rect + flag.flag_size[1]), fill ='white', outline ='black')

        cropped_text = img.image.crop((delta_text, 0, text_size[0] + delta_text, text_size[1]))
        base_img.paste(cropped_text, (x_pos_text, y_pos_text, x_pos_text + text_size[0], y_pos_text + text_size[1]))

        column_width = max([column_width, delta_text + text_size[0]])

        currentY += row_height

base_img.save(DEST_FILE_NAME)


if GENERATE_TAMPA:
    generate_tampa(flags)

print('Done.')