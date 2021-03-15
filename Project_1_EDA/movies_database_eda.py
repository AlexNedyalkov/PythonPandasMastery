import pandas as pd
import numpy as np
from IPython.display import HTML
pd.options.display.max_colwidth = 200
pd.options.display.float_format = '{:.2f}'.format
import matplotlib.pyplot as plt
pd.options.display.max_columns = 30
from wordcloud import WordCloud

FILE_NAME = 'movies_complete.csv'
DATA_FOLDER = '/home/user/Documents/PythonPandasMastery/Data/'
INPUT_SOURCE = DATA_FOLDER + FILE_NAME


def best_worst(df_best, n, by, ascending=False, min_bud=0, min_votes=0):
    df2 = df_best.loc[(df_best.Budget >= min_bud) & (df_best.Votes >= min_votes),
                      ["", by]].sort_values(by=by, ascending=ascending).head(n).copy()

    return HTML(df2.to_html(escape=False))

movies = pd.read_csv(INPUT_SOURCE, parse_dates= ["release_date"])
# print(movies.info())
# print(movies.describe(include = 'object'))

# movies.hist(figsize=(20, 12), bins = 100)

movies_best = movies[["poster_path", "title", "budget_musd", "revenue_musd",
              "vote_count", "vote_average", "popularity"]].copy()
movies_best["profit_musd"] = movies.revenue_musd - movies.budget_musd
movies_best["return"] = movies.revenue_musd/movies.budget_musd

movies_best.columns = ["", "Title", "Budget", "Revenue", "Votes",
                   "Average Rating", "Popularity", "Profit", "ROI"]

# movies_best.set_index('Title', inplace = True)
#
# movies_best.Budget.fillna(0, inplace = True)
# movies_best.Votes.fillna(0, inplace = True)
#
# best_worst(df = movies_best, n = 5, by = "Revenue")
#
# best_worst(5, "ROI", min_bud = 50)

mask_genres = movies.genres.str.contains('Action') & movies.genres.str.contains('Science Fiction')
mask_actor = movies.cast.str.contains('Bruce Willis')
# print(movies.loc[mask_actor & mask_genres, ['title', 'vote_average']].sort_values(by = 'vote_average', ascending = False).set_index('title'))

mask_studio = movies.production_companies.str.contains('Pixar').fillna(False)
mask_time = movies.release_date.between("2010-01-01", "2015-12-31")
# print(movies.loc[mask_studio & mask_studio, ['title', 'vote_average']].sort_values(by = 'vote_average', ascending = False).set_index('title'))

movies_titles = movies.title.dropna()
movies_taglines = movies.tagline.dropna()
movies_overviews = movies.overview.dropna()

title_corpus = ' '.join(movies_titles)
overview_corpus = ' '.join(movies_overviews)
tagline_corpus = ' '.join(movies_taglines)

title_wordcloud = WordCloud(background_color='white', height=2000, width=4000, max_words= 200).generate(title_corpus)

# plt.figure(figsize=(16,8))
# plt.imshow(title_wordcloud, interpolation= "bilinear")
# plt.axis('off')
# plt.show()

movies["Franchise"] = movies.belongs_to_collection.notna()
print('Movies belonging to a franchise: ', movies.Franchise.value_counts())
print('Average return for franchise movies: ',movies.loc[movies["Franchise"] == True, 'revenue_musd'].mean())
print('Average return for non-franchise movies: ',movies.loc[movies["Franchise"] == False, 'revenue_musd'].mean())
print('Average return for franchise movies: ',movies.groupby("Franchise")['revenue_musd'].median())
print(df.groupby("Franchise").agg({"budget_musd": "mean", "revenue_musd": "mean", "vote_average": "mean",
                            "popularity": "mean", "ROI":"median", "vote_count":"mean"}))
