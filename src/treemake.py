from ply import yacc
import ply.lex as lex

from src.calclex import tokens
class Map:
    def __init__(self, width, height, base):
        self.width = width
        self.height = height
        self.terrain = [[Terrain(base) for i in range(height)] for j in range(width)]
        self.objects = [[[] for i in range(height)] for j in range(width)]
    def __str__(self):
        return f'Map({self.width}, {self.height})'
    def __repr__(self):
        return str(self)

    def edit_terrain(self, x, y, new):
        self.terrain[x][y] = new
    def add_object(self, obj, x, y):
        self.objects[x][y].append(obj)


class Road:
    def __init__(self):
        pass
class River:
    def __init__(self):
        pass
class City:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        pass
class Terrain:
    def __init__(self, base):
        self.base = base
        pass
    def __str__(self):
        return f'Terrain({self.base})'
    def __repr__(self):
        return str(self)
class tree_node:
    def __init__(self, type, value, children):
        self.type = type
        self.value = value
        self.children = children

names = []
objects = {}

def p_start(p):
    '''start : instruction_iterator EOF
             | EOF'''
    pass


def p_instruction_iterator(p):
    '''instruction_iterator : instruction NEWLINE
                            | instruction_iterator instruction NEWLINE'''
    pass


def p_instruction_create(p):
    '''instruction : CREATE_KEYWORD type VARNAME_ARGNAME construction_arguments'''
    if p[3] in names:
        raise Exception(f'Name {p[3]} already in use')
    names.append(p[3])
    if p[2] == 'map':
        objects[p[3]] = Map(p[4]['width'], p[4]['height'], p[4]['base'])
    elif p[2] == 'city':
        objects[p[3]] = City(p[3], p[4]['size'])
    elif p[2] == 'road':
        objects[p[3]] = Road()
    elif p[2] == 'river':
        objects[p[3]] = River()
    elif p[2] == 'terrain':
        if 'base' not in p[4]:
            raise Exception('Terrain must have a base')
        if len(p[4]) > 1:
            raise Exception('Invalid arguments for terrain')
        objects[p[3]] = Terrain(p[4]['base'])
    else:
        raise Exception(f'Unknown type {p[2]}')
    pass


def p_instruction_place_new_unnamed(p):
    '''instruction : PLACE_KEYWORD type construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinates'''
    if p[5] not in names:
        raise Exception(f'Name {p[5]} not found')
    if p[2] == 'map':
        raise Exception('Cannot place new map. - It makes no sense')
    elif p[2] == 'city':
        objects[p[5]].add_object(City(None, p[3]['size']), p[6][0], p[6][1])
    elif p[2] == 'road':
        objects[p[5]].add_object(Road(), p[6][0], p[6][1])
    elif p[2] == 'river':
        objects[p[5]].add_object(River(), p[6][0], p[6][1])
    elif p[2] == 'terrain':
        if 'base' not in p[3]:
            raise Exception('Terrain must have a base')
        if len(p[3]) > 1:
            raise Exception('Invalid arguments for terrain')
        objects[p[5]].edit_terrain(p[6][0], p[6][1], Terrain(p[3]['base']))
    pass


def p_instruction_place_new_named(p):
    '''instruction : PLACE_KEYWORD type VARNAME_ARGNAME construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinates'''
    if p[3] in names:
        raise Exception(f'Name {p[3]} already in use')
    if p[6] not in names:
        raise Exception(f'Name {p[6]} not found')
    names.append(p[3])
    if p[2] == 'map':
        raise Exception('Cannot place new map. - It makes no sense')
    if p[2] == 'city':
        objects[p[3]] = City(p[3], p[4]['size'])
        objects[p[6]].add_object(objects[p[3]], p[7][0], p[7][1])
    elif p[2] == 'road':
        objects[p[3]] = Road()
        objects[p[6]].add_object(objects[p[3]], p[7][0], p[7][1])
    elif p[2] == 'river':
        objects[p[3]] = River()
        objects[p[6]].add_object(objects[p[3]], p[7][0], p[7][1])
    elif p[2] == 'terrain':
        if 'base' not in p[4]:
            raise Exception('Terrain must have a base')
        if len(p[4]) > 1:
            raise Exception('Invalid arguments for terrain')
        objects[p[3]] = Terrain(p[4]['base'])
        objects[p[6]].add_object(objects[p[3]], p[7][0], p[7][1])
    else:
        raise Exception(f'Unknown type {p[2]}')
    pass


