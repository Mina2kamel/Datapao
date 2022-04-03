from TheBigIMDBquest import WebScraping
import pytest
import pandas as pd
from bs4 import BeautifulSoup
import requests

#test Scraper function in pytest using fixtures tool
# @pytest.fixture(scope='module')
# def scraped_data():
#    scraped_data = WebScraping()
#    scraped_data.Scraper(url = "https://www.imdb.com/chart/top/")
#    return scraped_data


# def test_Scraper(scraped_data):
#     # expected
#    df_expected = pd.DataFrame(
#                        [['The Shawshank Redemption', 9.2,2568797,0],
#                         ['The Godfather', 9.2,1768532,3 ],
#                         ['The Dark Knight', 9.0,2533703,2]],
#                         index=[0,1,2],
#                         columns=['Title', 'Rating', 'Number of ratings','Number of Oscars'])
#    assert scraped_data.Scraper(url = "https://www.imdb.com/chart/top/").head(3).equals(df_expected)

 #test RatingAdjustment function in pytest using parameterization tool
@pytest.mark.parametrize("Number_of_ratings,Oscars,expected",

                        [[2568797,0,9.2],[1768532,3,8.9],[2533703,2,9.3]])

def test_RatingAdjustment(Number_of_ratings,Oscars,expected):
   assert WebScraping.RatingAdjustment(Number_of_ratings,Oscars)== expected
