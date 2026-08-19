"""
TASK 5 - COMPLETE AUTOMATED PIPELINE
"""

from pathlib import Path
import subprocess
import sys

PROJECT_DIR = Path(__file__).resolve().parent


def run_script(script_name):
    script_path = PROJECT_DIR / script_name

    if not script_path.exists():
        raise FileNotFoundError(f"Missing project file: {script_name}")

    print(f"\nRunning {script_name}...")
    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_DIR),
        check=True
    )


def main():
    print("=" * 65)
    print("WEB DATA EXTRACTION & ANALYSIS - TASK 5")
    print("=" * 65)

    try:
        run_script("scraper.py")
        run_script("data_cleaning.py")
        run_script("analysis.py")

    except subprocess.CalledProcessError as error:
        print("\nPROJECT STOPPED because one step failed.")
        print(f"Failed script exit code: {error.returncode}")
        raise SystemExit(1)

    except Exception as error:
        print(f"\nPROJECT ERROR: {error}")
        raise SystemExit(1)

    print("\n" + "=" * 65)
    print("PROJECT COMPLETED SUCCESSFULLY")
    print("=" * 65)
    print("\nCheck:")
    print("  data\\raw_books.csv")
    print("  data\\cleaned_books.csv")
    print("  output\\web_data_analysis.xlsx")
    print("  output\\key_insights.txt")
    print("  charts\\")


if __name__ == "__main__":
    main()
