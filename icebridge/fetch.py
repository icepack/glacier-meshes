
import argparse
import os, os.path
import re as regex
import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import progressbar

url = "https://data.cresis.ku.edu/data/rds/"

def get_urls(region, start_year, final_year):
    page = requests.get(url)
    if not page.ok:
        print("Couldn't access CReSIS!")

    content = BeautifulSoup(page.content, 'html.parser')
    r = regex.compile("Greenland|Antarctica" if region=="All" else region)
    seasons = [season for season in content.find_all("a", href=r, text=r)
               if start_year <= int(season.text[:4]) <= final_year]

    urls = []
    print("Exploring CReSIS website for available elevation data. "
          "{} seasons found.".format(len(seasons)))
    progress = progressbar.ProgressBar()
    for season in progress(seasons):
        season_url = urljoin(urljoin(url, season['href']), "csv_good/")
        season_page = requests.get(season_url)
        if season_page.ok:
            season_content = BeautifulSoup(season_page.content, 'html.parser')
            season_segments = season_content.find_all(
                "a", href=regex.compile("csv"), text=regex.compile("Data"))

            for segment in season_segments:
                segment_url = urljoin(season_url, segment['href'])
                urls.append(segment_url)

    print("Done exploring CReSIS website. {} files found.".format(len(urls)))
    return urls


def fetch_url(url):
    directory = url.split('/')[-3]
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = os.path.join(directory, url.split('/')[-1])
    if not os.path.exists(filename):
        segment = requests.get(url, stream=True)
        if not segment.ok:
            return False

        with open(filename, 'wb') as csv_file:
            for chunk in segment.iter_content(chunk_size=1024):
                csv_file.write(chunk)

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", default="all",
        help="Geographical region; either 'Greenland', 'Antarctica' or 'all'")
    parser.add_argument("--start", type=int, default=0,
        help="Starting year to fetch data from")
    parser.add_argument("--final", type=int, default=4000,
        help="Final year (inclusive) to fetch data from")
    args = parser.parse_args()

    urls = get_urls(args.region.title(), args.start, args.final)
    print("Downloading elevation data from CReSIS (skipping existing files).")
    progress = progressbar.ProgressBar()

    failures = []
    for url in progress(urls):
        result = fetch_url(url)
        if not result:
            failures.append(url)

    print("Done downloading elevation data from CReSIS.")
    if failures:
        print("The following segments could not be downloaded:")
        print("\n".join(failures))
