#!/usr/bin/env python3
"""Radio pack tool for GTA: Chinatown Wars 4.4.243 (Android). Converts audio files into the radio/ folder that the
"Load texture and radio packs" patch loads from Android/data/com.rockstargames.gtactw/files/radio/.

  make_radio.py IN_DIR OUT_DIR [--names PRESET_OR_FILE]

IN_DIR holds one audio file per station, named after the game's station file (any format ffmpeg reads, including the
PSP's ATRAC3plus .AT3): radio1 radio2 radio3 radio4 radio5 khalil tortoise wonderwheel anvil chinese dfa
(toth = wonderwheel, as the PSP version calls Turntables on the Hudson). Stations without a file keep the game's.

Every file becomes what the game's MP3 streamer expects: mono, 44.1 kHz, 96 kbps CBR, with no ID3 tag in front
(the game reads the first MP3 frame from byte 0; a tag there plays as static).

--names writes radio/names.txt, the station names shown in the game: a file of "station=Name" lines or a preset
(gta4-psp-part1, gta4-psp-part2: the two parts of the GTA IV radio mod for the PSP version by AshleyVT92).
Anvil, Sinowav FM (chinese) and DFA have no text name in the game, only a logo; logos are not changed.
"""
import os, shutil, subprocess, sys

STATIONS = ['radio1', 'radio2', 'radio3', 'radio4', 'radio5', 'khalil', 'tortoise', 'wonderwheel', 'anvil',
            'chinese', 'dfa']
ALIASES = {'toth': 'wonderwheel'}
GXT = {'radio1': 0xe0, 'radio2': 0xe1, 'radio3': 0xe2, 'radio4': 0xe3, 'radio5': 0xe4,  # E_MAIN.gxt entries
       'khalil': 0xe7, 'tortoise': 0xe8, 'wonderwheel': 0xe9}
PRESETS = {  # stations identified from their jingles and DJ breaks
    'gta4-psp-part1': {'radio1': 'Vladivostok FM', 'radio2': 'Public Liberty Radio', 'radio3': 'San Juan Sounds',
                       'radio4': 'Electro-Choc', 'radio5': 'The Classics 104.1', 'khalil': 'IF99',
                       'tortoise': 'Tuff Gong Radio', 'wonderwheel': 'Integrity 2.0'},
    'gta4-psp-part2': {'radio1': 'Massive B Soundsystem', 'radio2': 'K109 The Studio', 'radio3': 'Self-Actualization FM',
                       'radio4': 'WKTT Talk Radio', 'radio5': 'Vice City FM', 'khalil': 'Liberty City Hardcore',
                       'tortoise': 'The Journey', 'wonderwheel': 'Fusion FM'},
}


def names_from(arg):
    if arg in PRESETS:
        return PRESETS[arg]
    out = {}
    for line in open(arg, encoding='utf-8'):
        if '=' in line:
            k, v = line.split('=', 1)
            out[ALIASES.get(k.strip().lower(), k.strip().lower())] = v.strip()
    return out


def main(argv):
    if len(argv) < 2 or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 1
    src, dst = argv[0], argv[1]
    names = names_from(argv[argv.index('--names') + 1]) if '--names' in argv else None
    if not shutil.which('ffmpeg'):
        sys.exit('ffmpeg is needed: https://ffmpeg.org/download.html')
    os.makedirs(dst, exist_ok=True)
    done = []
    for f in sorted(os.listdir(src)):
        stem = os.path.splitext(f)[0].lower()
        st = ALIASES.get(stem, stem)
        if st not in STATIONS:
            continue
        out = os.path.join(dst, st + '.mp3')
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', os.path.join(src, f), '-vn', '-ac', '1',
                        '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '96k', '-map_metadata', '-1',
                        '-id3v2_version', '0', '-write_id3v1', '0', out], check=True)
        with open(out, 'rb') as m:
            assert m.read(3) != b'ID3', out  # the game would play a leading tag as static
        done.append(st)
        print(f'{f} -> {out}')
    if names:
        with open(os.path.join(dst, 'names.txt'), 'w', encoding='utf-8') as n:
            for st, i in GXT.items():
                if st in names:
                    n.write(f'{hex(i)}={names[st]}\n')
        print('names.txt written')
    missing = [s for s in STATIONS if s not in done]
    if missing:
        print('kept the game\'s own: ' + ', '.join(missing))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
