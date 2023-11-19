import pandas as pd
import numpy as np




def get_update_btest_dataframe(update_path):
    btest_updated = pd.read_json('http://bechdeltest.com/api/v1/getAllMovies')
    btest_updated.to_csv(update_path, index=False)
    print("extraction of movies from www.bechdeltest.com completed")




def update_bechdel_df(kaggle_path, update_path):

    btest_updated = pd.read_csv(kaggle_path, index_col=0)
    btest_kaggle = pd.read_csv(update_path, index_col=0)

    n_movies = btest_updated.shape[0] - btest_kaggle.shape[0]
    
    # create an empty dataframe
    df_new = pd.DataFrame(columns=['title', 'year', 'rating', 'dubious', 'imdbid', 'id', 'submitterid', 'date', 'visible'])

    count = 1
    # call from the latest to the earliest movie, in case the website crashes
    for imdbid in btest_updated['imdbid'][-1:n_movies:-1]:
        series = pd.read_json('http://bechdeltest.com/api/v1/getMovieByImdbId?imdbid=' + str(imdbid), typ='series')
        df_new.loc[len(df_new.index)] = series
        
        # every 10 movies, we save to a csv file, so that we wouldn't lose everything when there is an error
        if count % 10 == 0:
            df_new.to_csv('../data/Bechdel_updated.csv')
        count += 1
    
    # reverse 
    df_new = df_new.iloc[::-1].reset_index(drop=True)

    df_new.to_csv('../data/Bechdel_updated.csv',index=False)

    bechdel_df = pd.concat([btest_kaggle,df_new],axis=0)
    bechdel_df.reset_index(inplace=True)
    bechdel_df.drop_duplicates()

    bechdel_df.to_csv('../data/Bechdel.csv',index=False)