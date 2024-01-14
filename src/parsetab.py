
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AS_KEYWORD CITY_KEYWORD COLON COMMA CREATE_KEYWORD ENDFOR_KEYWORD EOF FOR_KEYWORD LPAREN LSQUAREPAREN MAP_KEYWORD NEWLINE NUMBER ON_KEYWORD PLACE_KEYWORD RENDER_KEYWORD RIVER_KEYWORD ROAD_KEYWORD RPAREN RSQUAREPAREN STRING TERRAIN_KEYWORD VARNAME_ARGNAMEstart : instruction_iterator EOFinstruction_iterator : instruction_iterator instruction NEWLINEinstruction_iterator : emptyinstruction : CREATE_KEYWORD type VARNAME_ARGNAME construction_argumentsinstruction : PLACE_KEYWORD type construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinatesinstruction : PLACE_KEYWORD type VARNAME_ARGNAME construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinatesinstruction : PLACE_KEYWORD VARNAME_ARGNAME ON_KEYWORD VARNAME_ARGNAME coordinatesinstruction : RENDER_KEYWORD VARNAME_ARGNAME optional_render_string optional_coordinatesinstruction : FOR_KEYWORD VARNAME_ARGNAME coordinates NEWLINE instruction_iterator ENDFOR_KEYWORDoptional_render_string : AS_KEYWORD STRING\n                              | emptyoptional_coordinates : coordinates\n                            | emptytype : MAP_KEYWORD\n            | TERRAIN_KEYWORD\n            | CITY_KEYWORD\n            | ROAD_KEYWORD\n            | RIVER_KEYWORDconstruction_arguments : LPAREN argument_iterator RPARENargument_iterator : argument\n                         | argument_iterator COMMA argument\n                         | emptyargument : VARNAME_ARGNAME COLON valuevalue : NUMBER\n             | STRING\n             | list\n             | coordinatesvalue : VARNAME_ARGNAMElist : LSQUAREPAREN list_item_iterator RSQUAREPARENlist_item_iterator : value\n                          | list_item_iterator COMMA value\n                          | emptycoordinates : LPAREN value COMMA value RPARENempty :'
    
