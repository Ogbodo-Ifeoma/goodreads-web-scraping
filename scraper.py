import requests
from bs4 import BeautifulSoup
import pandas as pd

books_to_movies = []

for i in range(1, 11):
    url = 'https://www.goodreads.com/list/show/1043.Books_That_Should_Be_Made_Into_Movies{?page=i}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html')
    table = soup.find('table', {'class' : 'tableList js-dataTooltip'})
    table_row = table.findAll('tr')

    for rows in table_row:
        

        book_class = rows.find('a', {'class' : 'bookTitle'})
        book_title = book_class.find('span').get_text()


        author_class = rows.find('a', {'class' : 'authorName'})
        author_name = author_class.find('span').get_text()

        ratings = rows.find('span', {'class' : 'minirating'}).get_text()
        avg_ratings = ratings[:5]
        avg_ratings = float(avg_ratings)

        no_of_ratings = ratings[19:]
        no_of_ratings = no_of_ratings.replace('ratings', '').strip()
        no_of_ratings = int(no_of_ratings.replace(',', ''))

        score_class = rows.findAll('span', {'class' : 'smallText'})
        score_class = score_class[1]


        score = score_class.findAll('a')
        scores = score[0].get_text()
        scores = int(scores[7:].replace(',', ''))
        
        vote_class = score[1].get_text()
        vote_class = vote_class.replace('people voted', '').strip()

        no_of_votes = int(vote_class.replace(',', ''))
       

        books_to_movies.append([book_title, author_name, avg_ratings, no_of_ratings, scores, no_of_votes])

df = pd.DataFrame(books_to_movies, columns = ["Title", "Author", "Star_rating", "No_of_ratings", "Score", "No_of_votes"])
df.to_csv('books_to_movies.csv')
