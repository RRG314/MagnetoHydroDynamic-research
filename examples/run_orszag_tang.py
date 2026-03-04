from mhd_toolkit.cli import main


if __name__ == "__main__":
    raise SystemExit(
        main([
            "run",
            "orszag-tang",
            "--nx",
            "128",
            "--ny",
            "128",
            "--steps",
            "40",
            "--divfree",
            "projection",
            "--output-dir",
            "results",
        ])
    )
