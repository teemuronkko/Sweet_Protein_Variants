reinit
set grid_mode, 1
bg_color white
set cartoon_loop_radius, 0.3
set cartoon_fancy_helices, 0
set cartoon_fancy_sheets, 0
set cartoon_oval_length, 1.0
set cartoon_oval_width, 0.25
set cartoon_rect_width, 0.25
set cartoon_rect_length, 1.5
set cartoon_rect_length, 1.5
fetch 4HE7, Brazzein_disulfide_object
set grid_slot, 1, Brazzein_disulfide_object
hide everything, Brazzein_disulfide_object
show cartoon, Brazzein_disulfide_object and chain A
color grey80, Brazzein_disulfide_object
set cartoon_transparency, 0.2, Brazzein_disulfide_object
select Brazzein_disulfide, Brazzein_disulfide_object and resi 34+33+7+8+13+51+46+21+11+54+45+12+32+15
set cartoon_transparency, 0, Brazzein_disulfide
set_color disulfide_color, [170,49,122]
color disulfide_color, Brazzein_disulfide


distance 8_11_bond, /Brazzein_disulfide_object//A/8/CA, /Brazzein_disulfide_object//A/11/CA
set dash_width, 4, 8_11_bond
set dash_color, disulfide_color, 8_11_bond
set dash_gap, 0.4, 8_11_bond
set grid_slot, 1, 8_11_bond
hide labels, 8_11_bond
distance 32_51_bond, /Brazzein_disulfide_object//A/32/CA, /Brazzein_disulfide_object//A/51/CA
set dash_width, 4, 32_51_bond
set dash_color, disulfide_color, 32_51_bond
set dash_gap, 0.4, 32_51_bond
set grid_slot, 1, 32_51_bond
hide labels, 32_51_bond
distance 15_21_bond, /Brazzein_disulfide_object//A/15/CA, /Brazzein_disulfide_object//A/21/CA
set dash_width, 4, 15_21_bond
set dash_color, disulfide_color, 15_21_bond
set dash_gap, 0.4, 15_21_bond
set grid_slot, 1, 15_21_bond
hide labels, 15_21_bond
distance 13_45_bond, /Brazzein_disulfide_object//A/13/CA, /Brazzein_disulfide_object//A/45/CA
set dash_width, 4, 13_45_bond
set dash_color, disulfide_color, 13_45_bond
set dash_gap, 0.4, 13_45_bond
set grid_slot, 1, 13_45_bond
hide labels, 13_45_bond
distance 33_54_bond, /Brazzein_disulfide_object//A/33/CA, /Brazzein_disulfide_object//A/54/CA
set dash_width, 4, 33_54_bond
set dash_color, disulfide_color, 33_54_bond
set dash_gap, 0.4, 33_54_bond
set grid_slot, 1, 33_54_bond
hide labels, 33_54_bond
distance 7_46_bond, /Brazzein_disulfide_object//A/7/CA, /Brazzein_disulfide_object//A/46/CA
set dash_width, 4, 7_46_bond
set dash_color, disulfide_color, 7_46_bond
set dash_gap, 0.4, 7_46_bond
set grid_slot, 1, 7_46_bond
hide labels, 7_46_bond
distance 12_15_bond, /Brazzein_disulfide_object//A/12/CA, /Brazzein_disulfide_object//A/15/CA
set dash_width, 4, 12_15_bond
set dash_color, disulfide_color, 12_15_bond
set dash_gap, 0.4, 12_15_bond
set grid_slot, 1, 12_15_bond
hide labels, 12_15_bond
distance 34_54_bond, /Brazzein_disulfide_object//A/34/CA, /Brazzein_disulfide_object//A/54/CA
set dash_width, 4, 34_54_bond
set dash_color, disulfide_color, 34_54_bond
set dash_gap, 0.4, 34_54_bond
set grid_slot, 1, 34_54_bond
hide labels, 34_54_bond
fetch 4HE7, Brazzein_object_2
set grid_slot, 2, Brazzein_object_2
hide everything, Brazzein_object_2
show cartoon, Brazzein_object_2 and chain A
color grey80, Brazzein_object_2
set cartoon_transparency, 0.2, Brazzein_object_2
select Brazzein_rosetta, Brazzein_object_2 and resi 5+31+19+8+13+35+11
set cartoon_transparency, 0.0, Brazzein_rosetta
set_color rosetta_color, [244,131,108]
color rosetta_color, Brazzein_rosetta
deselect
select Brazzein_bibliography, Brazzein_object_2 and resi 50
set cartoon_transparency, 0.0, Brazzein_bibliography
set_color bibliography_color, [248,158,68]
color bibliography_color, Brazzein_bibliography
deselect
alignto Brazzein_object_2
center
orient
