import os
import csv
import shutil
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from google_images_download import google_images_download

def download_images_by_url(output_dir, url, limit):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    response = google_images_download.googleimagesdownload()
    response.download({
                      "similar_images": url,
                      "color_type": "transparent",
                      "size": "medium",
                      "limit": limit,
                      "output_directory": output_dir,
                      "chromedriver": "/usr/local/bin/chromedriver"})

def download_images_by_keyword(output_dir, keyword, limit):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    response = google_images_download.googleimagesdownload()
    response.download({
                      "keywords": keyword,
                      "color_type": "transparent",
                      "size": "medium",
                      "limit": limit,
                      "output_directory": output_dir,
                      "chromedriver": "/usr/local/bin/chromedriver"})


def download_images_by_csv_line(output_dir, subdir1, url, limit1, keyword, limit2):
    output_dir+=subdir1
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    response = google_images_download.googleimagesdownload()
    response.download({
                      "similar_images": url,
                      "color_type": "transparent",
                      "size": "medium",
                      "limit": limit1,
                      "output_directory": output_dir,
                      "chromedriver": "/usr/local/bin/chromedriver"})
    response = google_images_download.googleimagesdownload()
    response.download({
                  "keywords": keyword,
                  "color_type": "transparent",
                  "size": "medium",
                  "limit": limit2,
                  "output_directory": output_dir,
                  "chromedriver": "/usr/local/bin/chromedriver"})


if __name__ == "__main__":
    #output_dir = os.path.join("data", "n0001_0000083")
    #download_images_by_url(output_dir,'https://images-eu.ssl-images-amazon.com/images/I/319xdE7YONL._AC_US1150_.jpg', 50)
    #download_images_by_keyword
    #output_dir2 = os.path.join("data2", "n0001_0000083")
    #download_images_by_keyword(output_dir2, "uriage depiderm spf 50 anti-brown spot daytime care", 50)
    ids = []
    urls = []
    labels = []
    #s1 = np.random.poisson(13, 30)
    #s2 = np.random.poisson(4, 30)
    with open('./part2.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        counter = 0
        for row in csvReader:
            ids.append(row[0])
            urls.append(row[1])
            labels.append(row[2])
            download_images_by_csv_line('./data_part2/', row[0], row[1], 25, row[2], 5)
