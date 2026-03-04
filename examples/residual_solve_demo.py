from mhd_toolkit.cli import main


if __name__ == "__main__":
    raise SystemExit(
        main([
            "opt",
            "residual-demo",
            "--nx",
            "40",
            "--ny",
            "40",
            "--steps",
            "300",
            "--output-dir",
            "results",
        ])
    )
