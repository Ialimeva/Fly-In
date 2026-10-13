"""
Starting point of the program.

This module is the starting point of the program where
simulation is called and ran.
"""
from simulation import Simulation
from pydantic import ValidationError


def main() -> None:
    """Starting point of the program"""
    try:
        simulation: Simulation = Simulation()
        simulation.run()
    except ValidationError as e:
        print(
            "An error occured:\n"
            f"{e.errors()[0]['msg']}"
        )
        raise SystemExit(1)
    except (KeyboardInterrupt, EOFError):
        raise SystemExit
    except Exception as e:
        print(f"An error occured:\n{e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
