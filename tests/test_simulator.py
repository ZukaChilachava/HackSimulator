import filecmp
import os

import pytest
from n2t.runner.cli import run_simulator
import n2t.definitions as definitions

CYCLES: dict[str, int] = {
    "SimpleAddAndStore": 6,
    "OperationsTest": 260,
    "FibonacciElement": 6000,
}

_TEST_FILES = ["SimpleAddAndStore", "OperationsTest", "FibonacciElement"]


@pytest.mark.parametrize("file", _TEST_FILES)
def test_simulate(file: str):
    run_simulator(os.path.join("tests", "test_files", f"{file}.hack"), CYCLES[file])

    assert filecmp.cmp(
        shallow=False,
        f1=str(
            os.path.join(
                os.path.dirname(definitions.N2T_DIRECTORY),
                "tests",
                "test_files",
                f"{file}.out",
            )
        ),
        f2=str(
            os.path.join(
                os.path.dirname(definitions.N2T_DIRECTORY),
                "tests",
                "test_files",
                f"{file}.cmp",
            )
        ),
    )
