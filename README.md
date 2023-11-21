# Data Analysis on Female Representation in Cinema through Bechdel Test scores


## Introduction
The Bechdel Test is a subjective test that can be used as an indicator of the active presence of women in fiction, popularized by the American cartoonist Alison Bechdel in the form of a joke.
In order to pass the test the following requirements should be satisfied: <br> (1) There has to be at least two women
<br>(2) who talk to each other, about 
<br>(3) something besides a man. 

By scrutinizing and analyzing Bechdel Test scores across a diverse range of movies, this project aims to unravel patterns, trends, and insights into the portrayal of women in cinema. 


## Libraries and Datasets used
The Kaggles dataset [Female representation in cinema](https://www.kaggle.com/datasets/vinifm/female-representation-in-cinema) was used for this project. This was obtained starting from another Kaggle dataset, [Movie Bechdel Test Scores](https://www.kaggle.com/datasets/alisonyao/movie-bechdel-test-scores), and enriching it with more information about the movies.

The dataset contains the following information for each movie: <br>
- **bt_score** : The bechdel test score.
- **dubious**: Whether the submitter considered the rating dubious.
- **imdbid**: id on IMDb
- **tmdbId**: id on TMDB
- **popularity**: TMDB popularity.
- **revenue**: revenue in American Dollar (USD). Not adjusted for inflation.
- **vote_average**: average rating
- **vote_count**: number of ratings
- **cast** and **crew**: a json with cast and crew information. Check the response body in the TMDB api docs.
- **cast_gender** and **crew_gender**: gender of cast and crew: Not specified (0),Female (1), Male (2), Non-binary (3)
- **cast_female_representation** and **crew_female_representation**: percentage of women in the cast or crew.

The dataset was updated with most recent movies added on [bechdeltest.com](https://bechdeltest.com/).


#### Libraries used:
- Pandas, numpy
- pymysql, sqlalchemy
- requests


## Workflow
1. Getting the updated list of movies from [bechdeltest.com](https://bechdeltest.com/)
2. Getting details and credits of these new movies, fetching [TMDB( The Movie DataBase) API](https://developer.themoviedb.org/docs)
3. Joining the new datas acquired with those already available
4. Creating three new datasets, specific for production companies, movie cast and movie crew
5. Loading the datasets on SQL and made some queries to explore the datasets
6. Present information obtained through Tableau


## Analysis & Results

### 1. Percentage of movies for each Bechdel-Test score

<img src=https://github.com/luciaaguzzoni/project-IV/blob/main/figures/1.1.png />

<img src=https://github.com/luciaaguzzoni/project-IV/blob/main/figures/1.2.png />

### 2. Comparing production companies 

<img src=https://github.com/luciaaguzzoni/project-IV/blob/main/figures/2.1.png />

<img src=https://github.com/luciaaguzzoni/project-IV/blob/main/figures/2.2.png />

<img src=https://github.com/luciaaguzzoni/project-IV/blob/main/figures/3.1.png />

### 3. Bechdel-Test score for most successful movies

<img src=https://github.com/luciaaguzzoni/project-IV/blob/main/figures/4.png />



<br>

### Tableu Presentation link: 
https://public.tableau.com/app/profile/lucia.aguzzoni/viz/Bechdel_Test/Story1
