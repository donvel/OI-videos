"""
Ten skrypt jest częścią pakietu narzędzi do automatycznej
obróbki omówień video na OI i PA.

UWAGA: skrypt run_blender.sh nie używa tego pliku, ale jego kopię dołączoną
do pliku make_movie.blend. Zatem po wprowadzeniu zmian w tym pliku należy
zaktualizować również tamtą kopię (używając edytora tekstu w Blenderze).

Zadaniem tego skryptu jest połączenie poszczególnych ujęć oraz
dodanie czołówki, tyłówki, paska z afiliacją i przejść.

Ścieżki do potrzebnych plików oraz parametry (typu długość
przejść, czas wyświetlania paska z afiliacją) konfiguruje
się w pliku config.ini.

Ten skrypt musi zostać wywołany wewnątrz Blendera.
Należy załadować go w projekcie jako blok tekstowy i kliknąć "Run script".
To podejście jest zautomatyzowane przez skrypt run_blender.sh,
wywołuje się je przez
./run_blender.sh id,
gdzie id jest nagłówkiem sekcji zawierającej odpowiednią konfigurację
w pliku config.ini.
Po jego wykonaniu otwiera się gotowy projekt Blendera z widokiem skonfigurowanym
do edycji wideo. Można oglądać go viewporcie, ewentualnie wprowadzać poprawki
w config.ini (kliknięcie "Run script" na nowo tworzy projekt z config.ini)
lub ręcznie (wymaga to pewnej znajomości Blendera). Kiedy projekt jest już
gotowy do renderowania, należy kliknąć "Animation".

Alternatywnie można otworzyć Blendera poleceniem
./blender --python make_movie.py -- id,
ale wtedy samemu trzeba ustawić odpowiedni widok do edytowania wideo.

Wymagania: zainstalowany Blender (ja używałem wersji 2.78c na Linuxie)

Autor: Bartosz Tarnawski
"""

import bpy
import configparser
import glob
import sys

# Get args
if "--" not in sys.argv:
    argv = []  # as if no args are passed
else:
    argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"

config_file = argv[0]
task_name = argv[1]


# Load config file
cp = configparser.ConfigParser()
cp.read(config_file)
config = cp[task_name]


# Clear all old sequence and prepare the sequence_editor
scn = bpy.context.scene
scn.sequence_editor_clear()
scn.sequence_editor_create()
seq = scn.sequence_editor


# Prepare render settings
scn.render.filepath = config['output_path']
scn.render.fps = config.getint('fps')

# https://support.google.com/youtube/answer/1722171?hl=en#
scn.render.image_settings.file_format = 'H264'
scn.render.ffmpeg.format = 'MPEG4'
scn.render.ffmpeg.audio_codec = 'AAC'
scn.render.ffmpeg.video_bitrate = config.getint('video_bitrate')
scn.render.ffmpeg.audio_bitrate = config.getint('audio_bitrate')
scn.render.resolution_x = config.getint('resolution_x')
scn.render.resolution_y = config.getint('resolution_y')


# Prepare video sequence for rendering
frame = 0
clip_num = 1

def add_movie(name_suffix, path, frame, with_sound=True):
    movie_strip = seq.sequences.new_movie('clip_{}'.format(name_suffix),
            path, 1, frame)
    if with_sound:
        sound_strip = seq.sequences.new_sound('sound_{}'.format(name_suffix),
                path, 2, frame)
    return movie_strip.frame_duration


# INTRO
frame += add_movie('intro', config['intro_path'], frame, with_sound=False)


# AFFILIATION
image_strip = seq.sequences.new_image(
        'affiliation',
        config['affiliation_path'],
        3,
        frame + config.getint('affiliation_start'))
image_strip.frame_final_duration = config.getint('affiliation_duration')
image_strip.blend_type = 'OVER_DROP'


# MOVIE CLIPS
for movie_file in sorted(glob.glob('{}/*.mp4'.format(config['clips_dir']))):
    frame += add_movie(clip_num, movie_file, frame)
    clip_num += 1


# OUTRO
frame += add_movie('outro', config['outro_path'], frame, with_sound=False)

scn.frame_end = frame


# add transitions

def fade_movie_strip(strip, fade_duration):
    scn.frame_current = strip.frame_final_start
    strip.blend_alpha = 0
    strip.keyframe_insert('blend_alpha')
    scn.frame_current += fade_duration
    strip.blend_alpha = 1.0
    strip.keyframe_insert('blend_alpha')
    scn.frame_current = strip.frame_final_end - fade_duration
    strip.blend_alpha = 1.0
    strip.keyframe_insert('blend_alpha')
    scn.frame_current = strip.frame_final_end
    strip.blend_alpha = 0
    strip.keyframe_insert('blend_alpha')


def fade_sound_strip(strip, fade_duration):
    scn.frame_current = strip.frame_final_start
    strip.volume = 0
    strip.keyframe_insert('volume')
    scn.frame_current += fade_duration
    strip.volume = 1.0
    strip.keyframe_insert('volume')
    scn.frame_current = strip.frame_final_end - fade_duration
    strip.volume = 1.0
    strip.keyframe_insert('volume')
    scn.frame_current = strip.frame_final_end
    strip.volume = 0
    strip.keyframe_insert('volume')


for strip in seq.sequences:
    if strip.type == 'SOUND':
        fade_sound_strip(strip, config.getint('fade_duration'))
    elif strip.type == 'MOVIE':
        fade_movie_strip(strip, config.getint('fade_duration'))
    elif strip.type == 'IMAGE':
        fade_movie_strip(strip, config.getint('affiliation_fade_duration'))
