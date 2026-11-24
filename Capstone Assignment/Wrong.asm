// Deliberately WRONG program - used to test the error-message feature
// (also contains a duplicate label to test the warning feature)

@5
D=A
(START)
@10
D=D+Q
(START)
@x
M=D
FOO=BAR
@
0;JMP