_lr_action_items = {'EOF':([0,2,3,10,],[-34,4,-3,-2,]),'CREATE_KEYWORD':([0,2,3,10,43,57,],[-34,6,-3,-2,-34,6,]),'PLACE_KEYWORD':([0,2,3,10,43,57,],[-34,7,-3,-2,-34,7,]),'RENDER_KEYWORD':([0,2,3,10,43,57,],[-34,8,-3,-2,-34,8,]),'FOR_KEYWORD':([0,2,3,10,43,57,],[-34,9,-3,-2,-34,9,]),'$end':([1,4,],[0,-1,]),'ENDFOR_KEYWORD':([3,10,43,57,],[-3,-2,-34,66,]),'NEWLINE':([5,19,26,28,29,31,39,40,41,42,53,56,62,66,70,71,],[10,-34,-34,-11,43,-4,-8,-12,-13,-10,-19,-7,-5,-9,-6,-33,]),'MAP_KEYWORD':([6,7,],[12,12,]),'TERRAIN_KEYWORD':([6,7,],[13,13,]),'CITY_KEYWORD':([6,7,],[14,14,]),'ROAD_KEYWORD':([6,7,],[15,15,]),'RIVER_KEYWORD':([6,7,],[16,16,]),'VARNAME_ARGNAME':([7,8,9,11,12,13,14,15,16,17,24,25,30,32,50,52,54,55,58,69,],[18,19,20,21,-14,-15,-16,-17,-18,23,37,38,49,51,49,63,37,49,49,49,]),'LPAREN':([12,13,14,15,16,17,19,20,21,23,26,28,30,38,42,50,51,55,58,63,69,],[-14,-15,-16,-17,-18,24,-34,30,24,24,30,-11,30,30,-10,30,30,30,30,30,30,]),'ON_KEYWORD':([18,22,33,53,],[25,32,52,-19,]),'AS_KEYWORD':([19,],[27,]),'RPAREN':([24,34,35,36,45,46,47,48,49,64,65,67,68,71,],[-34,53,-20,-22,-24,-25,-26,-27,-28,-21,-23,71,-29,-33,]),'COMMA':([24,34,35,36,44,45,46,47,48,49,50,59,60,61,64,65,68,71,72,],[-34,54,-20,-22,58,-24,-25,-26,-27,-28,-34,69,-30,-32,-21,-23,-29,-33,-31,]),'STRING':([27,30,50,55,58,69,],[42,46,46,46,46,46,]),'NUMBER':([30,50,55,58,69,],[45,45,45,45,45,]),'LSQUAREPAREN':([30,50,55,58,69,],[50,50,50,50,50,]),'COLON':([37,],[55,]),'RSQUAREPAREN':([45,46,47,48,49,50,59,60,61,68,71,72,],[-24,-25,-26,-27,-28,-34,68,-30,-32,-29,-33,-31,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'instruction_iterator':([0,43,],[2,57,]),'empty':([0,19,24,26,43,50,],[3,28,36,41,3,61,]),'instruction':([2,57,],[5,5,]),'type':([6,7,],[11,17,]),'construction_arguments':([17,21,23,],[22,31,33,]),'optional_render_string':([19,],[26,]),'coordinates':([20,26,30,38,50,51,55,58,63,69,],[29,40,48,56,48,62,48,48,70,48,]),'argument_iterator':([24,],[34,]),'argument':([24,54,],[35,64,]),'optional_coordinates':([26,],[39,]),'value':([30,50,55,58,69,],[44,60,65,67,72,]),'list':([30,50,55,58,69,],[47,47,47,47,47,]),'list_item_iterator':([50,],[59,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> instruction_iterator EOF','start',2,'p_start','treemakenew.py',135),
  ('instruction_iterator -> instruction_iterator instruction NEWLINE','instruction_iterator',3,'p_instruction_iterator','treemakenew.py',146),
  ('instruction_iterator -> empty','instruction_iterator',1,'p_instruction_iterator_end','treemakenew.py',153),
  ('instruction -> CREATE_KEYWORD type VARNAME_ARGNAME construction_arguments','instruction',4,'p_instruction_create','treemakenew.py',159),
  ('instruction -> PLACE_KEYWORD type construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinates','instruction',6,'p_instruction_place_new_unnamed','treemakenew.py',169),
  ('instruction -> PLACE_KEYWORD type VARNAME_ARGNAME construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinates','instruction',7,'p_instruction_place_new_named','treemakenew.py',180),
  ('instruction -> PLACE_KEYWORD VARNAME_ARGNAME ON_KEYWORD VARNAME_ARGNAME coordinates','instruction',5,'p_instruction_place_existing','treemakenew.py',192),
  ('instruction -> RENDER_KEYWORD VARNAME_ARGNAME optional_render_string optional_coordinates','instruction',4,'p_instruction_render','treemakenew.py',202),
  ('instruction -> FOR_KEYWORD VARNAME_ARGNAME coordinates NEWLINE instruction_iterator ENDFOR_KEYWORD','instruction',6,'p_instruction_for','treemakenew.py',212),
  ('optional_render_string -> AS_KEYWORD STRING','optional_render_string',2,'p_optional_render_string','treemakenew.py',222),
  ('optional_render_string -> empty','optional_render_string',1,'p_optional_render_string','treemakenew.py',223),
  ('optional_coordinates -> coordinates','optional_coordinates',1,'p_optional_coordinates','treemakenew.py',232),
  ('optional_coordinates -> empty','optional_coordinates',1,'p_optional_coordinates','treemakenew.py',233),
  ('type -> MAP_KEYWORD','type',1,'p_type','treemakenew.py',242),
  ('type -> TERRAIN_KEYWORD','type',1,'p_type','treemakenew.py',243),
  ('type -> CITY_KEYWORD','type',1,'p_type','treemakenew.py',244),
  ('type -> ROAD_KEYWORD','type',1,'p_type','treemakenew.py',245),
  ('type -> RIVER_KEYWORD','type',1,'p_type','treemakenew.py',246),
  ('construction_arguments -> LPAREN argument_iterator RPAREN','construction_arguments',3,'p_construction_arguments','treemakenew.py',252),
  ('argument_iterator -> argument','argument_iterator',1,'p_argument_iterator','treemakenew.py',258),
  ('argument_iterator -> argument_iterator COMMA argument','argument_iterator',3,'p_argument_iterator','treemakenew.py',259),
  ('argument_iterator -> empty','argument_iterator',1,'p_argument_iterator','treemakenew.py',260),
  ('argument -> VARNAME_ARGNAME COLON value','argument',3,'p_argument','treemakenew.py',274),
  ('value -> NUMBER','value',1,'p_value','treemakenew.py',280),
  ('value -> STRING','value',1,'p_value','treemakenew.py',281),
  ('value -> list','value',1,'p_value','treemakenew.py',282),
  ('value -> coordinates','value',1,'p_value','treemakenew.py',283),
  ('value -> VARNAME_ARGNAME','value',1,'p_value_VARNAME','treemakenew.py',287),
  ('list -> LSQUAREPAREN list_item_iterator RSQUAREPAREN','list',3,'p_list','treemakenew.py',293),
  ('list_item_iterator -> value','list_item_iterator',1,'p_list_item_iterator','treemakenew.py',299),
  ('list_item_iterator -> list_item_iterator COMMA value','list_item_iterator',3,'p_list_item_iterator','treemakenew.py',300),
  ('list_item_iterator -> empty','list_item_iterator',1,'p_list_item_iterator','treemakenew.py',301),
  ('coordinates -> LPAREN value COMMA value RPAREN','coordinates',5,'p_coordinates','treemakenew.py',313),
  ('empty -> <empty>','empty',0,'p_empty','treemakenew.py',319),
]