def p_instruction_place_existing(p):
    '''instruction : PLACE_KEYWORD VARNAME_ARGNAME ON_KEYWORD VARNAME_ARGNAME coordinates'''
    if p[2] not in names:
        raise Exception(f'Name {p[2]} not found')
    if p[4] not in names:
        raise Exception(f'Name {p[4]} not found')
    if type(objects[p[2]]) != Map:
        objects[p[4]].add_object(objects[p[2]], p[5][0], p[5][1])
    else:
        x_add = p[5][0]
        y_add = p[5][1]
        for x in range(objects[p[2]].width):
            for y in range(objects[p[2]].height):
                for i in objects[p[2]].global_objects[x][y]:
                    if x + x_add < objects[p[4]].width and y + y_add < objects[p[4]].height:
                        objects[p[4]].add_object(i, x + x_add, y + y_add)
                objects[p[4]].edit_terrain(x + x_add, y + y_add, objects[p[2]].terrain[x][y])
    pass


def p_instruction_render(p):
    '''instruction : RENDER_KEYWORD VARNAME_ARGNAME optional_render_string optional_coordinates'''
                                                                                                             #todo: render
    pass


def p_optional_render_string(p):
    '''optional_render_string : AS_KEYWORD STRING
                              | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None
    pass


def p_optional_coordinates(p):
    '''optional_coordinates : coordinates
                            | empty'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None
    pass


def p_type(p):
    '''type : MAP_KEYWORD
            | TERRAIN_KEYWORD
            | CITY_KEYWORD
            | ROAD_KEYWORD
            | RIVER_KEYWORD'''
    p[0] = p[1]
    pass


def p_construction_arguments(p):
    '''construction_arguments : LPAREN argument_iterator RPAREN'''
    p[0] = p[2]
    pass


def p_argument_iterator(p):
    '''argument_iterator : argument
                         | argument_iterator COMMA argument
                         | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = {
            p[1][0]: p[1][1]
        }
    elif len(p) == 4:
        p[0] = p[1]
        p[0][p[3][0]] = p[3][1]
    else:
        p[0] = {}
    pass


def p_argument(p):
    '''argument : VARNAME_ARGNAME COLON value'''
    p[0] = (p[1], p[3])
    pass


def p_value(p):
    '''value : NUMBER
             | STRING
             | list
             | coordinates'''
    p[0] = p[1]
    pass


def p_list(p):
    '''list : LSQUAREPAREN list_item_iterator RSQUAREPAREN'''
    p[0] = p[2]
    pass


def p_list_item_iterator(p):
    '''list_item_iterator : value
                          | list_item_iterator COMMA value
                          | empty'''
    if len(p) == 2 and p[1] is not None:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1]
        p[0].append(p[3])
    else:
        p[0] = []
    pass


def p_coordinates(p):
    '''coordinates : LPAREN NUMBER COMMA NUMBER RPAREN'''
    p[0] = (p[2], p[4])
    pass


def p_empty(p):
    '''empty :'''
    p[0] = None
    pass


def p_error(p):
    print("Syntax error in input! Line: " + str(p.lineno) + " Token: " + str(p.value) + " Type: " + str(p.type))
    print(p)
    pass


if __name__ == '__main__':
    data = \
        "Create map myMap (width: 18, height: 21, base: \"water\")\n\
        Create map myMap2 (width: 8, height: 2, base: \"grass\")\n\
        Place terrain (base: \"grass\") on myMap2 (4, 1)\n\
        Create city myCity (size: \"small\")\n\
        Place myCity on myMap2 (3, 1)\n\
        Place road () on myMap2 (0,0)\n\
        Create road myRoad ()\n\
        Place myRoad on myMap2 (0,0)\n\
        Place myMap2 on myMap (1,2)\n\
        Render myMap as \"./mymap.png\" (1920,1080)\n\
        EOF"
    #data = "Create city myCity (size: \"small\")\n\
           #EOF"
    #data = "EOF"
    parser = yacc.yacc()
    result = parser.parse(data)
    print(result)
