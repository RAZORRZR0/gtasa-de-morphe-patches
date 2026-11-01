# GTA SA DE Mods: Morphe patches

[Morphe](https://morphe.software) patches that add the AML mod loader and PC mod ports to
**GTA: San Andreas – Definitive Edition** for Android (`com.rockstargames.gtasa.de` **1.87.0**, arm64).
No PC and no root needed. The mods are built in
[GTASA-DE-Android-ModLoader](https://github.com/RAZORRZR0/GTASA-DE-Android-ModLoader).

## Use

1. In Morphe Manager add this patch source: `https://github.com/RAZORRZR0/gtasa-de-morphe-patches`
   ([add](https://morphe.software/add-source?github=RAZORRZR0/gtasa-de-morphe-patches)).
2. Select GTA: SA 1.87.0, tick the mods, patch, install.
   **The first install replaces the Play Store game, which deletes its saves on the phone**: keep them in
   Rockstar's cloud save or back them up first. Later re-patches are updates and keep them.
3. To add or remove mods, patch again with a different selection. Settings are in the game (ModMenu); a mod's
   `.ini` is only written when it does not exist yet, so re-patching keeps them.

<!-- PATCHES_START EXPANDED -->
<!-- PATCHES_END -->

Project Props downloads its placements from [user-grinch/Project-Props](https://github.com/user-grinch/Project-Props) while patching (pinned commit, needs internet) and builds `ProjectPropsDE.dat` like the mod repo's `build_props.py`, so this patches file ships none of them.

## How it works

- Every mod patch depends on the hidden **mod loader** patch: it adds `lib/arm64-v8a/libAML.so` and the
  `gtade.boot.Boot` extension, and calls `Boot.start()` in `GameActivity`'s static init right after
  `loadLibrary("UE4")`.
- Mod patches put their library in `assets/gtade/mods/` and their config/data files in `assets/gtade/configs/`.
- At the first start after a (re)patch, `Boot` copies them to `Android/data/com.rockstargames.gtasa.de/{mods,configs}`
  (an existing `.ini` is kept), deletes mod libraries of the previous patch that are no longer included, then loads
  AML, which loads the mods. Logcat tag `GTADEBoot`.

## Build

```sh
./sync-mods.sh <path to GTASA-DE-Android-ModLoader>   # after its loader/build_aml_arm64.sh and mods/build.sh
GITHUB_ACTOR=<user> GITHUB_TOKEN=<token with read:packages> ./gradlew buildAndroid
# -> patches/build/libs/patches-<version>.mpp
```

Test on a PC with [Morphe Desktop](https://github.com/MorpheApp/morphe-desktop):
`java -jar morphe-desktop-<v>-all.jar patch -p patches/build/libs/patches-<v>.mpp <game.apk>`.

## License

GPLv3 (see `LICENSE`). Bundled: AML (RusJJ, MIT) and the mods from the mod loader repo (MIT).
