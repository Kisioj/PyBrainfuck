#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys

BF_ALLOWED_SYMBOLS = '><+-.,[]'

C_FILE_TEMPLATE = """#include<stdio.h>

int main(void) {
\tchar array[30000] = {0};
\tchar *ptr = array + 15000;
%s
\treturn 0;
}
"""


def load_bf_code(filename):
    with open(filename) as f:
        return [
            command
            for command in f.read()
            if command in BF_ALLOWED_SYMBOLS
        ]


def preprocess_bf_code(raw_bf_code):
    bf_code = []
    indent = 1
    last_op = None
    for op in raw_bf_code:
        if op == ']':
            indent -= 1

        if op in '><+-' and op == last_op:
            bf_code[-1]['count'] += 1
        else:
            bf_code.append({'op': op, 'indent': indent, 'count': 1})

        if op == '[':
            indent += 1

        last_op = op
    return bf_code


def transpile_to_c(bf_code):
    c_code = []
    for record in bf_code:
        op = record['op']
        indent = record['indent']
        count = record['count']
        instr = ''

        if op == '>':
            instr = 'ptr += {};'.format(count) if count > 1 else 'ptr++;'
        elif op == '<':
            instr = 'ptr -= {};'.format(count) if count > 1 else 'ptr--;'
        elif op == '+':
            instr = '(*ptr) += {};'.format(count) if count > 1 else '(*ptr)++;'
        elif op == '-':
            instr = '(*ptr) -= {};'.format(count) if count > 1 else '(*ptr)--;'
        elif op == '.':
            instr = 'putchar(*ptr);'
        elif op == ',':
            instr = '(*ptr) = getchar();'
        elif op == '[':
            instr = 'while (*ptr) {'
        elif op == ']':
            instr = '}'

        c_code.append('\t' * indent + instr)
    return c_code


def save_c_code(filename, c_code):
    code = C_FILE_TEMPLATE % '\n'.join(c_code)
    with open(filename, 'w') as f:
        f.write(code)
        print(code)


def compile_c_code(filename):
    subprocess.call('gcc -x c {0} -o {0}'.format(filename), shell=True)


def main(input_filename, output_filename='a.out'):
    bf_code = load_bf_code(input_filename)
    bf_code = preprocess_bf_code(bf_code)
    c_code = transpile_to_c(bf_code)
    save_c_code(output_filename, c_code)
    compile_c_code(output_filename)


if __name__ == '__main__':
    main(*sys.argv[1:])
