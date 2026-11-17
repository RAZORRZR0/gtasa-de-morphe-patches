# GTA: Chinatown Wars packs

The *Load texture and radio packs* patch loads these files from
`Android/data/com.rockstargames.gtactw/files/` each time the game starts. Copy them there with a file manager or a
PC (USB, MTP), then restart the game. Remove or rename a file to go back to the game's own.

| File | What it replaces | Made with |
|---|---|---|
| `DXT.bin` | The 3D world's texture sheets (buildings, signs; 107 entries of the game's `assets/dxt.bin`) | `ctwtex.py build` |
| `CTWHD.bin` | 2D art kept in `assets/game.pak`: cutscene panels, character portraits, menus (1,379 PNG textures) | `ctwtex.py sidecar` |
| `radio/<station>.mp3` | Radio stations (`radio1` … `radio5`, `khalil`, `tortoise`, `wonderwheel`, `anvil`, `chinese`, `dfa`) | `make_radio.py` |
| `radio/names.txt` | Station names shown in the game | `make_radio.py --names` |

No packs are published with the patches: they are made from the game's own files (textures) or from other people's
mods (radio), so you make them yourself from your own copies with the tools here.

## Textures: make an HD pack

Needs Python 3 with `pip install numpy pillow`, and an AI upscaler (any that writes PNGs).

1. Get `assets/game.pak` and `assets/dxt.bin` out of the game's APK (it is a zip file).
2. Extract the textures:
   ```sh
   python3 ctwtex.py extract-dxt dxt.bin sheets/        # 3D world sheets, 1024x1024
   python3 ctwtex.py extract game.pak flat/             # 2D textures + flat/index.json
   ```
3. Upscale `sheets/` and `flat/` into `sheets_hd/` and `flat_hd/`, keeping the file names (`<id>.png`). Any size
   works; 2x is the sweet spot for phones. What we used and recommend:
   - Sheets: [1x DXTDecompressor Source V3](https://openmodeldb.info/models/1x-DXTDecompressor-Source-V3) first (removes
     the DXT1 block artifacts the sheets are stored with), then
     [4x-UltraSharpV2](https://huggingface.co/Kim2091/UltraSharpV2), then downscale to 2048x2048.
   - 2D art: 4x-UltraSharpV2, then downscale to 2x the original size.
   - Real-ESRGAN invents brick-like detail and smears text on these sheets; avoid it.
   - No GPU? A free Kaggle notebook (2x T4) runs the 1,379 2D textures in about 5 hours and the sheets in about 1.
4. Pack them:
   ```sh
   python3 ctwtex.py build dxt.bin sheets_hd/ DXT.bin           # ~200 MB at 2048x2048
   python3 ctwtex.py sidecar flat/index.json flat_hd/ CTWHD.bin  # ~730 MB at 2x
   ```

`sidecar` skips the raw textures (radar map tiles, sprite sheets): the game reads those pixel by pixel, and bigger
ones break the radar. `build` re-encodes the sheets as DXT1/DXT5; the game converts them to its GPU's format itself.

## Radio: replace the stations

Needs Python 3 and [ffmpeg](https://ffmpeg.org/download.html) (it also reads the PSP's ATRAC3plus `.AT3`).

```sh
python3 make_radio.py IN_DIR radio/ --names gta4-psp-part1
```

`IN_DIR` holds one audio file per station, named after the game's station files listed above (`toth` also works for
`wonderwheel`). Each becomes a mono 44.1 kHz 96 kbps MP3 without an ID3 tag: the game reads MP3 frames from the first
byte, so a tag at the start plays as static. Stations can be hours long; the game streams them.

The `gta4-psp-part1` and `gta4-psp-part2` name presets match the two parts of the
**GTA IV radio mod for the PSP version by [AshleyVT92](https://www.youtube.com/@AshleyVT92)**: point `IN_DIR` at that
mod's `PSP_GAME/USRDIR/WAD/` folder. Or write your own `names.txt` with `station=Name` lines. Anvil, Sinowav FM
(`chinese`) and DFA have no text name in the game, only a logo, and the logos are not changed.

To switch between two radio sets, keep the other one in a folder with another name (for example `radio_part2`) and
swap the folder names.

## Formats

See the comments at the top of `ctwtex.py` (`game.pak`, `dxt.bin`, `CTWHD.bin`) and
`native/ctw/ctwpacks/main.cpp` (how the game loads them).
