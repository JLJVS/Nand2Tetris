// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.

@8191
D=A
@i
M=D
@KBD
D=M
@LOOPWHITE
D;JEQ
@LOOPBLACK
D;JGT

(LOOPBLACK)
@i
D=M
@END
D;JLT
@SCREEN
A=D+A
M=-1
@i
M=M-1
@LOOPBLACK
0;JMP

(LOOPWHITE)
@i
D=M
@END
D;JLT
@SCREEN
A=D+A
M=0
@i
M=M-1
@LOOPWHITE
0;JMP


(END)
@0
0;JMP