# WEB DATA EXTRACTION & ANALYSIS
## TASK 5 PROJECT REPORT

### 1. Introduction

This project demonstrates an end-to-end web data extraction and analytics workflow using Python. Publicly available book information is collected from Books to Scrape, an educational website designed for web-scraping practice.

### 2. Objectives

- Collect publicly available web data.
- Extract structured product information.
- Create a dataset from scraped information.
- Clean and organize the data.
- Perform exploratory data analysis.
- Identify price and rating patterns.
- Generate visualizations.
- Export results to CSV and Excel.
- Automate the complete process.

### 3. Technologies

- Python
- Requests
- BeautifulSoup
- Pandas
- Matplotlib
- OpenPyXL
- VS Code

### 4. Data Collected

The project extracts:

- Book title
- Price
- Rating
- Availability
- Product URL

Derived fields:

- Availability count
- Price band
- Rating label

### 5. Methodology

#### Web Scraping
Requests downloads the website HTML and BeautifulSoup parses the page structure.

#### Data Extraction
The scraper identifies product containers and extracts title, price, rating, availability and URL.

#### Pagination
The scraper automatically follows the next-page link until the catalogue is completed.

#### Data Cleaning
Pandas converts prices and ratings into numeric values, removes duplicate product URLs, handles missing values and creates useful derived fields.

#### Exploratory Analysis
The project calculates average, minimum and maximum price, average rating, rating distribution, price-band distribution and top-priced products.

#### Visualization
Four charts are generated:

1. Price distribution
2. Rating distribution
3. Price-band distribution
4. Price versus rating

#### Export
The cleaned dataset and analytical summaries are exported to CSV and Excel.

### 6. Automation

`main.py` executes the complete workflow:

Web scraping → Data cleaning → EDA → CSV/Excel export → Charts

`run_project.bat` provides a Windows one-click option.

### 7. Conclusion

The project demonstrates practical skills in web scraping, structured data extraction, data preprocessing, exploratory analysis, visualization, automation and data export. It extends previous dataset-based tasks by generating the dataset directly from a public website.

### 8. Ethical Considerations

The project uses a public educational website intended for scraping practice. It does not bypass authentication, access controls or other restrictions. A short delay is included between page requests.
