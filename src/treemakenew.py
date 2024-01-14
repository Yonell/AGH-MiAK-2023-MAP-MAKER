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

names = []
objects = {}

def execute(list_of_instructions):
    for instruction in list_of_instructions:
        if instruction[0] == "create":
            if instruction[2] in names:
                raise Exception("Name already taken")
            else:
                if instruction[1] == "map":
                    objects[instruction[2]] = Map(instruction[3]['width'], instruction[3]['height'], instruction[3]['base'])
                elif instruction[1] == "road":
                    objects[instruction[2]] = Road()
                elif instruction[1] == "river":
                    objects[instruction[2]] = River()
                elif instruction[1] == "city":
                    objects[instruction[2]] = City(instruction[2], instruction[3]['size'])
                elif instruction[1] == "terrain":
                    objects[instruction[2]] = Terrain(instruction[3]['base'])
                else:
                    raise Exception("Unknown type")
                names.append(instruction[2])

        elif instruction[0] == "place_new_unnamed":
            if instruction[3] not in names:
                raise Exception("Name not found")
            else:
                if instruction[1] == "road":
                    objects[instruction[3]].add_object(Road(), instruction[4][0], instruction[4][1])
                elif instruction[1] == "river":
                    objects[instruction[3]].add_object(River(), instruction[4][0], instruction[4][1])
                elif instruction[1] == "city":
                    objects[instruction[3]].add_object(City(None, instruction[2]['size']), instruction[4][0], instruction[4][1])
                elif instruction[1] == "terrain":
                    objects[instruction[3]].edit_terrain(instruction[4][0], instruction[4][1], Terrain(instruction[2]['base']))
                else:
                    raise Exception("Unknown type")
        elif instruction[0] == "place_new_named":  #(flag, type, name, args, mapname, coordinates)
            if instruction[2] in names:
                raise Exception("Name already taken")
            elif instruction[4] not in names:
                raise Exception("Map name not found")
            else:
                if instruction[1] == "road":
                    objects[instruction[2]] = Road()
                    names.append(instruction[2])
                    objects[instruction[4]].add_object(objects[instruction[2]], instruction[5][0], instruction[5][1])
                elif instruction[1] == "river":
                    objects[instruction[2]] = River()
                    names.append(instruction[2])
                    objects[instruction[4]].add_object(objects[instruction[2]], instruction[5][0], instruction[5][1])
                elif instruction[1] == "city":
                    objects[instruction[2]] = City(instruction[2], instruction[3]['size'])
                    names.append(instruction[2])
                    objects[instruction[4]].add_object(objects[instruction[2]], instruction[5][0], instruction[5][1])
                elif instruction[1] == "terrain":
                    objects[instruction[2]] = Terrain(instruction[3]['base'])
                    names.append(instruction[2])
                    objects[instruction[4]].terrain[instruction[5][0]][instruction[5][1]] = objects[instruction[2]]
                else:
                    raise Exception("Unknown type")
        elif instruction[0] == "place_existing": #(flag, name, mapname, coordinates)
            if instruction[1] not in names:
                raise Exception("Name not found")
            elif instruction[2] not in names:
                raise Exception("Map name not found")
            else:
                if type(objects[instruction[1]]) == Terrain:
                    objects[instruction[2]].edit_terrain(instruction[3][0], instruction[3][1], objects[instruction[1]].base)
                elif type(objects[instruction[1]]) == Map:
                    for i in range(len(objects[instruction[1]].terrain)):
                        for j in range(len(objects[instruction[1]].terrain[i])):
                            objects[instruction[2]].edit_terrain(instruction[3][0]+i, instruction[3][1]+j, objects[instruction[1]].terrain[i][j])
                    for i in range(len(objects[instruction[1]].objects)):
                        for j in range(len(objects[instruction[1]].objects[i])):
                            for k in range(len(objects[instruction[1]].objects[i][j])):
                                objects[instruction[2]].add_object(objects[instruction[1]].objects[i][j][k], instruction[3][0]+i, instruction[3][1]+j)
                else:
                    objects[instruction[2]].add_object(objects[instruction[1]], instruction[3][0], instruction[3][1])
        elif instruction[0] == "render":
            pass                                                                # TODO: render
    pass

def p_start(p):
    '''start : instruction_iterator EOF'''
    try:
        execute(p[1])
        p[0] = True
    except Exception as e:
        print(e)
        p[0] = False
    pass


def p_instruction_iterator(p):
    '''instruction_iterator : instruction_iterator instruction NEWLINE'''
    p[1].append(p[2])
    p[0] = p[1]
    pass


def p_instruction_iterator_end(p):
    '''instruction_iterator : empty'''
    p[0] = []
    pass


def p_instruction_create(p):                                                        #(flag, type, name, args)
    '''instruction : CREATE_KEYWORD type VARNAME_ARGNAME construction_arguments'''
    p[0] = []
    p[0].append("create")
    p[0].append(p[2])
    p[0].append(p[3])
    p[0].append(p[4])
    pass


def p_instruction_place_new_unnamed(p):                                             #(flag, type, args, name, coordinates)
    '''instruction : PLACE_KEYWORD type construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinates'''
    p[0] = []
    p[0].append("place_new_unnamed")
    p[0].append(p[2])
    p[0].append(p[3])
    p[0].append(p[5])
    p[0].append(p[6])
    pass


def p_instruction_place_new_named(p):                                               #(flag, type, name, args, mapname, coordinates)
    '''instruction : PLACE_KEYWORD type VARNAME_ARGNAME construction_arguments ON_KEYWORD VARNAME_ARGNAME coordinates'''
    p[0] = []
    p[0].append("place_new_named")
    p[0].append(p[2])
    p[0].append(p[3])
    p[0].append(p[4])
    p[0].append(p[6])
    p[0].append(p[7])
    pass


def p_instruction_place_existing(p):                                                #(flag, name, mapname, coordinates)
    '''instruction : PLACE_KEYWORD VARNAME_ARGNAME ON_KEYWORD VARNAME_ARGNAME coordinates'''
    p[0] = []
    p[0].append("place_existing")
    p[0].append(p[2])
    p[0].append(p[4])
    p[0].append(p[5])
    pass


def p_instruction_render(p):                                                        #(flag, name, renderstring, coordinates)
    '''instruction : RENDER_KEYWORD VARNAME_ARGNAME optional_render_string optional_coordinates'''
    p[0] = []
    p[0].append("render")
    p[0].append(p[2])
    p[0].append(p[3])
    p[0].append(p[4])
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
def p_value_VARNAME(p):
    '''value : VARNAME_ARGNAME'''
    p[0] = ("varname", p[1])
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
