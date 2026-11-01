package gtade.patches

import app.morphe.patcher.patch.rawResourcePatch

@Suppress("unused")
val modMenuPatch = rawResourcePatch(
    name = "ModMenu",
    description = "In-game settings menu for the other mods.",
    default = true,
) {
    compatibleWith(GTASA_DE)
    dependsOn(modLoaderPatch)
    execute { addMod("libmodmenu.so", "modmenu.ini") }
}

@Suppress("unused")
val propFixPatch = rawResourcePatch(
    name = "GTA Prop Fix",
    description = "Restores map props missing from the Definitive Edition.",
    default = true,
) {
    compatibleWith(GTASA_DE)
    dependsOn(modLoaderPatch)
    execute { addMod("libpropfix.so", "GTA_Prop_Fix.ini") }
}

@Suppress("unused")
val skyGfxPatch = rawResourcePatch(
    name = "SkyGfx",
    description = "PS2-style graphics: PS2 timecyc, radiosity, distant lamp coronas, post effects.",
    default = true,
) {
    compatibleWith(GTASA_DE)
    dependsOn(modLoaderPatch)
    execute { addMod("libskygfx.so", "SkyGfx.ini", "SALodLights.dat", "timecyc_ps2.dat") }
}

@Suppress("unused")
val projectPropsPatch = rawResourcePatch(
    name = "Project Props",
    description = "Project Props 4: about 16,000 extra map props. Downloads the Project Props placements " +
        "from github.com/user-grinch/Project-Props while patching (needs internet).",
    default = true,
) {
    compatibleWith(GTASA_DE)
    dependsOn(modLoaderPatch)
    execute {
        addMod("libprojectpropsde.so", "ProjectPropsDE.ini")
        val dat = ProjectPropsData.build(String(bundled("ProjectPropsDE.stock"), Charsets.UTF_8))
        get("assets/gtade/configs/ProjectPropsDE.dat", false).writeText(dat)
    }
}
