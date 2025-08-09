import re

import ply.lex as lex

fun_names = {
    'avg': 'AVG',
    'sum': 'SUM',
    'min': 'MIN',
    'max': 'MAX',
    'count': 'COUNT'
}

sort_orders = {
    'asc': 'ASC',
    'desc': 'DESC'
}

set_ops = {
    'union': 'UNION',
    'minus': 'SET_MINUS',
    'except': 'EXCEPT',
    'intersect': 'INTERSECT'
}

logic_ops = {
    'and': 'AND',
    'or': 'OR'
}

keywords = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE',
    'group': 'GROUP',
    'join': 'JOIN',
    'order': 'ORDER',
    'limit': 'LIMIT',
    'like': 'LIKE',
    'regexp': 'REGEXP',
    'having': 'HAVING',
    'on': 'ON',
    'by': 'BY',
    'as': 'AS',
    'in': 'IN',
    'is': 'IS',
    'null': 'NULL',
    'not': 'NOT',
    'between': 'BETWEEN',
    'distinct': 'DISTINCT',
    'exists': 'EXISTS',
    'inner': 'INNER',
    'cast': 'CAST',
    'left': 'LEFT',
    'full': 'FULL',
    'outer': 'OUTER',
    'cross': 'CROSS',
    'rollup': 'ROLLUP',
    'right': 'RIGHT',
    'rank': 'RANK',
    'row_number': 'ROW_NUMBER',
    'dense_rank': 'DENSE_RANK',
    'partition': 'PARTITION',
    'over': 'OVER',
    'end': 'END',
    'then': 'THEN',
    'else': 'ELSE',
    'case': 'CASE',
    'when': 'WHEN',
    'with': 'WITH',
    'recursive': 'RECURSIVE',
    'all': 'ALL',
    'using': 'USING'
}

reserved = keywords | sort_orders | set_ops | logic_ops

tokens = [
             'ID',
             'NUMBER',
             'COMMA',
             'LPAREN',
             'RPAREN',
             'COMP_OP',
             'ARITH_OP',
             'DOT',
             'STRING',
             'STAR',
             'ORR',
             'MINUS',
             'DATE_LITERAL',
             'TYPE_NAME'
         ] + list(reserved.values())


def t_NUMBER(t):
    r'\b(?:\d+\.\d+)\b|\.\d+\b|\b(?:\d+)\b'
    if t.value.isdigit():
        t.value = int(t.value)
    else:
        t.value = float(t.value)
    return t


t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_STAR = r'\*'
t_DOT = r'\.'
t_ORR = r'\|\|'
t_MINUS = r'-'


def t_TYPE_NAME(t):
    r'\b(?:integer|int|float|real|unsigned|text|date|numeric|varchar|datetime|datetime2|time|char)\b'
    t.value = t.value.lower()
    return t


def t_DATE_LITERAL(t):
    r'\d{4}-\d{2}-\d{2}'  # Match dates in YYYY-MM-DD format
    return t


# r'\'[^\']*\'|\"[^\"]*\"'
def t_STRING(t):
    r"\'([^']|'')*\'|\"([^\"]|\"\")*\"|\`([^\`]|\`\`)*\`"
    val = str(t.value)
    val = val.replace("\"", "")
    val = val.replace("\'", "")
    val = val.replace("\''", "")
    val = val.replace("`", "")
    # val = val.lower()
    t.value = val
    return t


def t_ARITH_OP(t):
    r'[+/\%\^]'
    return t


def t_COMP_OP(t):
    r'!=|<>|>=|<=|=|>|<'
    return t


def t_ID(t):
    r'\[[^\[\]]+\]|\w+'
    if t.value.lower() in reserved:
        t.value = t.value.lower()
        t.type = reserved[t.value.lower()]
    else:
        t.value = t.value.lower()
        t.type = 'ID'  # Check for reserved words
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' '


# Error handling rule
def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def get_lexer():
    lexer = lex.lex(reflags=re.IGNORECASE)
    # lexer = lex.lex()
    return lexer
