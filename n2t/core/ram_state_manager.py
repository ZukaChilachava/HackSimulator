from typing import Optional

import n2t.definitions as definitions


class RamStateManager:
    def __init__(self) -> None:
        self.ram: list[Optional[int]] = [None] * definitions.RAM_SIZE

    def read(self, index: int) -> Optional[int]:
        return self.ram[index]

    def write(self, index: int, value: int) -> None:
        self.ram[index] = value

    def get_ram_state(self) -> list[str]:
        ram_state: list[str] = []
        for index, value in enumerate(self.ram):
            binary: str = ""
            if value is not None:
                binary = "0" if value >= 0 else "1"
                binary += format(abs(value), "015b")

            ram_state.append(
                f"RAM {index} -> "
                f"{' ' if value is None else 'bin: ' + binary + ' dec: ' + str(value)}"
            )

        return ram_state
