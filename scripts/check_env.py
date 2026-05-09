from pathlib import Path


REQUIRED = [".env.example", "compose.yaml", "apps/api/pyproject.toml", "apps/worker/pyproject.toml"]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    missing = [item for item in REQUIRED if not (root / item).exists()]
    if missing:
        raise SystemExit(f"Missing required files: {', '.join(missing)}")
    print("Wayfinder environment scaffold looks ready.")


if __name__ == "__main__":
    main()
