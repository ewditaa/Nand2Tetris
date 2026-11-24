# Nand to Tetris – Capstone: Make the Computer Draw a Box

Nand to Tetris – I (ETCCNT301), School of Engineering & Technology, K.R. Mangalam University

- Name: _your name_
- Roll no.: ending in 06
- K (last two digits of roll no.): 6
- Box: starts at row 6, 20 rows tall, 48 pixels wide (3 words)
- Extra feature (K mod 3 = 0): labels and variables saved to symbols.txt

## Files

| File | What it is |
|---|---|
| `CPU.hdl`, `Memory.hdl`, `Computer.hdl` | Part A – the Hack computer |
| `assembler.py` | Part B – Hack assembler in Python |
| `Add.asm`, `Max.asm`, `Rect.asm`, `Pong.asm` | Test programs (and their `.hack` outputs) |
| `Wrong.asm` | Deliberately wrong program to test error messages and warnings |
| `Box.asm`, `Box.hack` | Part C – the box program and its output from my own assembler |

## How to use the assembler

    python assembler.py Add.asm      # writes Add.hack and symbols.txt
    python assembler.py Box.asm      # writes Box.hack

How it works:

1. **First reading** – remove comments, blank lines and spaces; record the ROM
   address of every label such as `(LOOP)`.
2. **Second reading** – translate every line to 16 bits. `@number` and
   `@symbol` become A-instructions; new variables get RAM addresses 16, 17, 18 ...
   C-instructions are built as `111 a cccccc ddd jjj` from lookup tables.

Extra features:

- Wrong lines print `Line N: invalid instruction ...` instead of crashing.
- A label defined twice prints a warning.
- All labels and variables with their addresses are saved to `symbols.txt`.

## Testing

Each of `Add`, `Max`, `Rect` and `Pong` was assembled with `assembler.py` and
compared with the output of the official assembler (no differences).

## Running the box

Load `Box.hack` in the CPU Emulator, set animation to "No animation", press and
hold a key on the keyboard: the box appears; release the key: it disappears.
