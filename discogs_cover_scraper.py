import os
import sys
import time
import string
import argparse
import urllib.request

import discogs_client
import pandas as pd

# Optionally place your token here
API_KEY = None
APP_NAME = "CoverScraper/1.0"

def download_cover(url, artist, cat_num):
    """
    Downloads cover art image from the given url and saves it to the 'images' directory.
    The image file will be named after the artist and catalogue number.
    """
    if not url:
        return

    if not os.path.exists("images"):
        os.makedirs("images")

    file_name = artist + "_" + cat_num + ".jpg"
    file_name = format_filename(file_name)
    file_path = os.path.join("images", file_name)

    try:
        urllib.request.urlretrieve(url, file_path)
    except Exception as e:
        print("Download Error!")
        print("URL: ", url, " Artist: ", artist, "Catalogue Number: ", cat_num)
        print("Error: ", e)
        return


def cover_art_url(artist_, catalogue_number):
    """
    Searches for the cover art image URL of the release with the given artist and catalogue number.
    """
    client = discogs_client.Client(APP_NAME, user_token=API_KEY)
    try:
        results = client.search(catalogue_number, artist=artist_)
        if results:
            return results[0].data['cover_image']
        else:
            return None
    except Exception as e:
        print("Search error! artist: ", artist_, ", catalogue_number: ", catalogue_number)
        print("Error: ", e)
        return None


def csv_to_dict(file_path):
    """
    Reads the CSV file at the given file path and returns its data as a list of dictionaries.
    """
    df = pd.read_csv(file_path)
    data = df.to_dict('records')
    return data


def format_filename(s):
    """
    Formats the given string into a valid filename.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    # I don't like spaces in filenames.
    filename = filename.replace(' ', '_')
    return filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="valid path to a csv file", type=str)
    parser.add_argument("-t", "--token", help="visit: https://www.discogs.com/settings/developers", type=str)
    args = parser.parse_args()

    if args.token:
        API_KEY = args.token
    elif API_KEY is None:
        print("Please specify a token from your Discogs account!")
        parser.print_usage()
        sys.exit(1)

    print("Welcome to the Discogs Cover Scraper!\n")
    data = csv_to_dict(args.csv)

    n = len(data) + 1
    pos = 0
    for item in data:
        catnum = item['catalogue_number']
        artist = item['artist']
        url = cover_art_url(artist, catnum)
        download_cover(url, artist, catnum)

        # time.sleep(0.15)
        pos += 1
        print("Downloaded Image: ", pos, "/", n)
