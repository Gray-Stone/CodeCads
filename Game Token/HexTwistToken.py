#!/usr/bin/env python
import build123d as bd
import ocp_vscode
from build123d import Mode as bdMode

THICKNESS = 7
HEIGHT = 5
RADIOUS = 20
LAYERS = 3
STARTING_EDGE_WIDTH = 4.5
STARTING_GAP_WIDTH = 0.7
PER_LAYER_WIDTH_REDUCTION = 0.7  # factor to reduct with
EDGE_ROTATE_ANGLE = 10
GAP_ROTATION_ANGLE = 8
with bd.BuildPart() as hexcoin1:
    # Make the base coin first, this makes chamfer easier
    current_hex_radious = RADIOUS
    current_rotation = 0
    current_edge_width = STARTING_EDGE_WIDTH
    # Have a base hex to start
    with bd.BuildSketch():
        bd.RegularPolygon(current_hex_radious, 6, rotation=current_rotation)

        current_hex_radious -= current_edge_width
        current_rotation += GAP_ROTATION_ANGLE
        bd.RegularPolygon(current_hex_radious,
                          6,
                          rotation=current_rotation,
                          mode=bdMode.SUBTRACT)
    bd.extrude(amount=THICKNESS)

    # Pick out the outter edges and faces first
    outter_hex_edges = hexcoin1.edges().filter_by(
        bd.Axis.Z, reverse=True).sort_by(bd.SortBy.DISTANCE, reverse=True)[0:12]

    outter_faces = hexcoin1.faces().filter_by(bd.Axis.Z, reverse=True).sort_by(
        bd.SortBy.AREA, reverse=True)[0:6]

    # ocp_vscode.show_object(outter_hex_edges ) # debug

    current_gap_width = STARTING_GAP_WIDTH

    with bd.BuildSketch():
        for i in range(LAYERS):
            current_edge_width *= PER_LAYER_WIDTH_REDUCTION
            current_rotation += EDGE_ROTATE_ANGLE

            current_gap_width *= PER_LAYER_WIDTH_REDUCTION
            current_hex_radious -= current_gap_width
            bd.RegularPolygon(current_hex_radious, 6, rotation=current_rotation)

            current_hex_radious -= current_edge_width
            current_rotation += GAP_ROTATION_ANGLE

            bd.RegularPolygon(current_hex_radious,
                              6,
                              rotation=current_rotation,
                              mode=bdMode.SUBTRACT)

    bd.extrude(amount=THICKNESS)

    # Actually do the chamfer and write letters
    bd.chamfer(outter_hex_edges, 1)

    for face in outter_faces:
        with bd.BuildSketch(face) as cut_text:
            bd.Text("5", font_size=5.5)
        bd.extrude(cut_text.sketch, amount=-0.6, mode=bdMode.SUBTRACT)

# hexcoin1.part.export_3mf(file_name="Gear.3mf",
#                     tolerance=0.001,
#                     angular_tolerance=0.1,
#                     unit=bd.Unit.MM)

hexcoin1.part.export_step("token.step")

# from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
# set_port(3939)

# ocp_vscode.set_defaults(reset_camera=ocp_vscode.Camera.KEEP)

# ocp_vscode.show_all()
# ocp_vscode.show_object(hexcoin)
# ocp_vscode.show_object(hexcoin_sk , reset_camera=ocp_vscode.Camera.KEEP)
ocp_vscode.show_object(hexcoin1, reset_camera=ocp_vscode.Camera.KEEP)
