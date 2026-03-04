from mhd_toolkit.cli import main


if __name__ == "__main__":
    raise SystemExit(
        main([
            "compare",
            "closures",
            "--problem",
            "brio-wu",
            "--closures",
            "ideal,resistive,viscous",
            "--steps",
            "60",
            "--nx",
            "400",
            "--output-dir",
            "results",
        ])
    )
