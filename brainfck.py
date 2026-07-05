#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} program.bf")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    code = "".join(c for c in f.read() if c in "><+-.,[]")

# Precompute matching brackets
stack = []
brackets = {}
for i, c in enumerate(code):
    if c == "[":
        stack.append(i)
    elif c == "]":
        if not stack:
            raise SyntaxError("Unmatched ]")
        j = stack.pop()
        brackets[i] = j
        brackets[j] = i

if stack:
    raise SyntaxError("Unmatched [")

tape = [0] * 30000
ptr = 0
pc = 0

while pc < len(code):
    c = code[pc]

    if c == ">":
        ptr += 1
        if ptr >= len(tape):
            tape.append(0)

    elif c == "<":
        ptr -= 1
        if ptr < 0:
            raise IndexError("Pointer moved before start of tape")

    elif c == "+":
        tape[ptr] = (tape[ptr] + 1) % 256

    elif c == "-":
        tape[ptr] = (tape[ptr] - 1) % 256

    elif c == ".":
        print(chr(tape[ptr]), end="")

    elif c == ",":
        ch = sys.stdin.read(1)
        tape[ptr] = ord(ch) if ch else 0

    elif c == "[":
        if tape[ptr] == 0:
            pc = brackets[pc]

    elif c == "]":
        if tape[ptr] != 0:
            pc = brackets[pc]

    pc += 1
