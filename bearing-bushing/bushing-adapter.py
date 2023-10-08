#!/usr/bin/env python
import build123d as bd
import ocp_vscode
from build123d import Mode as bdMode
ocp_vscode.set_defaults(reset_camera=ocp_vscode.Camera.KEEP)

# https://www.prusa3d.com/product/linear-bearing-lm8uu/
LM8UU_OD = 16
LM8UU_LENGTH = 22

# https://us.misumi-ec.com/vona2/detail/110302289820/?HissuCode=MPBP8-15
BUSHING_OD = 12
BUSHING_LENGTH = 15
BRIM_AMOUNT = 1
BRIM_LENGTH = 2

PADDED_LENGTH = LM8UU_LENGTH -2 - BRIM_AMOUNT

HEX_CUT_SIZE = 2.5

with bd.BuildPart() as sleeve:
    # Make the base coin first, this makes chamfer easier

    with bd.BuildSketch(bd.Plane.XY) as sleeve_sk:
        
        bd.Circle(LM8UU_OD/2)
        bd.Circle(BUSHING_OD/2 , mode=bdMode.SUBTRACT)

    # ocp_vscode.show_object(sleeve_sk, reset_camera=ocp_vscode.Camera.KEEP)
    bd.extrude(sleeve_sk.sketch , amount=PADDED_LENGTH)

    # ocp_vscode.show_object( )
    with bd.BuildSketch(bd.Plane.XY) as sleeve_brim:
        bd.Circle(LM8UU_OD/2)

        bd.Circle(BUSHING_OD/2 - BRIM_AMOUNT,mode=bdMode.SUBTRACT )
    bd.extrude(sleeve_brim.sketch , amount= BRIM_LENGTH , dir=(0,0,-1),mode=bdMode.ADD)


    # Small cuts in brim to help push the bushing back out if needed. 
    top_surface = sleeve.faces().filter_by(bd.Axis.Z).sort_by(bd.Axis.Z)[0]
    # ocp_vscode.show_object(top_surface,reset_camera=ocp_vscode.Camera.KEEP )
    with bd.BuildSketch(-top_surface) as notch_cut:
        bd.Rectangle(2,BUSHING_OD+1 )
    bd.extrude(notch_cut.sketch , amount=BRIM_LENGTH , mode=bdMode.SUBTRACT)


    
    # HEX cutouts on the side
    single_hex_planes = [bd.Plane.XZ , bd.Plane.YZ]
    
    for plane in single_hex_planes:

        with bd.BuildSketch(plane) as hex_cut :
            # Note: The cord inside a sketch is not global cord, so offset in Z of global cord becomes offset in Y 
            with bd.Locations((0,PADDED_LENGTH/2-1) , (0,PADDED_LENGTH)):
                hex_sk = bd.RegularPolygon(radius=HEX_CUT_SIZE,side_count=6,rotation=30)
        # ocp_vscode.show_object(hex_cut,reset_camera=ocp_vscode.Camera.KEEP)

        bd.extrude(hex_cut.sketch, amount=20 ,both=True , mode=bdMode.SUBTRACT)

    double_hex_planes = [bd.Plane.XZ.rotated((0,0,45)) , bd.Plane.YZ.rotated((0,0,45))]

    for plane in double_hex_planes:

        with bd.BuildSketch( plane ) as hex_cut2 :
            # Note: The cord inside a sketch is not global cord, so offset in Z of global cord becomes offset in Y 
            with bd.Locations((0,PADDED_LENGTH/4-2) , (0,PADDED_LENGTH/4*3)):
                hex_sk = bd.RegularPolygon(radius= HEX_CUT_SIZE ,side_count=6,rotation=30)
        # ocp_vscode.show_object(hex_cut,reset_camera=ocp_vscode.Camera.KEEP)
        
        bd.extrude(hex_cut2.sketch, amount=20 ,both=True , mode=bdMode.SUBTRACT)



# ocp_vscode.show_all(reset_camera=ocp_vscode.Camera.KEEP)
ocp_vscode.show_object(sleeve, reset_camera=ocp_vscode.Camera.KEEP)

import pathlib


# current_path = pathlib.Path(__file__).parent.resolve()

# print(f"Outputing to {current_path/'token.step'}")

# hexcoin1.part.export_step(str(current_path/"token.step"))
out_folder = pathlib.Path("/home/leogray/Downloads/Prints").resolve()
print(f"Outputing to {out_folder/'sleeve_adaptor.step'}")
sleeve.part.export_step(str(out_folder/"sleeve_adaptor.step"))


sleeve.part.export_3mf(file_name=str(out_folder/"Sleeve_adapter.3mf"),
                    tolerance=0.0001,
                    angular_tolerance=0.01,
                    unit=bd.Unit.MM)


