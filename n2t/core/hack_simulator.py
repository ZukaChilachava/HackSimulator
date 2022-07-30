from n2t.core.command_processor import CommandProcessor


class HackSimulator:
    @staticmethod
    def simulate(instructions: list[str], cycles: int) -> list[str]:
        command_processor: CommandProcessor = CommandProcessor(instructions)

        for _ in range(cycles):
            command_processor.execute_current()

        result: list[str] = command_processor.ram_state.get_ram_state()
        return result
