import pandas as pd 

scrape = pd.read_html("https://en.wikipedia.org/wiki/List_of_all-time_NBA_win%E2%80%93loss_records")

#regular season statistics 
df = scrape[1]
df.to_csv('nba_winlosses.csv', index=False)
df_scrape_file = pd.read_csv('nba_winlosses.csv')

#playoff statics 
df2 = scrape[5]
df2.to_csv('playoff_winlosses.csv', index=False)
df2_scrape_file = pd.read_csv('playoff_winlosses.csv')