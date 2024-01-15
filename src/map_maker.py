import os

from ply import yacc
import PIL.Image as pil_image
import PIL.ImageDraw as pil_image_draw
import PIL.ImageFont as pil_image_font
import sys

from calclex import tokens
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
    def __str__(self):
        return f'Road'
    def __repr__(self):
        return str(self)
class River:
    def __init__(self):
        pass
    def __str__(self):
        return f'River'
    def __repr__(self):
        return str(self)
class City:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        pass
    def __str__(self):
        return f'City({self.name})'
    def __repr__(self):
        return str(self)
class Terrain:
    def __init__(self, base):
        self.base = base
        pass
    def __str__(self):
        return f'Terrain({self.base})'
    def __repr__(self):
        return str(self)

class Mountain:
    def __init__(self):
        pass
    def __str__(self):
        return f'Mountain'
    def __repr__(self):
        return str(self)


names = []
global_objects = {}

def execute(list_of_instructions, local_objects = {}):
    for instruction in list_of_instructions:
        if instruction[0] == "create":
            if instruction[2] in names:
                raise Exception("Name already taken")
            else:
                if instruction[1] == "map":
                    global_objects[instruction[2]] = Map(instruction[3]['width'], instruction[3]['height'], instruction[3]['base'])
                elif instruction[1] == "road":
                    global_objects[instruction[2]] = Road()
                elif instruction[1] == "river":
                    global_objects[instruction[2]] = River()
                elif instruction[1] == "city":
                    global_objects[instruction[2]] = City(instruction[2], instruction[3]['size'])
                elif instruction[1] == "mountain":
                    global_objects[instruction[2]] = Mountain()
                elif instruction[1] == "terrain":
                    global_objects[instruction[2]] = Terrain(instruction[3]['base'])
                else:
                    raise Exception("Unknown type")
                names.append(instruction[2])

        elif instruction[0] == "place_new_unnamed":
            if instruction[3] not in names:
                raise Exception("Name not found")
            else:
                x_coord = instruction[4][0]
                y_coord = instruction[4][1]
                if type(x_coord) == tuple:
                    if x_coord[0] == "varname":
                        x_coord = local_objects[x_coord[1]]
                        if x_coord == None:
                            x_coord = global_objects[x_coord[1]]
                if type(y_coord) == tuple:
                    if y_coord[0] == "varname":
                        y_coord = local_objects[y_coord[1]]
                        if y_coord == None:
                            y_coord = global_objects[y_coord[1]]

                if instruction[1] == "road":
                    global_objects[instruction[3]].add_object(Road(), x_coord, y_coord)
                elif instruction[1] == "river":
                    global_objects[instruction[3]].add_object(River(), x_coord, y_coord)
                elif instruction[1] == "mountain":
                    global_objects[instruction[3]].add_object(Mountain(), x_coord, y_coord)
                elif instruction[1] == "city":
                    global_objects[instruction[3]].add_object(City(None, instruction[2]['size']), x_coord, y_coord)
                elif instruction[1] == "terrain":
                    global_objects[instruction[3]].edit_terrain(x_coord, y_coord, Terrain(instruction[2]['base']))
                else:
                    raise Exception("Unknown type")
        elif instruction[0] == "place_new_named":  #(flag, type, name, args, mapname, coordinates)
            if instruction[2] in names:
                raise Exception("Name already taken")
            elif instruction[4] not in names:
                raise Exception("Map name not found")
            else:
                x_coord = instruction[5][0]
                y_coord = instruction[5][1]
                if type(x_coord) == tuple:
                    if x_coord[0] == "varname":
                        x_coord = local_objects[x_coord[1]]
                        if x_coord == None:
                            x_coord = global_objects[x_coord[1]]
                if type(y_coord) == tuple:
                    if y_coord[0] == "varname":
                        y_coord = local_objects[y_coord[1]]
                        if y_coord == None:
                            y_coord = global_objects[y_coord[1]]

                if instruction[1] == "road":
                    global_objects[instruction[2]] = Road()
                    names.append(instruction[2])
                    global_objects[instruction[4]].add_object(global_objects[instruction[2]], x_coord, y_coord)
                elif instruction[1] == "river":
                    global_objects[instruction[2]] = River()
                    names.append(instruction[2])
                    global_objects[instruction[4]].add_object(global_objects[instruction[2]], x_coord, y_coord)
                elif instruction[1] == "mountain":
                    global_objects[instruction[2]] = Mountain()
                    names.append(instruction[2])
                    global_objects[instruction[4]].add_object(global_objects[instruction[2]], x_coord, y_coord)
                elif instruction[1] == "city":
                    global_objects[instruction[2]] = City(instruction[2], instruction[3]['size'])
                    names.append(instruction[2])
                    global_objects[instruction[4]].add_object(global_objects[instruction[2]], x_coord, y_coord)
                elif instruction[1] == "terrain":
                    global_objects[instruction[2]] = Terrain(instruction[3]['base'])
                    names.append(instruction[2])
                    global_objects[instruction[4]].terrain[x_coord][y_coord] = global_objects[instruction[2]]
                else:
                    raise Exception("Unknown type")
        elif instruction[0] == "place_existing": #(flag, name, mapname, coordinates)
            if instruction[1] not in names:
                raise Exception("Name not found")
            elif instruction[2] not in names:
                raise Exception("Map name not found")
            else:
                x_coord = instruction[3][0]
                y_coord = instruction[3][1]
                if type(x_coord) == tuple:
                    if x_coord[0] == "varname":
                        x_coord = local_objects[x_coord[1]]
                        if x_coord == None:
                            x_coord = global_objects[x_coord[1]]
                if type(y_coord) == tuple:
                    if y_coord[0] == "varname":
                        y_coord = local_objects[y_coord[1]]
                        if y_coord == None:
                            y_coord = global_objects[y_coord[1]]

                if type(global_objects[instruction[1]]) == Terrain:
                    global_objects[instruction[2]].edit_terrain(x_coord, y_coord, global_objects[instruction[1]].base)
                elif type(global_objects[instruction[1]]) == Map:
                    for i in range(len(global_objects[instruction[1]].terrain)):
                        for j in range(len(global_objects[instruction[1]].terrain[i])):
                            global_objects[instruction[2]].edit_terrain(x_coord + i, y_coord + j, global_objects[instruction[1]].terrain[i][j])
                    for i in range(len(global_objects[instruction[1]].objects)):
                        for j in range(len(global_objects[instruction[1]].objects[i])):
                            for k in range(len(global_objects[instruction[1]].objects[i][j])):
                                global_objects[instruction[2]].add_object(global_objects[instruction[1]].objects[i][j][k], x_coord + i, y_coord + j)
                else:
                    global_objects[instruction[2]].add_object(global_objects[instruction[1]], x_coord, y_coord)
        elif instruction[0] == "render":   #(flag, name, renderstring, coordinates)
            render(instruction[1], instruction[2], instruction[3])
        elif instruction[0] == "for":
            execute_for_loop(instruction[3], instruction[1], instruction[2][0], instruction[2][1], local_objects)
    pass

