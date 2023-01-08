# Discogs Cover Scraper

This Python script allows you to search the Discogs database using artist and catalogue number, and download 
the corresponding cover art images. Simply provide a CSV file containing the relevant release information, 
and the script will do the rest.

## Getting Started

1. Create a new virtual environment and install the required dependencies:

```bash
python3 -m venv env
source env/bin/activate
pip3 install discogs_client pandas
```

2. Obtain a Discogs API key [here](https://www.discogs.com/settings/developers)

3. Download some cover art images by running the script with your API key and a CSV file containing the release information:

```bash
python3 discogs_cover_scraper.py example.csv -t YOURTOKEN
```

## Note

Modify the script appropriately to search for different criteria or customize the output. Enjoy!
