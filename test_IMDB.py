"""Testing the Web scrapping app
"""
import unittest
import requests
from bs4 import BeautifulSoup
from imdb import WebScraping


class Testing(unittest.TestCase):
   soup = None
   def setUpClass():
      '''Initalize the resources before testing'''

      url = "https://www.imdb.com/chart/top/"
      Testing.soup = BeautifulSoup(requests.get(url).content, 'html.parser')

   def test_titletext(self):
      '''Test the first function By scraping the Page title'''

      page_title = Testing.soup.find('h1').get_text()
      self.assertEqual('IMDb Top 250 Movies', page_title)

   def test_ratingnumber_firstmovie(self):
      '''Testing the first function by scarping therating of "The Shawshank Redemption" movie'''

      rating = Testing.soup.find("td",{"class":"ratingColumn imdbRating"}).text.replace('\n',"")
      self.assertEqual(str(9.2), rating)

   def test_ratingadjustment(self):
      '''
      Testing the second function and check the adjusted rating
      '''

      data = WebScraping()
      rating=[9.2,9.2,9.0]
      number_of_rating=[2568797,1768532,2533703]
      oscars=[0,3,2]
      expected_rating=[9.2,8.9,9.3]
      self.assertEqual(data.rating_adjustment(rating,number_of_rating,oscars),expected_rating)

if __name__ == '__main__':
   unittest.main()