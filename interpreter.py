#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

BF_ALLOWED_SYMBOLS = '><+-.,[]'


def load_bf_code(filename):
    with open(filename) as f:
        return [
            command
            for command in f.read()
            if command in BF_ALLOWED_SYMBOLS
        ]


def main(input_filename):
    bf_code = load_bf_code(input_filename)

    array = [0] * 30000
    ptr = 0

    stack = []
    i = 0
    length = len(bf_code)
    while i < length:
        op = bf_code[i]

        if op == '>':
            ptr += 1
        elif op == '<':
            ptr -= 1
        elif op == '+':
            array[ptr] += 1
        elif op == '-':
            array[ptr] -= 1
        elif op == '.':
            sys.stdout.write(chr(array[ptr]))
        elif op == ',':
            array[ptr] = ord(sys.stdin.read(1))
        elif op == '[':
            if array[ptr]:
                stack.append(i)
            else:
                depth = 0
                while True:
                    op = bf_code[i]
                    if op == '[':
                        depth += 1
                    elif op == ']':
                        depth -= 1
                    if depth == 0:
                        break
                    i += 1

        elif op == ']':
            i = stack.pop() - 1

        i += 1


if __name__ == '__main__':
    main(*sys.argv[1:])
