"""
TASK 5 - DATA CLEANING AND PREPROCESSING
Robust version: handles currency symbols/encoding and invalid numeric values.
"""

from pathlib import Path
import re
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

RAW_FILE = DATA_DIR / "raw_books.csv"
CLEAN_FILE = DATA_DIR / "cleaned_books.csv"


def extract_number(value):
    """Extract the first decimal number from a value such as £51.77 or Â£51.77."""
    if pd.isna(value):
        return None

    text = str(value).replace(",", "").strip()
    match = re.search(r"\d+(?:\.\d+)?", text)

    if match:
        return float(match.group())

    return None


def clean_data(df):
    df = df.copy()

    # Standardize column names.
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    required = {"title", "price_gbp", "rating", "availability", "product_url"}
    missing = required.difference(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    # Clean title.
    df["title"] = (
        df["title"].astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Robustly extract numeric price even if currency encoding is unusual.
    df["price_gbp"] = df["price_gbp"].apply(extract_number)

    # Convert rating robustly.
    rating_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5
    }

    def convert_rating(value):
        if pd.isna(value):
            return None

        text = str(value).strip().lower()

        if text in rating_words:
            return rating_words[text]

        number = extract_number(text)
        if number is not None and 1 <= number <= 5:
            return int(number)

        return None

    df["rating"] = df["rating"].apply(convert_rating)

    # Clean availability.
    df["availability"] = (
        df["availability"].astype("string")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df["availability_count"] = pd.to_numeric(
        df["availability"].str.extract(r"(\d+)")[0],
        errors="coerce"
    )

    # Remove duplicate product URLs.
    df = df.drop_duplicates(subset="product_url")

    # Remove records where required analysis fields cannot be recovered.
    df = df.dropna(subset=["title", "price_gbp", "rating"])

    # Ensure correct numeric types.
    df["price_gbp"] = df["price_gbp"].astype(float)
    df["rating"] = df["rating"].astype(int)
    df["availability_count"] = (
        df["availability_count"].fillna(0).astype(int)
    )

    # Derived analysis fields.
    df["price_band"] = pd.cut(
        df["price_gbp"],
        bins=[-float("inf"), 10, 20, 30, float("inf")],
        labels=["Under £10", "£10-£20", "£20-£30", "Above £30"]
    )

    df["rating_label"] = df["rating"].map({
        1: "1 Star",
        2: "2 Stars",
        3: "3 Stars",
        4: "4 Stars",
        5: "5 Stars"
    })

    return df.reset_index(drop=True)


def main():
    if not RAW_FILE.exists():
        print("ERROR: raw_books.csv was not found.")
        print("Run main.py to collect the web data first.")
        raise SystemExit(1)

    try:
        raw = pd.read_csv(RAW_FILE)

        print(f"Raw records found: {len(raw)}")

        cleaned = clean_data(raw)

        if cleaned.empty:
            raise ValueError(
                "No valid records remained after cleaning. "
                "Check data/raw_books.csv."
            )

        cleaned.to_csv(
            CLEAN_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"SUCCESS: {len(cleaned)} cleaned records.")
        print(f"Saved to: {CLEAN_FILE}")

    except Exception as error:
        print(f"ERROR during data cleaning: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
