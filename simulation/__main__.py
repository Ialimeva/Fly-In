def main() -> None:
    try:
        print("Running")
    except Exception as e:
        print(f"An error occured: {e}")
        raise SystemExit


if __name__ == "__main__":
    main()