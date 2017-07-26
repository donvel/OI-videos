# Ten skrypt jest cześcią pakietu narzędzi do automatycznej
# obróbki omówień video na OI i PA.
# Autor: Bartosz Tarnawski
CONFIG_FILE=/home/bartek/Dropbox/PA16/video_scripts/config.ini
BLENDER_EXEC=/home/bartek/Programs/blender-2.78c-linux-glibc219-x86_64/blender
BLENDER_FILE=/home/bartek/Dropbox/PA16/video_scripts/make_movie.blend
SCRIPT_TEXT_BLOCK=make_movie.py
$BLENDER_EXEC $BLENDER_FILE --python-text $SCRIPT_TEXT_BLOCK -- $CONFIG_FILE $1
