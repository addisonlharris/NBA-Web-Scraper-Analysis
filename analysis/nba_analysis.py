import plotly.express as px
import pandas as pd

# Get the data, skipping the header row
df = pd.read_csv("csv files/nba_winlosses.csv").iloc[1:]  # Skip the header row

# Clean and sort the data
df = df[df['Team'].notna()]  # Remove any rows without team names
df = df[df['Team'] != 'This list is accurate through the end of the 2023–24 NBA season.']  # Remove the note row
df['Won'] = pd.to_numeric(df['Won'], errors='coerce')  # Convert Won column to numeric, handling any errors
df = df.dropna(subset=['Won'])  # Remove any rows where Won couldn't be converted to numeric
df = df.sort_values('Won')   # Sort by wins in ascending order

# Create the bar chart
fig = px.bar(df, x='Team', y='Won', 
             title='NBA Teams Ranked by Wins Regular Season (Ascending)',
             labels={'Column 2': 'Team Name', 'Column 4': 'Number of Wins'})

# Update layout for better readability
fig.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor='white',
    showlegend=False
)

fig.show()