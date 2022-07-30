from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from n2t import definitions
from n2t.core.hack_simulator import HackSimulator


@dataclass
class Simulator:
    cycles: int
    file_name: str
    file_path: Path
    path_to_dir: str

    @classmethod
    def load_from(cls, file_name: str, cycles: int) -> Simulator:
        if not os.path.isabs(file_name):
            file_name = os.path.join(
                os.path.dirname(definitions.N2T_DIRECTORY),
                file_name,
            )
        file_path: Path = Path(file_name)
        file_name = file_path.stem
        path_to_dir = os.path.dirname(file_path)

        return cls(cycles, file_name, file_path, path_to_dir)

    def translate(self) -> None:
        to_simulate: list[str] = []

        with self.file_path.open("r", newline="") as file:
            for line in file:
                to_simulate.append(line)

        ram_output: list[str] = HackSimulator.simulate(to_simulate, self.cycles)

        new_path: Path = Path(os.path.join(self.path_to_dir, self.file_name + ".out"))

        with new_path.open("w", newline="") as file:
            for current_ram in ram_output:
                file.write(f"{current_ram}\n")
