import pandas as pd
from tabulate import tabulate
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tabulate import tabulate
import numpy as np

pd.set_option("display.max_rows", None)

#load the file excel
file_path = "genshin-v5.6_DSA-excel.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

#use this!
print(tabulate(df
    [["Name", "Quality (star)", "Element", "Weapon", "HP", "ATK", "DEF", "DPS", "On-field", "Off-field", "Support", "Survivability"]].fillna("N/A").values.tolist(), 
    headers=["Name", "Quality (star)", "Element", "Weapon", "HP", "ATK", "DEF", "DPS", "On-field", "Off-field", "Support", "Survivability"],
        tablefmt="simple"))

print()
print("The table above provides the character list of Genshin Impact.")
print()
print()

# DATA SCIENCE AND ANALYTICS
print ()
stats_options = ["HP", "ATK", "DEF"]
team = []
max_team_size = 4

#precompute quartile
atk_q = df["ATK"].quantile([0.25, 0.5, 0.75])
def_q = df["DEF"].quantile([0.25, 0.5, 0.75])
hp_q = df["HP"].quantile([0.25, 0.5, 0.75])


def get_quartile(value, stat_quartiles):
    if value <= stat_quartiles[0.25]:
        return "Q1"
    elif value <= stat_quartiles[0.5]:
        return "Q2"
    elif value <= stat_quartiles[0.75]:
        return "Q3"
    else:
        return "Q4"
    
while len(team) < max_team_size:
    name_input = input(f"Enter a character name: ({len(team)+1}/{max_team_size}): ")
    matches = df[df["Name"].str.lower().str.contains(name_input.lower())]
    
    if matches.empty:
        print("No matches found.")
        continue
    elif len(matches) > 1:
        print("Multiple matches found: ")
        for i, name in enumerate(matches["Name"], 1):
            print(f"{i}. {name}")
        choice = int(input("Select character number: ")) - 1
        if choice not in range(len(matches)):
            print("Invalid choice.")
            continue
        selected = matches.iloc[choice]
    else:
        selected = matches.iloc[0]
    
    team.append(selected)

# Build summary table
summary = []
for char in team:
    summary.append([
        char["Name"],
        get_quartile(char["ATK"], atk_q),
        get_quartile(char["DEF"], def_q),
        get_quartile(char["HP"], hp_q)
    ])

headers = ["Name", "ATK", "DEF", "HP"]

print("\nCharacter Stat Rank Check")
print(tabulate(summary, headers=headers, tablefmt="fancy_grid"))

def plot_radar_chart(characters_df):
    stats = ['ATK', 'DEF', 'HP']
    num_vars = len(stats)


    scaler = MinMaxScaler()
    normalized = scaler.fit_transform(characters_df[stats])
    normalized_df = pd.DataFrame(normalized, columns=stats)
    normalized_df["Name"] = characters_df["Name"].values

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fiq, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for idx, row in normalized_df.iterrows():
        values = [row[stat] for stat in stats]
        values += values[:1]
        ax.plot(angles, values, label=row["Name"])
        ax.fill(angles, values, alpha=0.1)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats)

    plt.title("Character Stat Comparison", size=14)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.show()    

team_df = pd.DataFrame(team)
plot_radar_chart(team_df)


    
