from n2t.core.command_processor import CommandProcessor
import n2t.definitions as definitions


def test_a_command():
    instructions: list[str] = [
        "0000000000000001",
        "0000000000000010",
        "0000000000000011",
        "0111111111111111",
    ]

    processor: CommandProcessor = CommandProcessor(instructions)

    for i in range(len(instructions)):
        processor.execute_current()
        assert processor.a_register == int(instructions[i], 2)


def test_destination_write():
    instructions: list[str] = [
        "1110111111000000",
        "1110111111001000",
        "1110111111010000",
        "1110111111100000",
        "1110101010100000",
        "1110101010111000",
        "1110111111011000",
        "1110111111101000",
        "1110101010110000",
    ]

    processor: CommandProcessor = CommandProcessor(instructions)

    processor.execute_current()
    assert (
        processor.a_register == 0
        and processor.d_register == 0
        and processor.ram_state.read(0) is None
    )

    processor.execute_current()
    assert (
        processor.a_register == 0
        and processor.d_register == 0
        and processor.ram_state.read(0) == 1
    )

    processor.execute_current()
    assert (
        processor.a_register == 0
        and processor.d_register == 1
        and processor.ram_state.read(0) == 1
    )

    processor.execute_current()
    assert (
        processor.a_register == 1
        and processor.d_register == 1
        and processor.ram_state.read(0) == 1
    )

    processor.execute_current()
    assert (
        processor.a_register == 0
        and processor.d_register == 1
        and processor.ram_state.read(0) == 1
    )

    processor.execute_current()
    assert (
        processor.a_register == 0
        and processor.d_register == 0
        and processor.ram_state.read(0) == 0
    )

    processor.execute_current()
    assert (
        processor.a_register == 0
        and processor.d_register == 1
        and processor.ram_state.read(0) == 1
    )

    processor.execute_current()
    assert (
        processor.a_register == 1
        and processor.d_register == 1
        and processor.ram_state.read(0) == 1
    )

    processor.execute_current()
    assert (
        processor.a_register == 0
        and processor.d_register == 0
        and processor.ram_state.read(0) == 1
    )


def test_comp_assignment():
    instructions: list[str] = [
        "0000000000000111",
        "1110110000010000",
        "1110001101100000",
        "1110111010010000",
        "1110110001001000",
        "1110001111010000",
        "1110110011001000",
        "1111110011001000",
        "1110011111100000",
        "1110110111010000",
        "1110001110001000",
        "1111110010010000",
        "1110000010101000",
        "1110010011010000",
        "1110000111100000",
        "1110001111010000",
        "1110000000001000",
        "1110010101001000",
    ]

    processor: CommandProcessor = CommandProcessor(instructions)

    processor.execute_current()
    processor.execute_current()
    assert processor.d_register == 7

    processor.execute_current()
    assert processor.a_register == 32760

    processor.execute_current()
    assert processor.d_register == -1

    processor.execute_current()
    assert processor.ram_state.read(32760) == 7

    processor.execute_current()
    assert processor.d_register == 1

    processor.execute_current()
    assert processor.ram_state.read(32760) == -32760

    processor.execute_current()
    assert processor.ram_state.read(32760) == 32760

    processor.execute_current()
    assert processor.a_register == 2

    processor.execute_current()
    assert processor.d_register == 3

    processor.execute_current()
    assert processor.ram_state.read(2) == 2

    processor.execute_current()
    assert processor.d_register == 1

    processor.execute_current()
    assert processor.a_register == 3 and processor.ram_state.read(2) == 3

    processor.execute_current()
    assert processor.d_register == -2

    processor.execute_current()
    assert processor.a_register == 5

    processor.execute_current()
    assert processor.d_register == 2

    processor.execute_current()
    assert processor.ram_state.read(5) == 0

    processor.execute_current()
    assert processor.ram_state.read(5) == 7


def test_jump():
    instructions: list[str] = ["0000000000000000", "1110110000000111"]

    processor: CommandProcessor = CommandProcessor(instructions)

    processor.execute_current()
    processor.execute_current()
    assert processor.stack_pointer == 0

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000110", False, definitions.JGT)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000000", False, definitions.JGT)
    )

    process_jump(processor)
    assert processor.stack_pointer == 4

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000000", False, definitions.JEQ)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", False, definitions.JEQ)
    )

    process_jump(processor)
    assert processor.stack_pointer == 4

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000000", False, definitions.JGE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", False, definitions.JGE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", True, definitions.JGE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 4

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", True, definitions.JLT)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000000", False, definitions.JLT)
    )

    process_jump(processor)
    assert processor.stack_pointer == 4

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", False, definitions.JLT)
    )

    process_jump(processor)
    assert processor.stack_pointer == 4

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", False, definitions.JNE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", True, definitions.JNE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000000", False, definitions.JNE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 4

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", True, definitions.JLE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000000", False, definitions.JLE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", False, definitions.JLE)
    )

    process_jump(processor)
    assert processor.stack_pointer == 4

    processor = CommandProcessor(
        assign_to_d_and_jump("0000000000000001", True, definitions.JMP)
    )

    process_jump(processor)
    assert processor.stack_pointer == 1


def assign_to_d_and_jump(value: str, negate: bool, jump: str) -> list[str]:
    return [
        value,
        "1110110011010000" if negate else "1110110000010000",
        "0000000000000001",
        f"1110001100000{jump}",
    ]


def process_jump(processor: CommandProcessor):
    processor.execute_current()
    processor.execute_current()
    processor.execute_current()
    processor.execute_current()
