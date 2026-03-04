from mhd_toolkit.cli import main


if __name__ == "__main__":
    raise SystemExit(
        main([
            "divfree",
            "demo",
            "--problem",
            "orszag-tang",
            "--method",
            "projection,glm",
            "--nx",
            "128",
            "--ny",
            "128",
            "--output-dir",
            "results",
        ])
    )
