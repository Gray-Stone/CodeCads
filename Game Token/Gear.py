import build123d as bd
from build123d import Mode as bdMode

import ocp_vscode


height = 5
radious = 15
layers = 5
starting_edge_width = 2
per_layer_width_reduction = 0.8 # factor to reduct with
rotate_angle = 15

with bd.BuildPart() as hexcoin1:
    with bd.BuildSketch() as hexcoin_sk:
        current_hex_radious = radious
        current_edge_width = starting_edge_width
        current_ratation = 0
        for i in range(layers):
            print(f"radious {current_hex_radious}, line-width {current_edge_width}")
            some_hex = bd.RegularPolygon(current_hex_radious,6, rotation=current_ratation)
            bd.offset(some_hex,amount=-current_edge_width,mode=bd.Mode.SUBTRACT)
            
            # prep size for next iteration
            current_hex_radious = current_hex_radious - current_edge_width -0.5
            current_edge_width = current_edge_width * per_layer_width_reduction
            current_ratation += rotate_angle


        # inner_hex =  bd.RegularPolygon(7,6,rotation=15, mode=bdMode.SUBTRACT)
        # inner_hex =  bd.RegularPolygon(7.8,6,rotation=rotate_angle)
        # bd.offset(inner_hex,amount=-1.6,mode=bd.Mode.SUBTRACT)
        
        # hex_3 =  bd.RegularPolygon(5.8,6,rotation=rotate_angle*2)
        # bd.offset(hex_3,amount=-1,mode=bd.Mode.SUBTRACT)

        # hex_4 =  bd.RegularPolygon(4.8,6,rotation=rotate_angle*3)
        # bd.offset(hex_4,amount=-0.8,mode=bd.Mode.SUBTRACT)
    bd.extrude(amount= 5)
    all_faces =    hexcoin1.faces().filter_by(bd.Axis.Z , reverse=True).sort_by(bd.SortBy.AREA,reverse=True)
    for face in all_faces[0:6]:
        with bd.BuildSketch(face) as cut_text:
            bd.Text("5",font_size=5)
        bd.extrude(cut_text.sketch,amount=-0.2,mode=bdMode.SUBTRACT)
    









# from ocp_vscode import show, show_object, reset_show, set_port, set_defaults, get_defaults
# set_port(3939)


# ocp_vscode.set_defaults(reset_camera=ocp_vscode.Camera.KEEP)

# ocp_vscode.show_all()
# ocp_vscode.show_object(hexcoin)
# ocp_vscode.show_object(hexcoin_sk , reset_camera=ocp_vscode.Camera.KEEP)
ocp_vscode.show_object(hexcoin1 , reset_camera=ocp_vscode.Camera.KEEP)
