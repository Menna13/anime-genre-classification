import pandas as pd

df = pd.read_csv('animes.csv')
df = df[['title', 'synopsis', 'genre']]
df = df.dropna(subset=['genre'], how='all')
#print(df['genre'])
genres = set()
for genre in df['genre']:
    s = genre[1:-1].split(',')
    for i in s:
        stripped = i.replace('\'', '').replace(' ', '')
        genres.add(stripped)
print(len(genres), genres)


