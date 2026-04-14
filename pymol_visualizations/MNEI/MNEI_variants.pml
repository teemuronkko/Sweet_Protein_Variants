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
fetch 1IV7, MNEI_disulfide_object
set grid_slot, 1, MNEI_disulfide_object
hide everything, MNEI_disulfide_object
show cartoon, MNEI_disulfide_object and chain A
color grey80, MNEI_disulfide_object
set cartoon_transparency, 0.2, MNEI_disulfide_object
select MNEI_disulfide, MNEI_disulfide_object and resi 34+43+19+8+54+44+22+66+1+20+23+86+6+48+56+12+17+73+89+32
set cartoon_transparency, 0, MNEI_disulfide
set_color disulfide_color, [170,49,122]
color disulfide_color, MNEI_disulfide


distance 8_12_bond, /MNEI_disulfide_object//A/8/CA, /MNEI_disulfide_object//A/12/CA
set dash_width, 4, 8_12_bond
set dash_color, disulfide_color, 8_12_bond
set dash_gap, 0.4, 8_12_bond
set grid_slot, 1, 8_12_bond
hide labels, 8_12_bond
distance 17_34_bond, /MNEI_disulfide_object//A/17/CA, /MNEI_disulfide_object//A/34/CA
set dash_width, 4, 17_34_bond
set dash_color, disulfide_color, 17_34_bond
set dash_gap, 0.4, 17_34_bond
set grid_slot, 1, 17_34_bond
hide labels, 17_34_bond
distance 23_89_bond, /MNEI_disulfide_object//A/23/CA, /MNEI_disulfide_object//A/89/CA
set dash_width, 4, 23_89_bond
set dash_color, disulfide_color, 23_89_bond
set dash_gap, 0.4, 23_89_bond
set grid_slot, 1, 23_89_bond
hide labels, 23_89_bond
distance 6_43_bond, /MNEI_disulfide_object//A/6/CA, /MNEI_disulfide_object//A/43/CA
set dash_width, 4, 6_43_bond
set dash_color, disulfide_color, 6_43_bond
set dash_gap, 0.4, 6_43_bond
set grid_slot, 1, 6_43_bond
hide labels, 6_43_bond
distance 19_73_bond, /MNEI_disulfide_object//A/19/CA, /MNEI_disulfide_object//A/73/CA
set dash_width, 4, 19_73_bond
set dash_color, disulfide_color, 19_73_bond
set dash_gap, 0.4, 19_73_bond
set grid_slot, 1, 19_73_bond
hide labels, 19_73_bond
distance 22_86_bond, /MNEI_disulfide_object//A/22/CA, /MNEI_disulfide_object//A/86/CA
set dash_width, 4, 22_86_bond
set dash_color, disulfide_color, 22_86_bond
set dash_gap, 0.4, 22_86_bond
set grid_slot, 1, 22_86_bond
hide labels, 22_86_bond
distance 20_34_bond, /MNEI_disulfide_object//A/20/CA, /MNEI_disulfide_object//A/34/CA
set dash_width, 4, 20_34_bond
set dash_color, disulfide_color, 20_34_bond
set dash_gap, 0.4, 20_34_bond
set grid_slot, 1, 20_34_bond
hide labels, 20_34_bond
distance 20_66_bond, /MNEI_disulfide_object//A/20/CA, /MNEI_disulfide_object//A/66/CA
set dash_width, 4, 20_66_bond
set dash_color, disulfide_color, 20_66_bond
set dash_gap, 0.4, 20_66_bond
set grid_slot, 1, 20_66_bond
hide labels, 20_66_bond
distance 48_56_bond, /MNEI_disulfide_object//A/48/CA, /MNEI_disulfide_object//A/56/CA
set dash_width, 4, 48_56_bond
set dash_color, disulfide_color, 48_56_bond
set dash_gap, 0.4, 48_56_bond
set grid_slot, 1, 48_56_bond
hide labels, 48_56_bond
distance 48_54_bond, /MNEI_disulfide_object//A/48/CA, /MNEI_disulfide_object//A/54/CA
set dash_width, 4, 48_54_bond
set dash_color, disulfide_color, 48_54_bond
set dash_gap, 0.4, 48_54_bond
set grid_slot, 1, 48_54_bond
hide labels, 48_54_bond
distance 1_44_bond, /MNEI_disulfide_object//A/1/CA, /MNEI_disulfide_object//A/44/CA
set dash_width, 4, 1_44_bond
set dash_color, disulfide_color, 1_44_bond
set dash_gap, 0.4, 1_44_bond
set grid_slot, 1, 1_44_bond
hide labels, 1_44_bond
distance 32_66_bond, /MNEI_disulfide_object//A/32/CA, /MNEI_disulfide_object//A/66/CA
set dash_width, 4, 32_66_bond
set dash_color, disulfide_color, 32_66_bond
set dash_gap, 0.4, 32_66_bond
set grid_slot, 1, 32_66_bond
hide labels, 32_66_bond
fetch 1IV7, MNEI_object_2
set grid_slot, 2, MNEI_object_2
hide everything, MNEI_object_2
show cartoon, MNEI_object_2 and chain A
color grey80, MNEI_object_2
set cartoon_transparency, 0.2, MNEI_object_2
select MNEI_rosetta, MNEI_object_2 and resi 42+60+47+41+16+12+29
set cartoon_transparency, 0.0, MNEI_rosetta
set_color rosetta_color, [244,131,108]
color rosetta_color, MNEI_rosetta
deselect
select MNEI_bibliography, MNEI_object_2 and resi 23
set cartoon_transparency, 0.0, MNEI_bibliography
set_color bibliography_color, [248,158,68]
color bibliography_color, MNEI_bibliography
deselect
remove MNEI_object_2 and chain B
alignto MNEI_object_2
center
orient
