from TheBigIMDBquest import WebScraping
import pytest


@pytest.fixture(scope='module')
def scraped_data():
     scraped_data = WebScraping()
     scraped_data.Scraper(url = "https://www.imdb.com/chart/top/")
     return scraped_data
def test_ForrestGump_Movie(scraped_data):
     adjusted_rating = scraped_data.RatingAdjustment()
     assert adjusted_rating[0]==9.2


