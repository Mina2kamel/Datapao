"""
IMBD web scarping app
"""
import math
import requests
import pandas as pd
from bs4 import BeautifulSoup

class WebScraping():
    '''
       Web scraping class for IMDB movies
    '''
    
    def __init__(self):
        '''
            Initialize the Class attributes
        '''
        self.title_name = []
        self.rating =[]
        self.number_of_ratings = []
        self.oscars=[]
        self.adjusted_rating=[]


    def scraper(self, url):
        '''
        Scrape web data for TOP 20 IMDB movies
        Arguments:
            url : link of the IMDB website
        return :
            Pandas df object
        '''

        headers = {'Accept-Language': 'en-US,en;q=0.8'}
        soup = BeautifulSoup(requests.get(url,headers=headers).content, "html.parser")
        scraped_movies = soup.find("tbody", {"class":"lister-list"}).find_all("tr")
        for movie in scraped_movies[:20]:
            title=  movie.find("td",class_="titleColumn").a.text
            rating = movie.find("td",{"class":"ratingColumn"}).text
            rat_num= movie.find('span',attrs = {'name':'nv'})['data-value']
            self.title_name.append(title)
            self.rating.append(float(rating))
            self.number_of_ratings.append(int(rat_num))
            for value in movie.a.attrs.values():
                url = "https://www.imdb.com" + value
                soup = BeautifulSoup(requests.get(url).content,"html.parser")
                oscar = soup.find("ul",class_ ="ipc-metadata-list ipc-metadata-list--dividers-none sc-fcdc3619-2 kTHpcg ipc-metadata-list--base").a.text
                if oscar[0:3]=="Won":
                    self.oscars.append(int(oscar[4]))
                else:
                    self.oscars.append(0)
        df = pd.DataFrame(list(zip(self.title_name,self.rating,self.number_of_ratings,self.oscars)),
                               columns=['Title','Rating','Number of ratings','Number of Oscars'])

        return df


    def rating_adjustment(self, rating, number_of_ratings, oscars):
        '''
        Modify Movie rating according to the number of ratings
        and number of oscars

        '''

        num_rating=[]
        benchmark = max(number_of_ratings)
        for index,num in enumerate(number_of_ratings):
            deviation = math.floor((benchmark-num)/100000.0)
            penalty = float(format(deviation *0.1, ".1f"))
            pen_rating= rating[index]-penalty
            num_rating.append(pen_rating)

        for index , num in enumerate(oscars):
            if num==0:
                oscar_rating = num_rating[index]
            elif num in range(1,3):
                oscar_rating = num_rating[index]+0.3
            elif num in range(3,6):
                oscar_rating  = num_rating[index]+0.5
            elif num in range(6,11):
                oscar_rating  = num_rating[index]+1.0
            else:
                oscar_rating  = num_rating[index]+1.5
            self.adjusted_rating.append(float(format(oscar_rating , ".1f")))

        return self.adjusted_rating


if __name__ == "__main__":

    Data = WebScraping()
    original_df = Data.scraper(url = "https://www.imdb.com/chart/top/")
    adjusted_rating= Data.rating_adjustment(Data.rating,Data.number_of_ratings,Data.oscars)
    total_df= original_df.copy()
    total_df.insert(2, "Adjusted_rating", adjusted_rating, True)
    sorted_df = total_df.sort_values(by=['Adjusted_rating'],ascending=False)
    sorted_df.to_csv('Sorted_ratings.csv', index=False, encoding='utf-8')



