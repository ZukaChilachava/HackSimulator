from n2t.core.hack_simulator import HackSimulator


def test_hack_simulator():
    result: list[str] = HackSimulator.simulate(
        [
            "0000000000000010",
            "1110110000010000",
            "0000000000000011",
            "1110000010010000",
            "0000000000000000",
            "1110001100001000",
        ],
        6,
    )

    assert result[0] == "RAM 0 -> bin: 0000000000000101 dec: 5"
