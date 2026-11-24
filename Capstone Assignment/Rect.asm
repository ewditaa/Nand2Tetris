// Draws a rectangle at the top-left corner of the screen.
// The rectangle is 16 pixels wide and R0 pixels high.

   @0
   D=M
   @INFINITE_LOOP
   D;JLE            // if R0 <= 0 nothing to draw
   @counter
   M=D              // counter = R0
   @SCREEN
   D=A
   @address
   M=D              // address = 16384 (base address of the screen)
(LOOP)
   @address
   A=M
   M=-1             // RAM[address] = 1111111111111111
   @address
   D=M
   @32
   D=D+A
   @address
   M=D              // address += 32 (next row)
   @counter
   MD=M-1           // counter--
   @LOOP
   D;JGT            // if counter > 0 goto LOOP
(INFINITE_LOOP)
   @INFINITE_LOOP
   0;JMP
