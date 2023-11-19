from src import bechdel_api as bt
from src import tmdb_api as tmdb




## get new movies from www.bechdeltest.com/api 
kaggle_path = "data/Bechdel_kaggle.csv"
update_path = "data/Bechdel_updated.csv"

bt.get_update_btest_dataframe(update_path)

bechdel_df = bt.update_bechdel_df(kaggle_path,update_path)







## get details + credits info for this new movies with tmdb/api and create a dataframe new_movies
# clean new_movies

## concatenate movies and new_movies 

## creates SQL tables
# SQL queries