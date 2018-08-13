#!/usr/bin/env python3

from lexer import LexToken
from outputs import stderr


class Result:
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __repr__(self):
        return f'Result({self.value}, {self.index})'


class Parser:
    def __call__(self, tokens, index):
        return None  # over ride!

    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return Process(self, function)


class ParserToken(Parser):
    def __init__(self, token):
        if isinstance(token, LexToken):
            self.token = token
        else:
            self.token = LexToken(*token)

    def __call__(self, tokens, index):
        token = tokens[index]  # expects LexToken
        if pos < len(tokens) and self._match(token):
            return Result(self.token.text, index + 1)

        return None

    def _match(self, token):
        return False  # over ride!


class ReservedToken(ParserToken):
    def _match(self, token):
        if token == self.token:
            return True
        return False


class NameToken(ParserToken):
    def _match(self, token):
        if token.tag == self.token.tag:
            return True
        return False


class Concat(Parser):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __call__(self, tokens, index):
        left_result = self.left(tokens, index)
        if left result is not None:
            right_result = self.right(tokens, left_result.index)
            if right_result is not None:
                value = (left_result.value, right_result.value)
                return Result(value, right_result.index)

        return None
