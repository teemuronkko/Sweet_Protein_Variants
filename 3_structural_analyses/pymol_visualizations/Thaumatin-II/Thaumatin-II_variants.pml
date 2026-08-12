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
fetch 3AOK, Thaumatin-II_disulfide_object
set grid_slot, 1, Thaumatin-II_disulfide_object
hide everything, Thaumatin-II_disulfide_object
show cartoon, Thaumatin-II_disulfide_object and chain A
color grey80, Thaumatin-II_disulfide_object
set cartoon_transparency, 0.2, Thaumatin-II_disulfide_object
select Thaumatin-II_disulfide, Thaumatin-II_disulfide_object and resi 68+109+108+173+60+148+104+157
set cartoon_transparency, 0, Thaumatin-II_disulfide
set_color disulfide_color, [170,49,122]
color disulfide_color, Thaumatin-II_disulfide


distance 68_109_bond, /Thaumatin-II_disulfide_object//A/68/CA, /Thaumatin-II_disulfide_object//A/109/CA
set dash_width, 4, 68_109_bond
set dash_color, disulfide_color, 68_109_bond
set dash_gap, 0.4, 68_109_bond
set grid_slot, 1, 68_109_bond
hide labels, 68_109_bond
distance 148_157_bond, /Thaumatin-II_disulfide_object//A/148/CA, /Thaumatin-II_disulfide_object//A/157/CA
set dash_width, 4, 148_157_bond
set dash_color, disulfide_color, 148_157_bond
set dash_gap, 0.4, 148_157_bond
set grid_slot, 1, 148_157_bond
hide labels, 148_157_bond
distance 104_173_bond, /Thaumatin-II_disulfide_object//A/104/CA, /Thaumatin-II_disulfide_object//A/173/CA
set dash_width, 4, 104_173_bond
set dash_color, disulfide_color, 104_173_bond
set dash_gap, 0.4, 104_173_bond
set grid_slot, 1, 104_173_bond
hide labels, 104_173_bond
distance 104_108_bond, /Thaumatin-II_disulfide_object//A/104/CA, /Thaumatin-II_disulfide_object//A/108/CA
set dash_width, 4, 104_108_bond
set dash_color, disulfide_color, 104_108_bond
set dash_gap, 0.4, 104_108_bond
set grid_slot, 1, 104_108_bond
hide labels, 104_108_bond
fetch 3AOK, Thaumatin-II_object_2
set grid_slot, 2, Thaumatin-II_object_2
hide everything, Thaumatin-II_object_2
show cartoon, Thaumatin-II_object_2 and chain A
color grey80, Thaumatin-II_object_2
set cartoon_transparency, 0.2, Thaumatin-II_object_2
select Thaumatin-II_consensus, Thaumatin-II_object_2 and resi 153+148+104+23+136+184
set cartoon_transparency, 0.0, Thaumatin-II_consensus
set_color consensus_color, [224,79,103]
color consensus_color, Thaumatin-II_consensus
deselect
select Thaumatin-II_rosetta, Thaumatin-II_object_2 and resi 68+105+207+26+155+65+32+160
set cartoon_transparency, 0.0, Thaumatin-II_rosetta
set_color rosetta_color, [244,131,108]
color rosetta_color, Thaumatin-II_rosetta
deselect
select Thaumatin-II_bibliography, Thaumatin-II_object_2 and resi 89
set cartoon_transparency, 0.0, Thaumatin-II_bibliography
set_color bibliography_color, [248,158,68]
color bibliography_color, Thaumatin-II_bibliography
deselect
alignto Thaumatin-II_object_2
center
orient
