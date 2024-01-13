import ply.lex as lex
reserved = {
    'Create' : 'CREATE_KEYWORD',
    'Place' : 'PLACE_KEYWORD',
    'Render' : 'RENDER_KEYWORD',
    'on' : 'ON_KEYWORD',
    'as' : 'AS_KEYWORD',
    'map' : 'MAP_KEYWORD',
    'terrain' : 'TERRAIN_KEYWORD',
    'city' : 'CITY_KEYWORD',
    'road' : 'ROAD_KEYWORD',
    'river' : 'RIVER_KEYWORD',
    'EOF' : 'EOF',
}
tokens = [
    'LPAREN',
    'RPAREN',
    'COMMA',
    'LSQUAREPAREN',
    'RSQUAREPAREN',
    'COLON',
    'NUMBER',
    'VARNAME_ARGNAME',
    'STRING',
    'NEWLINE',
] + list(reserved.values())

t_ignore = ' \t'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_LSQUAREPAREN = r'\['
t_RSQUAREPAREN = r'\]'
t_COLON = r':'

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

def t_VARNAME_ARGNAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'VARNAME_ARGNAME')
    return t
def t_STRING(t):
    r'\"[^"]*\"'
    t.value = t.value[1:-1]
    return t
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

