#!/usr/bin/env python3
from collections import namedtuple
import re
import sys


from outputs import stderr

def lex(characters, expressions):
    position = 0
    expressions = [TokenExpression(*e) for e in EXPRESSIONS]
    tokens = []
    lines = 1
    while position < len(characters):
        remainder = characters[position:]
        token = None
        for expression in expressions:
            token = expression.match(remainder)
            if token is not None:
                tokens.append(token)
                position += len(token.text)
                lines += token.text.count('\n')
                break

        if token is None:  # no expressions matched!
            line = re.match(r'([^\n]*)', remainder)
            if line is None:
                line =''
            else:
                line = line.group(0)
            stderr(f'Illegal character(s) {remainder[0]} on line {lines}:\n{line}\n')
            sys.exit(1)

    return tokens


class TokenExpression:
    def __init__(self, tag, regex):
        self.tag = tag
        self.regex = re.compile(regex)

    def match(self, characters, position=0):
        match = self.regex.match(characters, position)
        if match is not None:
            return LexToken(self.tag, match.group(0))

        return None


LexToken = namedtuple('MatchToken', 'tag text')


EXPRESSIONS = (
    ('SPACE',    r'([\t ]+)'),
    ('SPACE',    r'(\\\\\n)'),  # backslash at end of line, i.e. "continuation"
    ('EOL',      r'(\n)'),

    ('COMMENT',  r'(#[^\n]*)'),
    ('QUOTE',    r'''((?P<q>['"])[^\n(?P=q)]*(?P=q))'''),  # single
    ('QUOTE',    r'''((?P<q>['"]{3})[^(?P=q)]*(?P=q))'''),  # triple

    ('RESERVED', r'(None)\b'),
    ('RESERVED', r'(False)\b'),
    ('RESERVED', r'(True)\b'),
    ('RESERVED', r'(and)\b'),
    ('RESERVED', r'(as)\b'),
    ('RESERVED', r'(break)\b'),
    ('RESERVED', r'(continue)\b'),
    ('RESERVED', r'(del)\b'),
    ('RESERVED', r'(elif)\b'),
    ('RESERVED', r'(else)\b'),
    ('RESERVED', r'(except)\b'),
    ('RESERVED', r'(finally)\b'),
    ('RESERVED', r'(for)\b'),
    ('RESERVED', r'(if)\b'),
    ('RESERVED', r'(in)\b'),
    ('RESERVED', r'(is)\b'),
    ('RESERVED', r'(not)\b'),
    ('RESERVED', r'(or)\b'),
    ('RESERVED', r'(pass)\b'),
    ('RESERVED', r'(return)\b'),
    ('RESERVED', r'(while)\b'),
    ('RESERVED', r'(with)\b'),

    ('RESERVED', r'(:=)'),  # assignment
    ('RESERVED', r'([\(\)])'),  # parens grouping
    ('RESERVED', r'([\[\]])'),  # bracket grouping
    ('RESERVED', r'([\{\}])'),  # brace grouping
    ('RESERVED', r'([\+\-])'),  # plus/minus
    ('RESERVED', r'([\*/]{1,2})'),  # mult, div, exponent
    ('RESERVED', r'([<>]=?|[\!=]=)'),  # comparisons
    ('RESERVED', r'(:)'),  # colon

    ('RESERVED', r'([1-9][0-9]*)'),  # int
    ('NAME',  r'([A-Za-z_][A-Za-z_0-9]*)\b'),  # identifier
)


if __name__ == '__main__':
    main()
