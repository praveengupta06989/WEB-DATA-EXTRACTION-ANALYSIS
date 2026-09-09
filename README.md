# WEB DATA EXTRACTION & ANALYSIS

## Ready-to-run VS Code project

### Website
Books to Scrape:
https://books.toscrape.com/

This is a public educational website intended for web-scraping practice.

### What the project does

1. Collects book data using Requests and BeautifulSoup.
2. Extracts title, price, rating, availability and product URL.
3. Cleans and structures the dataset with Pandas.
4. Performs exploratory data analysis.
5. Generates four charts.
6. Exports CSV files and an Excel workbook.
7. Provides one-click automation with `main.py` or `run_project.bat`.

### Files

- `main.py` - complete pipeline
- `scraper.py` - web scraping
- `data_cleaning.py` - preprocessing
- `analysis.py` - EDA and charts
- `requirements.txt` - libraries
- `run_project.bat` - Windows one-click runner
- `project_report.md` - report for submission

### Recommended way to run on Windows

1. Keep the complete project folder on the Desktop.
2. Open the folder in VS Code.
3. Open Terminal.
4. Run:

```powershell
python -m pip install -r requirements.txt
```

5. Then run:

```powershell
python main.py
```

### Output

After a successful run:

`data/`
- raw_books.csv
- cleaned_books.csv

`output/`
- web_data_analysis.xlsx
- summary_statistics.csv
- rating_distribution.csv
- price_band_distribution.csv
- top_10_expensive_books.csv
- key_insights.txt

`charts/`
- price_distribution.png
- rating_distribution.png
- price_bands.png
- price_vs_rating.png

### Important

Run the project while connected to the internet because the scraper collects live data from the public website.
