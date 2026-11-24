// Box.asm  -  K = 6
// Box: starts at row 6, 20 rows tall, 48 pixels wide (3 word(s)).
// Black while any key is pressed, white when released.
// First screen word of box = SCREEN + 32*6 = 16576

(LOOP)
    @KBD
    D=M
    @DRAW
    D;JNE           // key pressed -> draw black
    @color
    M=0             // no key -> colour white
    @PAINT
    0;JMP
(DRAW)
    @color
    M=-1            // all 16 bits = 1 = black
(PAINT)
    @16576
    D=A
    @addr           // addr = first word of current row
    M=D
    @20
    D=A
    @rows           // rows left to paint
    M=D
(ROWLOOP)
    @3
    D=A
    @cols           // words left in this row
    M=D
    @addr
    D=M
    @p              // p = word being painted
    M=D
(COLLOOP)
    @color
    D=M
    @p
    A=M
    M=D             // RAM[p] = colour
    @p
    M=M+1
    @cols
    M=M-1
    D=M
    @COLLOOP
    D;JGT
    @32
    D=A
    @addr
    M=D+M           // move down one screen row
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @LOOP
    0;JMP