def execute_for_loop(list_of_instructions, varname, start, stop, local_objects):
    if(type(start) != int or type(stop) != int):
        raise Exception("For loop start and stop must be integers")
    for i in range(start, stop):
        new_local_objects = {}
        for key in local_objects:
            new_local_objects[key] = local_objects[key]
        new_local_objects[varname] = i
        execute(list_of_instructions, new_local_objects)
    pass

def render(mapname, renderstring, coords):
    if renderstring is None:
        renderstring = "/.tmp/output.png"
    map = global_objects[mapname]
    x_size = int((0.25+len(map.terrain)*0.75)*278)
    y_size = int((0.5+len(map.terrain[0]))*242)
    output_sprite = pil_image.new("RGBA", (x_size, y_size), (0, 0, 0))
    draw = pil_image_draw.Draw(output_sprite)
    font_city = pil_image_font.load_default(size=30)
    road_alpha = pil_image.open("./img/RoadAlpha.png")
    road_isolated_alpha = pil_image.open("./img/RoadIsolatedAlpha.png")
    mountain_sprite = pil_image.open("./img/Mountain.png")
    city_sprites = {
        'big': pil_image.open("./img/BigCity.png"),
        'medium': pil_image.open("./img/MediumCity.png"),
        'small': pil_image.open("./img/SmolCity.png")
    }
    terrain_sprites = {
        'water': pil_image.open("./img/Water.png"),
        'grass': pil_image.open("./img/Grass.png")
    }
    is_road = [[False for i in range(len(map.terrain[0]))] for j in range(len(map.terrain))]
    for i in range(len(map.terrain)):
        for j in range(len(map.terrain[i])):
            for obj in map.objects[i][j]:
                if type(obj) == Road:
                    is_road[i][j] = True
                    break
    for i in range(len(map.terrain)):
        for j in range(len(map.terrain[i])):
            terrain = map.terrain[i][j].base
            output_sprite.paste(terrain_sprites[terrain], calc_position(i, j, x_size, y_size), terrain_sprites[terrain])

            # todo: road drawing
            if is_road[i][j]:

                if j > 0:
                    if is_road[i][j-1]:
                        new_sprite = road_alpha.copy()
                        output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                if j < len(map.terrain[i])-1:
                    if is_road[i][j+1]:
                        new_sprite = road_alpha.copy().rotate(180)
                        output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                if i % 2 == 0:
                    if i>0:
                        if is_road[i-1][j]:
                            new_sprite = road_alpha.copy().rotate(-120)
                            output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                        if j > 0:
                            if is_road[i-1][j-1]:
                                new_sprite = road_alpha.copy().rotate(-60)
                                output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                    if i < len(map.terrain)-1:
                        if is_road[i+1][j]:
                            new_sprite = road_alpha.copy().rotate(120)
                            output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                        if j > 0:
                            if is_road[i+1][j-1]:
                                new_sprite = road_alpha.copy().rotate(60)
                                output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                else:
                    if i>0:
                        if is_road[i-1][j]:
                            new_sprite = road_alpha.copy().rotate(-60)
                            output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                        if j < len(map.terrain[i])-1:
                            if is_road[i-1][j+1]:
                                new_sprite = road_alpha.copy().rotate(-120)
                                output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                    if i < len(map.terrain)-1:
                        if is_road[i+1][j]:
                            new_sprite = road_alpha.copy().rotate(60)
                            output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)
                        if j < len(map.terrain[i])-1:
                            if is_road[i+1][j+1]:
                                new_sprite = road_alpha.copy().rotate(120)
                                output_sprite.paste(new_sprite, calc_position(i, j, x_size, y_size), new_sprite)

            is_mountains = False
            for obj in map.objects[i][j]:
                if type(obj) == Mountain:
                    is_mountains = True
                    break
            if is_mountains:
                output_sprite.paste(mountain_sprite, calc_position(i, j, x_size, y_size), mountain_sprite)



            is_city = False
            size = None
            city_name = None
            for obj in map.objects[i][j]:
                if type(obj) == City:
                    is_city = True
                    size = obj.size
                    city_name = obj.name
                    break
            if is_city:
                city_coords = calc_position(i, j, x_size, y_size)
                output_sprite.paste(city_sprites[size], city_coords, city_sprites[size])
                text_coords = (city_coords[0]+139, city_coords[1]+187)
                draw.text(text_coords, city_name, (0, 0, 0), font=font_city, align="center", anchor="mm")



            textpos = calc_position(i, j, x_size, y_size)
            new_textpos = (textpos[0]+139, textpos[1]+227)
            font_coords = pil_image_font.load_default(10)
            draw.text(new_textpos, str(i)+","+str(j), (0, 0, 0), font=font_coords, align="center", anchor="mm")
    folderpath = renderstring
    while folderpath[-1] != "/":
        folderpath = folderpath[:-1]
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    output_sprite.save(renderstring, "PNG")

