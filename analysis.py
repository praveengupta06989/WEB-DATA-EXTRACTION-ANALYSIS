"""
TASK 5 - EXPLORATORY DATA ANALYSIS
Robust version: validates numeric columns before analysis.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "cleaned_books.csv"
OUTPUT_DIR = PROJECT_DIR / "output"
CHART_DIR = PROJECT_DIR / "charts"


def save_chart(path, title, xlabel, ylabel):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def main():
    if not DATA_FILE.exists():
        print("ERROR: cleaned_books.csv was not found.")
        print("Run main.py first.")
        raise SystemExit(1)

    df = pd.read_csv(DATA_FILE)

    # Ensure analysis columns are numeric.
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["price_gbp", "rating"]).copy()

    if df.empty:
        raise SystemExit(
            "ERROR: No valid numeric price/rating records are available."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)
    CHART_DIR.mkdir(exist_ok=True)

    summary = pd.DataFrame({
        "Metric": [
            "Total products",
            "Average price (£)",
            "Minimum price (£)",
            "Maximum price (£)",
            "Average rating",
            "5-star products",
            "1-star products",
        ],
        "Value": [
            len(df),
            round(df["price_gbp"].mean(), 2),
            round(df["price_gbp"].min(), 2),
            round(df["price_gbp"].max(), 2),
            round(df["rating"].mean(), 2),
            int((df["rating"] == 5).sum()),
            int((df["rating"] == 1).sum()),
        ],
    })

    rating_counts = (
        df["rating"].value_counts()
        .sort_index()
        .rename_axis("rating")
        .reset_index(name="product_count")
    )

    # Recreate price bands if needed after CSV round-trip.
    df["price_band"] = pd.cut(
        df["price_gbp"],
        bins=[-float("inf"), 10, 20, 30, float("inf")],
        labels=["Under £10", "£10-£20", "£20-£30", "Above £30"]
    )

    price_bands = (
        df["price_band"].value_counts()
        .sort_index()
        .rename_axis("price_band")
        .reset_index(name="product_count")
    )

    top_expensive = df.nlargest(10, "price_gbp")[
        ["title", "price_gbp", "rating", "availability_count"]
    ]

    summary.to_csv(OUTPUT_DIR / "summary_statistics.csv", index=False)
    rating_counts.to_csv(OUTPUT_DIR / "rating_distribution.csv", index=False)
    price_bands.to_csv(OUTPUT_DIR / "price_band_distribution.csv", index=False)
    top_expensive.to_csv(
        OUTPUT_DIR / "top_10_expensive_books.csv",
        index=False
    )

    # Price distribution.
    plt.figure(figsize=(9, 5))
    plt.hist(df["price_gbp"], bins=20)
    save_chart(
        CHART_DIR / "price_distribution.png",
        "Distribution of Book Prices",
        "Price (£)",
        "Number of Books"
    )

    # Rating distribution.
    plt.figure(figsize=(8, 5))
    df["rating"].value_counts().sort_index().plot(kind="bar")
    plt.xticks(rotation=0)
    save_chart(
        CHART_DIR / "rating_distribution.png",
        "Book Rating Distribution",
        "Rating",
        "Number of Books"
    )

    # Price bands.
    plt.figure(figsize=(8, 5))
    df["price_band"].value_counts().sort_index().plot(kind="bar")
    plt.xticks(rotation=20)
    save_chart(
        CHART_DIR / "price_bands.png",
        "Books by Price Band",
        "Price Band",
        "Number of Books"
    )

    # Price versus rating.
    plt.figure(figsize=(8, 5))
    plt.scatter(df["rating"], df["price_gbp"], alpha=0.6)
    save_chart(
        CHART_DIR / "price_vs_rating.png",
        "Price vs Rating",
        "Rating",
        "Price (£)"
    )

    excel_file = OUTPUT_DIR / "web_data_analysis.xlsx"

    with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)
        rating_counts.to_excel(writer, sheet_name="Ratings", index=False)
        price_bands.to_excel(writer, sheet_name="Price Bands", index=False)
        top_expensive.to_excel(
            writer, sheet_name="Top Expensive", index=False
        )

    highest = df.loc[df["price_gbp"].idxmax()]
    lowest = df.loc[df["price_gbp"].idxmin()]
    most_common_rating = int(df["rating"].mode().iloc[0])

    insights = f"""WEB DATA EXTRACTION & ANALYSIS - KEY INSIGHTS

Total products analysed: {len(df)}
Average price: £{df["price_gbp"].mean():.2f}
Minimum price: £{df["price_gbp"].min():.2f}
Maximum price: £{df["price_gbp"].max():.2f}
Average rating: {df["rating"].mean():.2f}/5
Most common rating: {most_common_rating}/5

Highest-priced book:
{highest["title"]} - £{highest["price_gbp"]:.2f}

Lowest-priced book:
{lowest["title"]} - £{lowest["price_gbp"]:.2f}
"""

    (OUTPUT_DIR / "key_insights.txt").write_text(
        insights,
        encoding="utf-8"
    )

    print()
    print("SUCCESS: EDA completed.")
    print(f"Records analysed: {len(df)}")
    print(f"Excel report: {excel_file}")
    print(f"Charts folder: {CHART_DIR}")


if __name__ == "__main__":
    main()
