import os

RAM_SIZE: int = 32768
A_INSTRUCTION: int = 0
C_INSTRUCTION: int = 1
N2T_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))

A_DEST_INDX: int = 10
D_DEST_INDX: int = 11
M_DEST_INDX: int = 12

A_INDX: int = 3

NULL = "000"
JGT = "001"
JEQ = "010"
JGE = "011"
JLT = "100"
JNE = "101"
JLE = "110"
JMP = "111"
