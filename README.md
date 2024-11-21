# Toilet Paper Market Scraper

A comprehensive web scraping tool that collects toilet paper product information from multiple e-commerce and industry-specific websites.

## Features

- Scrapes product information from 14 different websites:
  - Major E-commerce: Amazon, Walmart, Alibaba, Made-in-China, Global Sources, Trade India
  - Industry-specific: ThomasNet, Tissue World, RISI Info
  - Corporate: Kimberly-Clark, P&G, Essity
  - Sustainability: Good On You, Environmental Paper

- Collects the following information for each product:
  - Brand name
  - Price (where available)
  - Normalized price for comparison
  - Source website
  - Product link

- Outputs data in both JSON and human-readable text formats
- Implements automatic price normalization
- Handles different website structures and loading patterns
- Includes error handling and retry mechanisms

## Requirements

- Python 3.8+
- Chrome browser installed
- Required Python packages listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Make sure you have Chrome browser installed

## Usage

Run the script:
```bash
python tpapescrappyVXX.py
```

The script will:
1. Initialize a Chrome WebDriver
2. Scrape data from all configured websites
3. Save results in two formats:
   - `toilet_paper_data.json`: Raw JSON data
   - `toilet_paper_data.txt`: Human-readable format

## Output Files

- `toilet_paper_data.json`: Contains the raw scraped data in JSON format
- `toilet_paper_data.txt`: A formatted text file with products sorted by price

## Error Handling

The script includes:
- Exception handling for missing elements
- Automatic retries for failed requests
- Timeouts for slow-loading pages
- Graceful handling of missing prices or information

## Notes

- Some websites may require authentication or have anti-scraping measures
- Corporate websites typically don't display prices directly
- Price normalization attempts to convert all prices to a common format
- Scraping speed is intentionally throttled to respect website resources

## Legal Notice

This tool is for educational purposes only. Before using it, ensure you comply with each website's terms of service and robots.txt policies.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
