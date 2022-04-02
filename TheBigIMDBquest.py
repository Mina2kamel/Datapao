import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
from urllib.request import urlopen

class WebScraping():

    def __init__(self):
        '''
            Initialize the Class attributes
        '''
        self.TitleName = []
        self.Rating =[]
        self.Number_of_ratings = []
        self.Oscars=[]
        self.adjusted_rating=[]


    def Scraper(self,url):
        '''
        Scrape web data for TOP 20 IMDB movies
        Arguments:
            url : link of the IMDB website
        '''

        headers = {'Accept-Language': 'en-US,en;q=0.8'}
        r = requests.get(url,headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        scraped_movies = soup.find("tbody", {"class":"lister-list"}).find_all("tr")
        for movie in scraped_movies[:20]:
            title=  movie.find("td",class_="titleColumn").a.text
            rating = movie.find("td",{"class":"ratingColumn"}).text
            RatNum= movie.find('span',attrs = {'name':'nv'})['data-value']
            self.TitleName.append(title)
            self.Rating.append(float(rating))
            self.Number_of_ratings.append(int(RatNum))
            for value in movie.a.attrs.values():
                url = "https://www.imdb.com" + value
                soup = BeautifulSoup(urlopen(url),"html.parser")
                oscar = soup.find("ul",class_ ="ipc-metadata-list ipc-metadata-list--dividers-none sc-fcdc3619-2 kTHpcg ipc-metadata-list--base").a.text
                if oscar[0:3]=="Won":
                    self.Oscars.append(int(oscar[4]))
                else:
                    self.Oscars.append(0)

        return self.TitleName,self.Rating,self.Number_of_ratings,self.Oscars

    def RatingAdjustment(self):
        '''
        Modify Movie rating according to the number of ratings
        and number of oscars

        '''

        Num_rating=[]
        benchmark = max(self.Number_of_ratings)
        for index,num in enumerate(self.Number_of_ratings):
            deviation = math.floor((benchmark-num)/100000.0)
            penalty = float(format(deviation *0.1, ".1f"))
            x = self.Rating[index]-penalty
            Num_rating.append(x)

        for index , num in enumerate(self.Oscars):
            if num==0:
                y = Num_rating[index]
            elif num in range(1,3):
                y = Num_rating[index]+0.3
            elif num in range(3,6):
                y = Num_rating[index]+0.5
            elif num in range(6,11):
                y = Num_rating[index]+1.0
            else:
                y = Num_rating[index]+1.5
            self.adjusted_rating.append(float(format(y, ".1f")))

        return self.adjusted_rating


if __name__ == "__main__":

    Data = WebScraping()
    TitleName,Rating,Number_of_ratings,Oscars = Data.Scraper(url = "https://www.imdb.com/chart/top/")
    adjusted_rating= Data.RatingAdjustment()
    df = pd.DataFrame(list(zip(TitleName,Rating,adjusted_rating,Number_of_ratings,Oscars)),
                               columns=['Title','Rating','Adjusted_rating','Number of ratings','Number of Oscars'])
    sorted_df = df.sort_values(by=['Adjusted_rating'],ascending=False)
    sorted_df.to_csv('Sorted_ratings.csv', index=False, encoding='utf-8')