def calc_position(x_on_map, y_on_map, maxx, maxy):
    x_ret = int(0.75*x_on_map*278)
    y_ret = maxy - (242*y_on_map) - 242 -(int(0.5*242)*(x_on_map%2))
    return x_ret, y_ret

def p_start(p):
    '''start : instruction_iterator EOF'''
    execute(p[1])
    p[0] = True


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


def p_instruction_for(p):                                                        #(flag, variable, range, instructions)
    '''instruction : FOR_KEYWORD VARNAME_ARGNAME coordinates NEWLINE instruction_iterator ENDFOR_KEYWORD'''
    p[0] = []
    p[0].append("for")
    p[0].append(p[2])
    p[0].append(p[3])
    p[0].append(p[5])
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
            | RIVER_KEYWORD
            | MOUNTAIN_KEYWORD'''
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
    '''coordinates : LPAREN value COMMA value RPAREN'''
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
    '''
    data = \
        "Create map myMap (width: 18, height: 21, base: \"water\")\n\
        Create map myMap2 (width: 8, height: 2, base: \"grass\")\n\
        Place terrain (base: \"grass\") on myMap2 (4, 1)\n\
        Place mountain () on myMap2 (4, 1)\n\
        Create city myCity (size: \"small\")\n\
        Place myCity on myMap (3, 1)\n\
        Place road () on myMap2 (7,0)\n\
        for i (0, 4)\n\
            for j (0, 7)\n \
                Place road () on myMap (i,j)\n\
            endfor\n\
        endfor\n\
        Create road myRoad ()\n\
        Place myRoad on myMap2 (0,0)\n\
        Place myMap2 on myMap (1,2)\n\
        Render myMap as \"./mymap.png\" (1920,1080)\n\
        EOF"
    #data = "Create city myCity (size: \"small\")\n\
           #EOF"
    #data = "EOF"'''
    filename = sys.argv[1]
    print("Parsing file: " + filename)
    data = open(filename, "r").read()

    parser = yacc.yacc()
    result = parser.parse(data)
    print("Map created successfully!")
