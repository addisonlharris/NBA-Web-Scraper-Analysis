import plotly.express as px
import pandas as pd

# Get the data, skipping the header row
df = pd.read_csv("csv files/playoff_winlosses.csv").iloc[1:]  # Skip the header row

# Clean the data
df = df[df['Team'].notna()]  # Remove any rows without team names
df = df[df['Team'] != 'This list is accurate through the end of the 2023–24 NBA season.']  # Remove the note row

# Convert Won and Lost columns to numeric
df['Won'] = pd.to_numeric(df['Won'], errors='coerce')  # Wins
df['Lost'] = pd.to_numeric(df['Lost'], errors='coerce')  # Losses

# Remove any rows with invalid data
df = df.dropna(subset=['Won', 'Lost'])

# Melt the dataframe to create a format suitable for grouped bars
df_melted = pd.melt(df, 
                    id_vars=['Team'],
                    value_vars=['Won', 'Lost'],
                    var_name='Type',
                    value_name='Games')

# Create the grouped bar chart
fig = px.bar(df_melted, 
             x='Team',
             y='Games',
             color='Type',
             barmode='group',
             title='NBA Teams: Wins vs Losses Comparison (Playoffs)',
             labels={'Team': 'Team Name', 
                    'Games': 'Number of Games',
                    'Type': 'Game Result'},
             color_discrete_map={'Wins': 'green', 'Losses': 'purple'})

# Update layout for better readability
fig.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor='white',
    legend_title_text=''
)

fig.show()