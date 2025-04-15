import plotly.express as px
import pandas as pd

# Get the data, skipping the header row
df = pd.read_csv("csv files/nba_winlosses.csv").iloc[1:]  # Skip the header row

# Clean the data
df = df[df['Team'].notna()]  # Remove any rows without team names
df = df[df['Team'] != 'This list is accurate through the end of the 2023–24 NBA season.']  # Remove the note row

# Print unique values in the Division column to see what we're working with
print("Unique divisions before cleaning:", df['Division'].unique())

# Manual division corrections for teams with ⁂
division_corrections = {
    'Boston Celtics': 'Atlantic',
    'Brooklyn Nets': 'Atlantic',
    'New York Knicks': 'Atlantic',
    'Philadelphia 76ers': 'Atlantic',
    'Toronto Raptors': 'Atlantic',
    'Chicago Bulls': 'Central',
    'Cleveland Cavaliers': 'Central',
    'Detroit Pistons': 'Central',
    'Indiana Pacers': 'Central',
    'Milwaukee Bucks': 'Central',
    'Atlanta Hawks': 'Southeast',
    'Charlotte Hornets': 'Southeast',
    'Miami Heat': 'Southeast',
    'Orlando Magic': 'Southeast',
    'Washington Wizards': 'Southeast',
    'Denver Nuggets': 'Northwest',
    'Minnesota Timberwolves': 'Northwest',
    'Oklahoma City Thunder': 'Northwest',
    'Portland Trail Blazers': 'Northwest',
    'Utah Jazz': 'Northwest',
    'Golden State Warriors': 'Pacific',
    'Los Angeles Clippers': 'Pacific',
    'Los Angeles Lakers': 'Pacific',
    'Phoenix Suns': 'Pacific',
    'Sacramento Kings': 'Pacific',
    'Dallas Mavericks': 'Southwest',
    'Houston Rockets': 'Southwest',
    'Memphis Grizzlies': 'Southwest',
    'New Orleans Pelicans': 'Southwest',
    'San Antonio Spurs': 'Southwest'
}

# Apply division corrections
df['Corrected_Division'] = df.apply(lambda row: division_corrections.get(row['Team'], row['Division']), axis=1)

# Convert columns to appropriate types
df['Won'] = pd.to_numeric(df['Won'], errors='coerce')  # Wins
df['Lost'] = pd.to_numeric(df['Lost'], errors='coerce')  # Losses

# Calculate win percentage
df['Win_Pct'] = df['Won'] / (df['Won'] + df['Lost']) * 100

# Group by corrected division and calculate statistics
division_stats = df.groupby('Corrected_Division').agg({
    'Win_Pct': ['mean', 'count'],
    'Team': lambda x: ', '.join(x)  # List of teams in each division
}).reset_index()

division_stats.columns = ['Division', 'Avg_Win_Pct', 'Team_Count', 'Teams']
division_stats['Teams_Count'] = division_stats['Team_Count'].astype(str) + ' teams'

# Sort by win percentage
division_stats = division_stats.sort_values('Avg_Win_Pct', ascending=True)

# Create the bar chart
fig = px.bar(division_stats, 
             x='Division',
             y='Avg_Win_Pct',
             text='Teams_Count',
             title='NBA Divisions Ranked by Average Win Percentage',
             labels={'Division': 'Division Name',
                    'Avg_Win_Pct': 'Average Win Percentage (%)'},
             color='Avg_Win_Pct',
             color_continuous_scale='RdYlGn')  # Red to Green color scale

# Add hover data to show teams in each division
fig.update_traces(
    hovertemplate="<br>".join([
        "Division: %{x}",
        "Win Percentage: %{y:.1f}%",
        "Teams: %{customdata}",
    ]),
    customdata=division_stats['Teams']
)

# Update layout for better readability
fig.update_traces(textposition='outside')
fig.update_layout(
    plot_bgcolor='white',
    showlegend=False,
    yaxis_range=[0, 100],  # Set y-axis from 0 to 100%
    xaxis_tickangle=-45
)

fig.show()