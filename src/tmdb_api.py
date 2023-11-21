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



## ids transformation

def get_id(dep_id):
# change imdbit in the format ddddddd: ex 542 -> 0000542
    try:
        dep_id = str(int(dep_id))
        l = len(dep_id)
        new_id = '0'*(7-l)+dep_id
        return new_id
    except:
        pass

def get_ids(id_list):
#applies function get_id to all elements of id_list
    for i in range(len(id_list)):
        id_list[i] = get_id(id_list[i])
    return id_list





## TMDB API call function

def get_movie_info(imdbid_list,update_path):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_access_token}"
    }
    
    new_movie_list = [] # list of dictionaries to create the movies dataframe
    
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
        
        # every 20 movies, we save to a csv file, so that we won't lose information in case of loop interruction
        if cont%20==0:
            pd.DataFrame(new_movie_list).to_csv("update_path",index=False)
        cont+=1


    new_movies_df = pd.DataFrame(new_movie_list) # creating dataframe
    new_movies_df.to_csv("update_path",index=False) # saving dataframe

    return new_movies_df





## CLEANING

def clean_prodcompanies(df):
    # changes types of column 'production_companies' as a list of strings
    for index, movie in df.iterrows():
        companies = eval(movie['production_companies'])
        companies_list = []

        for company in companies:
            company_name = company['name']
            companies_list.append(company_name)

        df.at[index, 'production_companies'] = companies_list
    return df


def change_dateformat(df): 
    # changes date format from Y-m-d to d-m-Y  
    for index, movie in df.iterrows():
        date = datetime.strptime(movie['release_date'], '%Y-%m-%d')
        reformatted_date = date.strftime('%d/%m/%Y')

        df.at[index, 'release_date'] = reformatted_date
    return df


def clean_cast(df):
    # insert new column 'cast_gender'
    # for each rows create a list of ints, each element of the list represent the gender of a member of the cast
    # 0: Not specified, 1: Female, 2: Male, 3: Non-binary
    df['cast_gender'] = pd.NA

    for index, movie in df.iterrows():
        cast = eval(movie['cast'])
        gender_list = []

        for cast_member in cast:
            gender = cast_member['gender']
            gender_list.append(gender)

        df.at[index, 'cast_gender'] = gender_list
    return df


def clean_crew(df):
    # insert new column 'crew_gender'
    # for each rows create a list of ints, each element of the list represent the gender of a member of the crew
    # 0: Not specified, 1: Female, 2: Male, 3: Non-binary
    df['cast_gender'] = pd.NA
    for index, movie in df.iterrows():
        crew = eval(movie['crew'])
        gender_list = []

        for crew_member in crew:
            gender = crew_member['gender']
            gender_list.append(gender)

        df.at[index, 'crew_gender'] = gender_list
    return df


def fem_columns(df):
    # create two columns for female representation resp between cast members and crew members
    df['cast_female_representation'] = pd.NA
    df['crew_female_representation'] = pd.NA


    for index, movie in df.iterrows():
        if len(movie['cast_gender']) != 0:
            df.at[index, 'cast_female_representation'] = 100*(movie['cast_gender'].count(1)/len(movie['cast_gender']))

        if len(movie['crew_gender']) != 0:
            df.at[index, 'crew_female_representation'] = 100*(movie['crew_gender'].count(1)/len(movie['crew_gender']))


    df = df.dropna().copy()
    df['cast_female_representation'] = df['cast_female_representation'].astype('float64')
    df['crew_female_representation'] = df['crew_female_representation'].astype('float64')
    return df






## Merge with bechdel dataframe (contains bt_scores)

def clean_merge(left_df, new_df):
    new_df.dropna(inplace=True)
    new_df.reset_index(drop=True,inplace=True)

    df = pd.merge(left_df, new_df, left_on='imdbid', right_on='imdbid', how='inner')
    df.drop(columns=["id","submitterid","date","visible"], inplace=True)

    df = clean_prodcompanies(df)
    df = change_dateformat(df)
    df = clean_cast(df)
    df = clean_crew(df)
    df = fem_columns(df)

    df.drop(columns=["cast","crew"],inplace=True)
    return df





## Concatenate with the previous dataframe

def get_all_movies(df_old,df_new,path):
    all_movies = pd.concat([df_old,df_new], axis=0)
    all_movies.dropna(how='all',inplace=True)
    all_movies.drop_duplicates(subset="imdbid", inplace=True)
    all_movies.reset_index(drop=True, inplace=True)
    all_movies.to_csv(path,index=False)
    return all_movies





