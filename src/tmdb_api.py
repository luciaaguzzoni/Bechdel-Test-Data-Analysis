import pandas as pd
import numpy as np
import requests
from datetime import datetime
import time

import os
from dotenv import load_dotenv 

load_dotenv()
tmdb_key = os.getenv("tmdb_key")

#load_dotenv()
tmdb_access_token = os.getenv("tmdb_access_token")



# change imdbit in the format ddddddd
def get_id(dep_id):
    try:
        dep_id = str(int(dep_id))
        l = len(dep_id)
        new_id = '0'*(7-l)+dep_id
        return new_id
    except:
        pass


def get_ids(id_list):
    for i in range(len(id_list)):
        id_list[i] = get_id(id_list[i])
    return id_list



def get_movie_info(imdbid_list):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_access_token}"
    }
    
    new_movie_list = []
    cont=0
    
    for imbdid in imdbid_list:
        movie_dict={}
        time.sleep(1)
        details_url = f"https://api.themoviedb.org/3/movie/tt{imbdid}?language=en-US"        
        credits_url = f"https://api.themoviedb.org/3/movie/tt{imbdid}/credits?language=en-US"
        
        
        details_response = requests.get(details_url, headers=headers).json()
        try: 
            movie_dict["imdbid"] = imbdid
            movie_dict["genres"] = [el["name"] for el in details_response["genres"]]           
            movie_dict["budget"] = details_response["budget"]
            movie_dict["popularity"] = details_response["popularity"]
            movie_dict["production_companies"] = details_response['production_companies']
            movie_dict["release_date"] = details_response['release_date']
            movie_dict["revenue"] = details_response['revenue']
            movie_dict["vote_average"] = details_response['vote_average']
            movie_dict["vote_count"] = details_response['vote_count']
        except:
            pass
    

        credit_response = requests.get(credits_url, headers=headers).json()
        try:
            movie_dict['cast'] = credit_response['cast']
            movie_dict['crew'] = credit_response['crew']
        except:
            pass
        
        new_movie_list.append(movie_dict)
        
        if cont%20==0:
            pd.DataFrame(new_movie_list).to_csv("../data/new_movies.csv",index=False)
        cont+=1
        
    new_movies_df = pd.DataFrame(new_movie_list)
    new_movies_df.to_csv("../data/new_movies.csv",index=False)

    return new_movies_df









