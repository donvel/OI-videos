#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Ten skrypt jest częścią pakietu narzędzi do automatycznej
obróbki omówień video na OI i PA.

Jego zadaniem jest wycięcie i przekonwertowanie kadrów do
dalszej obróbki z całości materiałów zgranych z kamery.
Kadry są wybierane na podstawie przygotowanego pliku
tekstowego z "minutkami". Taki plik składa się z linii
pasujących do wyrażenia regularnego
(\w+.\w+) (\d+):(\d+) (\d+):(\d+) (\w+)$
o następującym znaczeniu:
(nazwa pliku wideo) 
(minuta):(sekunda początku ujęcia)
(minuta):(sekunda końca ujęcia)
(opis ujęcia)
np. 
00341.MTS 00:01 01:26 tresc_zadania

Generowane pliki wideo są w formacie zgodnym
z zaleceniami YouTube, patrz:
https://www.virag.si/2015/06/encoding-videos-for-youtube-with-ffmpeg/
https://support.google.com/youtube/answer/1722171?hl=en#

Pliki trzeba jeszcze połączyć, dodać czołówkę, tyłówkę,
pasek z afiliacją i przejścia.
Można to zrobić np. za pomocą Blendera i skryptu make_movie.py.

Wymagania: zainstalowany ffmpeg (ja używałem wersji 3.2.5-1)

Autor: Bartosz Tarnawski
"""

import argparse
import codecs
import re
import subprocess


regex_line = '(\w+.\w+) (\d+):(\d+) (\d+):(\d+) (\w+)$'
constr = [str, int, int, int, int, str]

# Taken from:
# https://www.virag.si/2015/06/encoding-videos-for-youtube-with-ffmpeg/
ffmpeg_line = 'ffmpeg -i {input_path} -ss {start_t} -t {duration} \
-codec:v libx264 -crf 21 -bf 2 -flags +cgop -pix_fmt yuv420p \
-codec:a aac -strict -2 -b:a 384k -r:a 48000 \
-movflags faststart \
{output_path}'


def get_args():
    parser = argparse.ArgumentParser(
        description="Program do wycinania kadrów z pliku video")
    parser.add_argument('video_dir',
        help="folder ze wszystkimi plikami video opisanymi w times_file")
    parser.add_argument('times_file',
        help="plik z czasam fragmentów w formacie '{}'".format(regex_line))
    parser.add_argument('output_dir',
        help="nazwa folderu, w którym mają znaleźć się wycięte fragmenty")
    parser.add_argument('--show', action='store_true', dest='show_only',
        help="tylko wypisuje polecenia do wykonania")

    return parser.parse_args()


args = get_args()
commands = ['mkdir -p {}'.format(args.output_dir)]
num = 1

with open(args.times_file) as clip_times:
    for line in clip_times:
        words = re.search(regex_line, line)
        [input_movie, start_m, start_s, end_m, end_s, fname] = \
                [f(gr) for (f, gr) in zip(constr, words.groups())]
        start_t = 60 * start_m + start_s
        end_t = 60 * end_m + end_s
        input_path = '{}/{}'.format(args.video_dir, input_movie)
        duration = end_t - start_t
        output_path = '{}/{:02d}_{}.mp4'.format(args.output_dir, num, fname)
        command = ffmpeg_line.format(
                input_path=input_path,
                start_t=start_t,
                duration=duration,
                output_path=output_path)
        commands += [command]
        num += 1

for c in commands:
    print(c)
    if not args.show_only:
        subprocess.call(c, shell=True)
