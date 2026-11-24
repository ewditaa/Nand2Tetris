#!/usr/bin/env python3
"""Hack assembler: .asm -> .hack  (Nand to Tetris, Part B)

Usage:  python assembler.py Prog.asm        -> writes Prog.hack and symbols.txt

Extra features (all three included; the one for your K = K mod 3):
  0 -> symbols.txt with all labels and variables and their addresses
  1 -> clear error message with line number instead of crashing
  2 -> warning if the same label is defined twice
"""
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JLE": "101", "JNE": "110", "JMP": "111"}

SYMBOLS = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
           "SCREEN": 16384, "KBD": 24576}
SYMBOLS.update({"R%d" % i: i for i in range(16)})


class AsmError(Exception):
    pass


def clean(line):
    """Remove comments and ALL whitespace."""
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def c_instruction(text):
    dest, jump = "", ""
    comp = text
    if "=" in comp:
        dest, comp = comp.split("=", 1)
    if ";" in comp:
        comp, jump = comp.split(";", 1)
    # accept M+D / A+D style by swapping to the table's order
    if comp not in COMP and "+" in comp:
        a, b = comp.split("+")
        comp = b + "+" + a
    if comp not in COMP:
        raise AsmError("invalid instruction (bad comp '%s')" % comp)
    if dest not in DEST:
        raise AsmError("invalid instruction (bad dest '%s')" % dest)
    if jump not in JUMP:
        raise AsmError("invalid instruction (bad jump '%s')" % jump)
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def assemble(lines):
    symbols = dict(SYMBOLS)
    errors, warnings = [], []
    program = []                     # (source line number, cleaned text)

    # ---------- First reading: strip, find labels ----------
    for num, raw in enumerate(lines, start=1):
        text = clean(raw)
        if not text:
            continue
        if text.startswith("("):
            if not text.endswith(")") or len(text) < 3:
                errors.append("Line %d: invalid label '%s'" % (num, text))
                continue
            label = text[1:-1]
            if label in symbols:
                warnings.append(
                    "Warning: Line %d: label (%s) is defined more than once"
                    % (num, label))
            symbols[label] = len(program)      # address of next instruction
        else:
            program.append((num, text))

    # ---------- Second reading: translate ----------
    next_var = 16
    out = []
    for num, text in program:
        try:
            if text.startswith("@"):
                sym = text[1:]
                if not sym:
                    raise AsmError("invalid instruction (empty @)")
                if sym.isdigit():
                    value = int(sym)
                    if value > 32767:
                        raise AsmError("value %d too large for A-instruction"
                                       % value)
                else:
                    if sym not in symbols:
                        symbols[sym] = next_var
                        next_var += 1
                    value = symbols[sym]
                out.append(format(value, "016b"))
            else:
                out.append(c_instruction(text))
        except AsmError as e:
            errors.append("Line %d: %s" % (num, e))
    return out, symbols, errors, warnings


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        print("Usage: python assembler.py File.asm")
        sys.exit(1)
    path = sys.argv[1]
    try:
        with open(path) as f:
            lines = f.read().splitlines()
    except OSError as e:
        print("Cannot open file:", e)
        sys.exit(1)

    out, symbols, errors, warnings = assemble(lines)

    for w in warnings:                       # feature for K mod 3 == 2
        print(w)
    if errors:                               # feature for K mod 3 == 1
        for e in errors:
            print(e)
        print("Assembly failed: %d error(s). No .hack file written."
              % len(errors))
        sys.exit(1)

    with open(path[:-4] + ".hack", "w") as f:
        f.write("\n".join(out) + "\n")

    # feature for K mod 3 == 0
    with open("symbols.txt", "w") as f:
        for name, addr in sorted(symbols.items(), key=lambda kv: kv[1]):
            if name in SYMBOLS:
                continue                      # skip predefined symbols
            f.write("%s = %d\n" % (name, addr))
    print("Wrote %s.hack (%d instructions)" % (path[:-4], len(out)))


if __name__ == "__main__":
    main()
