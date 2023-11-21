import pandas as pd
import numpy as np




def get_update_btest_dataframe(update_path):
    # get all movies on www.bechdeltest.com and save the dataframe in 'update_path'
    btest_updated = pd.read_json('http://bechdeltest.com/api/v1/getAllMovies') 
    # btest_updated columns: id, rating(bechdel_test score), title, year, imdbid
    btest_updated.to_csv(update_path, index=False)
    print("extraction of movies from www.bechdeltest.com completed")





def update_bechdel_df(old_path, update_path):
    # returns a list with the imdb_ids of the new movies added on www.bechdeltest.com

    btest_updated = pd.read_csv(old_path, index_col=0) # most updated version of the dataframe obtained by from www.bechdeltest.com 
    btest = pd.read_csv(update_path, index_col=0) # previous dataframe obtained from www.bechdeltest.com

    # if there are no new movies the function returns an empty list (no new movie ids)
    if btest_updated["imdbid"].iloc[-1]==btest["imdbid"].iloc[-1]:
        print("Bechdel dataframe already up to date")
        return pd.DataFrame([])

    
    else:
        n_movies = btest_updated.shape[0] - btest.shape[0] # index of last movie in btest

        # create an empty dataframe with the below columns
        df_new = pd.DataFrame(columns=['title', 'year', 'bt_score', 'dubious', 'imdbid', 'id', 'submitterid', 'date', 'visible'])

        count = 1
        
        for imdbid in btest_updated['imdbid'][-1:n_movies:-1]: # call from the latest movie added on bechdeltest.com
            series = pd.read_json('http://bechdeltest.com/api/v1/getMovieByImdbId?imdbid=' + str(imdbid), typ='series')
            df_new.loc[len(df_new.index)] = series
            
            # every 10 movies, we save to a csv file, so that we won't lose information in case of loop interruction
            if count % 10 == 0:
                df_new.to_csv(update_path,index=False)
            count += 1
        
        # reverse 
        df_new = df_new.iloc[::-1].reset_index(drop=True)
        # save definitive version
        df_new.to_csv(update_path,index=False) # only the latest movies, for which I will need to obtain details and credits from TMDB API

        # concatenate with the previous version and save
        bechdel_df = pd.concat([btest,df_new],axis=0)
        bechdel_df.reset_index(inplace=True)
        bechdel_df.drop_duplicates()
        bechdel_df.to_csv(old_path,index=False) # all movies currently on www.bechdeltest.com

        return df_new
