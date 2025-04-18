import pandas as pd
from pybaseball import statcast

def fetch_stats(start_date, end_date):
    """
    Fetch baseball statistics from the Statcast API for the given date range.
    
    Parameters:
    start_date (str): The start date in 'YYYY-MM-DD' format.
    end_date (str): The end date in 'YYYY-MM-DD' format.
    
    Returns:
    DataFrame: A pandas DataFrame containing the fetched statistics.
    """
    stats = statcast(start_dt=start_date, end_dt=end_date)
    return stats

def process_stats(stats_df):
    """
    Process the fetched statistics DataFrame to extract relevant information.
    
    Parameters:
    stats_df (DataFrame): The DataFrame containing raw statistics.
    
    Returns:
    DataFrame: A processed DataFrame with relevant statistics.
    """
    if stats_df is None or stats_df.empty:
        return pd.DataFrame()
        
    # Select and rename relevant columns
    columns_to_keep = [
        'player_name', 
        'game_date', 
        'events', 
        'hit_distance_sc',
        'launch_speed',
        'home_score',
        'away_score'
    ]
    
    # Only keep columns that exist in the DataFrame
    available_columns = [col for col in columns_to_keep if col in stats_df.columns]
    processed_stats = stats_df[available_columns].copy()
    
    # Group by player and date to get daily stats
    daily_stats = processed_stats.groupby(['player_name', 'game_date']).agg({
        'launch_speed': 'mean',
        'hit_distance_sc': 'mean',
        'events': lambda x: x.value_counts().to_dict()
    }).reset_index()
    
    return daily_stats