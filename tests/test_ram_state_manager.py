import pytest

from n2t.core.ram_state_manager import RamStateManager
import n2t.definitions as definitions
import random


@pytest.fixture()
def state():
    return RamStateManager()


def test_empty_state(state) -> None:
    for index in range(definitions.RAM_SIZE):
        assert state.read(index) is None


def test_full_state(state) -> None:
    for index in range(definitions.RAM_SIZE):
        state.write(index, index)

    for index in range(definitions.RAM_SIZE):
        assert state.read(index) is not None


def test_random_states(state) -> None:
    random_indexes: list[int] = []

    for _ in range(100):
        index: int = random.randint(0, definitions.RAM_SIZE - 1)
        random_indexes.append(index)
        state.write(index, index)

    for index in random_indexes:
        assert state.read(index) == index


def test_get_ram_state(state) -> None:
    state.write(0, 100)

    assert state.get_ram_state()[0] == "RAM 0 -> bin: 0000000001100100 dec: 100"
    assert state.get_ram_state()[1] == "RAM 1 ->  "
