from src import bechdel_api as bt
from src import tmdb_api as tmdb





bechdel_path = "data/Bechdel.csv"
update_bechdel_path = "data/Bechdel_updated.csv"

## get new movies from www.bechdeltest.com/api 
bt.get_update_btest_dataframe(update_bechdel_path)
update_bechdel_df = bt.update_bechdel_df(bechdel_path,update_bechdel_path)


## get details + credits for the new movies with TMDB API and create a new updated dataframe
movies_path = "data/all_movies.csv"
new_movies_path = "data/new_movies.csv"

imdbid_list = tmdb.get_ids(list(update_bechdel_df["imdbid"])) # get imbdb_id of the new movies

new_movies_df = tmdb.get_movie_info(imdbid_list,new_movies_path) # get details + credits of the new movies

# clean new_movies
new_movies_df = tmdb.clean_merge(update_bechdel_df,new_movies_df)
# concatenate dataframe old_movies and dataframe new_movies and save 
old_movies = pd.read_csv(movies_path)
all_movies = tmdb.get_all_movies(old_movies,new_movies_df,movies_path)









