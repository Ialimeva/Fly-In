from .model import Simulation


def main() -> None:
    try:
        simulation: Simulation = Simulation()
        simulation.run()
    except Exception as e:
        print(f"An error occured: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
