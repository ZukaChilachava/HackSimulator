import typer
from typer import Typer, echo

from n2t.infra.simulator import Simulator

cli = Typer(
    name="Nand 2 tetris simulator",
    no_args_is_help=True,
    add_completion=False,
)


@cli.command("execute", no_args_is_help=True)
def run_simulator(hack_file: str, cycles: int = typer.Option(...)) -> None:
    echo(f"Simulating hack instructions (⌐■_■) {hack_file}")
    Simulator.load_from(hack_file, cycles).translate()
    echo("Simulation done (づ ◕‿◕ )づ")


@cli.callback()
def callback() -> None:
    pass
