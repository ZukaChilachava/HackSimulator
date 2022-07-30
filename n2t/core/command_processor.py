import n2t.definitions as definitions
from n2t.core.ram_state_manager import RamStateManager


class CommandProcessor:
    def __init__(self, instructions: list[str]):
        self.a_register = 0
        self.d_register = 0
        self.stack_pointer: int = 0
        self.instructions = instructions
        self.ram_state = RamStateManager()

    def execute_current(self) -> None:
        instruction_type: int = self.__get_current_instruction_type()
        current_instruction: str = self.__get_current_instruction_value()

        if instruction_type == definitions.A_INSTRUCTION:
            self.a_register = self.__binary_to_decimal()
            self.stack_pointer += 1
        else:
            comp: int = self.__get_comp_value(
                current_instruction[3], current_instruction[4:10]
            )
            self.__write_to_dest(current_instruction[10:13], comp)
            self.stack_pointer = self.__get_jump_location(
                current_instruction[13:16], comp
            )

    def __get_current_instruction_type(self) -> int:
        current_instruction: str = self.__get_current_instruction_value()

        result: int = (
            definitions.A_INSTRUCTION
            if current_instruction[0] == "0"
            else definitions.C_INSTRUCTION
        )
        return result

    def __write_to_dest(self, dest: str, comp: int) -> None:
        if dest[2] == "1":
            self.ram_state.write(self.a_register, comp)

        if dest[0] == "1":
            self.a_register = comp

        if dest[1] == "1":
            self.d_register = comp

    def __get_comp_value(self, a: str, comp: str) -> int:
        result: int = -1
        if comp == "111111":
            result = 1
        elif comp == "101010":
            result = 0
        elif comp == "111010":
            result = -1
        elif comp == "001100":
            result = self.d_register
        elif comp == "110000":
            # A or M
            result = (
                self.a_register if a == "0" else self.ram_state.read(self.a_register)
            )
        elif comp == "001101":
            result = 32767 - self.d_register
        elif comp == "110001":
            result = (
                32767 - self.a_register
                if a == "0"
                else 32767 - self.ram_state.read(self.a_register)
            )

        elif comp == "001111":
            result = -1 * self.d_register
        elif comp == "110011":
            result = (
                -1 * self.a_register
                if a == "0"
                else -1 * self.ram_state.read(self.a_register)
            )
        elif comp == "011111":
            result = self.d_register + 1
        elif comp == "110111":
            result = (
                self.a_register + 1
                if a == "0"
                else self.ram_state.read(self.a_register) + 1
            )
        elif comp == "001110":
            result = self.d_register - 1
        elif comp == "110010":
            result = (
                self.a_register - 1
                if a == "0"
                else self.ram_state.read(self.a_register) - 1
            )
        elif comp == "000010":
            result = (
                self.d_register + self.a_register
                if a == "0"
                else self.d_register + self.ram_state.read(self.a_register)
            )
        elif comp == "010011":
            result = (
                self.d_register - self.a_register
                if a == "0"
                else self.d_register - self.ram_state.read(self.a_register)
            )
        elif comp == "000111":
            result = (
                self.a_register - self.d_register
                if a == "0"
                else self.ram_state.read(self.a_register) - self.d_register
            )
        elif comp == "000000":
            result = (
                self.a_register & self.d_register
                if a == "0"
                else self.ram_state.read(self.a_register) & self.d_register
            )
        elif comp == "010101":
            result = (
                self.a_register | self.d_register
                if a == "0"
                else self.ram_state.read(self.a_register) | self.d_register
            )

        return result

    def __get_jump_location(self, jump: str, comp: int) -> int:
        next_pos: int = self.stack_pointer + 1
        result: int = -1

        if jump == definitions.NULL:
            result = next_pos
        elif jump == definitions.JGT:
            result = self.a_register if comp > 0 else next_pos
        elif jump == definitions.JEQ:
            result = self.a_register if comp == 0 else next_pos
        elif jump == definitions.JGE:
            result = self.a_register if comp >= 0 else next_pos
        elif jump == definitions.JLT:
            result = self.a_register if comp < 0 else next_pos
        elif jump == definitions.JNE:
            result = self.a_register if comp != 0 else next_pos
        elif jump == definitions.JLE:
            result = self.a_register if comp <= 0 else next_pos
        elif jump == definitions.JMP:
            result = self.a_register

        return result

    def __binary_to_decimal(self) -> int:
        return int(self.__get_current_instruction_value(), 2)

    def __get_current_instruction_value(self) -> str:
        return self.instructions[self.stack_pointer]
