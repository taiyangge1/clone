import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load your dataset
df = pd.read_excel(r"C:\Users\24766\Desktop\Wimbledon_featured_matches.xlsx")  # Adjust the file path as necessary

# -------------------------------------------------------------------
# Convert the traditional tennis scores to continuous numbers
score_mapping = {0: 0, 15: 1, 30: 2, 40: 3, 'AD': 4}
df['p1_score'] = df['p1_score'].map(score_mapping).fillna(df['p1_score'])
df['p2_score'] = df['p2_score'].map(score_mapping).fillna(df['p2_score'])

# Convert 'winner_shot_type' from 'F', 'B' to 1, 2
shot_type_mapping = {'F': 1, 'B': 2}
df['winner_shot_type'] = df['winner_shot_type'].map(shot_type_mapping).fillna(df['winner_shot_type'])

# Choose the right features
features_to_scale = [
    "p1_unf_err",  # player 1 made an unforced error
    "p2_unf_err",  # player 2 made an unforced error
    "p1_double_fault",  # player 1 missed both serves and lost the point
    "p2_double_fault",  # player 2 missed both serves and lost the point
    "p1_sets",  # sets won by player 1
    "p2_sets",  # sets won by player 2
    "p1_games",  # games won by player 1 in current set
    "p2_games",  # games won by player 2 in current set
    "p1_score",  # player 1's score within current game
    "p2_score",  # player 2's score within current game
    "server",  # server of the point
    "serve_no",  # first or second serve
    "p1_winner",  # player 1 hit an untouchable winning shot
    "p2_winner",  # player 2 hit an untouchable winning shot
    "speed_mph",  # speed of serve (miles per hour; mph)
    "p1_distance_run",  # player 1's distance ran during point (meters)
    "p2_distance_run",  # player 2's distance ran during point (meters)
    "rally_count",  # number of shots during the point
    "p1_ace",  # player 1 hit an untouchable winning serve
    "p2_ace",  # player 2 hit an untouchable winning serve
]

columns_to_keep = ['match_id', 'elapsed_time'] + features_to_scale
df_subset = df[columns_to_keep]

# -------------------------------------------------------------------
# Function to replace outliers with the group's median
def replace_outliers_with_median(group, features):
    for feature in features:
        Q1 = group[feature].quantile(0.25)
        Q3 = group[feature].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        median = group[feature].median()
        group[feature] = group[feature].apply(lambda x: median if x < lower_bound or x > upper_bound else x)
    return group

# Apply the function to each match_id group
df_processed = df.groupby('match_id').apply(lambda group: replace_outliers_with_median(group, features_to_scale))


# Function to fill missing values with the median and scale features for each group
def process_group(group):
    # Fill missing numeric values with the group's median
    for column in features_to_scale:
        if group[column].isnull().any():
            group[column].fillna(group[column].median(), inplace=True)
    # Scale features
    scaler = StandardScaler()
    group[features_to_scale] = scaler.fit_transform(group[features_to_scale])
    return group

# Apply the function to each match_id group
df_subset_processed = df_subset.groupby('match_id').apply(process_group)
df_subset_processed.reset_index(drop=True, inplace=True)
# -------------------------------------------------------------------
# Save the processed dataset
df_subset_processed.to_excel(r"C:\Users\24766\Desktop\processed_Wimbledon_featured_matches.xlsx", index=False)