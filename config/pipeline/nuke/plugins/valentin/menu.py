# ------ Add PluginPaths to tools and icons
nuke.pluginAddPath("./gizmos")
nuke.pluginAddPath("./python")
nuke.pluginAddPath("./icons")

# ----- Load gizmos
toolbar = nuke.menu("Nodes")
valentinMenu = toolbar.addMenu("Valentin", icon="valentin_icon.svg")
valentinMenu.addCommand("Expoglow", lambda: nuke.createNode("expoglow.gizmo"))
valentinMenu.addCommand("Atmosphere", lambda: nuke.createNode("atmosphere.gizmo"))
valentinMenu.addCommand(
    "Firefly Killer", lambda: nuke.createNode("firefly_killer.gizmo")
)
valentinMenu.addCommand("X Denoise", lambda: nuke.createNode("x_denoise.gizmo"))
valentinMenu.addCommand(
    "Chromatic Aberration", lambda: nuke.createNode("fxt_chromaticaberration.gizmo")
)
valentinMenu.addCommand(
    "Heat Distorsion", lambda: nuke.createNode("t_heatdistortion.gizmo")
)
valentinMenu.addCommand(
    "Lens/Virtual Lens", lambda: nuke.createNode("virtual_lens.gizmo")
)
valentinMenu.addCommand(
    "Lens/Lens Engine", lambda: nuke.createNode("lens_engine.gizmo")
)
valentinMenu.addCommand(
    "Lens/Flare Factory", lambda: nuke.createNode("flare_factory.gizmo")
)
