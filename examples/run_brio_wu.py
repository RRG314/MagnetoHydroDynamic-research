from mhd_toolkit.cli import main


if __name__ == "__main__":
    raise SystemExit(
        main([
            "run",
            "brio-wu",
            "--nx",
            "400",
            "--steps",
            "80",
            "--closure",
            "resistive",
            "--divfree",
            "none",
            "--output-dir",
            "results",
        ])
    )
