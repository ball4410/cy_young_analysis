from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
        executable_path = {'executable_path': ChromeDriverManager().install()}
        browser = Browser('chrome', **executable_path, headless=False)
        # news_title, news_paragraph = mars_news(browser)
        
        data = {
        # "news_title": news_title,
        # "news_paragraph": news_paragraph,
        # "featured_image": featured_image(browser),
        "predictions": espn_predictions()
        }       
        browser.quit()
        return data

def espn_predictions():
    # url = "https://www.espn.com/mlb/features/cyyoung"

    # tables = pd.read_html(requests.get(url).text)
    # df = tables[0]

    df = pd.read_html("https://www.espn.com/mlb/features/cyyoung")[0]

    al_df = df.iloc[1:12:]
    nl_df = df.iloc[13:]

    new_header = al_df.iloc[0] #grab the first row for the header
    al_df = al_df[1:] #take the data less the header row
    al_df.columns = new_header

    new_header = nl_df.iloc[0] #grab the first row for the header
    nl_df = nl_df[1:] #take the data less the header row
    nl_df.columns = new_header

    frames = [al_df, nl_df]
    po_df = pd.concat(frames)

    po_df = po_df.sort_values(by = ["CYP"], ascending=False)
    po_df = po_df.reset_index(drop = True)

    return po_df.to_html(classes="table table-striped table-sm")