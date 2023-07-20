import pandas as pd
from collections import Counter

eclair_receives = 0
fritter_receives = 0
eclair_goals = 0
fritter_goals = 0
eclair_assists = 0
fritter_assists = 0
eclair_passes = 0
fritter_passes = 0
fritter_to_fritter_pass = 0
eclair_to_fritter_pass = 0
eclair_to_eclair_pass = 0
fritter_to_eclair_pass = 0

passes = {
    "Female-matching Handler" : Counter(),
    "Female-matching Cutter" : Counter(),
    "Male-matching Handler" : Counter(),
    "Male-matching Cutter" : Counter(),
}

stats = pd.read_csv('Donuts-stats.csv')
players = pd.read_csv('players.csv')
player_names = []

for index, row in players.iterrows():
    name = row['Name']
    player_names.append(name)

total_passes_to_eclairs = dict.fromkeys(player_names, 0)
total_passes = dict.fromkeys(player_names, 0)
passes_to_eclairs_percentage = dict.fromkeys(player_names, 0)

stats = stats[["Date/Time", "Tournament", "Opponent", "Line", "Event Type", "Action", "Passer", "Receiver"]]
# stats = stats[(stats["Date/Time"] > "2022") & (stats["Date/Time"] < "2023")]
stats = stats[stats.Tournament == "SFI 2023"]
stats = stats[stats.Line == "O"]
# stats = stats[(stats.Opponent == "BW") | (stats.Opponent == "Lights Out") | (stats.Opponent == "ABBQ")]
# stats = stats[(stats.Opponent == "LIT") | (stats.Opponent == "Tower") | (stats.Opponent == "Robot")]
stats = stats[(stats.Action == "Catch") | (stats.Action == "Goal")]
stats = stats[stats['Event Type'] == "Offense"]
for index, row in stats.iterrows():
    gen = ""
    passer = row['Passer']
    receiver = row['Receiver']
    p_fritter = True
    r_fritter = True
    p_type = None
    r_type = None
    p = players[players.Name == passer]
    r = players[players.Name == receiver]
    total_passes[passer] += 1
    for p in p.itertuples():
        gen = getattr(p, 'Role')
        position = getattr(p, 'Position')
        p_type = gen + " " + position
        if gen == "Female-matching": 
            p_fritter = False
            eclair_passes += 1
            if row['Action'] == "Goal":
                eclair_assists += 1
        elif gen == "Male-matching":
            fritter_passes += 1
            if row['Action'] == "Goal":
                fritter_assists += 1
    for r in r.itertuples():
        gen = getattr(r, 'Role')
        position = getattr(r, 'Position')
        r_type = gen + " " + position
        if gen == "Female-matching":
            r_fritter = False
            eclair_receives += 1
            total_passes_to_eclairs[passer] += 1
            if p_fritter:
                fritter_to_eclair_pass += 1
            else:
                eclair_to_eclair_pass += 1
            if row['Action'] == "Goal":
                eclair_goals += 1
        elif gen == "Male-matching":
            fritter_receives += 1
            if p_fritter:
                fritter_to_fritter_pass += 1
            else:
                eclair_to_fritter_pass += 1
            if row['Action'] == "Goal":
                fritter_goals += 1
    passes[p_type][r_type] += 1

for name in passes_to_eclairs_percentage.keys():
    if total_passes[name] == 0:
        continue
    passes_to_eclairs_percentage[name] = round(total_passes_to_eclairs[name]/total_passes[name], 2)

print("Eclair touches: ", eclair_receives)
print("Fritter touches: ", fritter_receives)
print("Eclair touch ratio: ", round(eclair_receives/(eclair_receives + fritter_receives) , 2))
print("Eclair goals: ", eclair_goals)
print("Fritter goals: ", fritter_goals)
print("Eclair assists: ", eclair_assists)
print("Fritter assists: ", fritter_assists)
print("Eclair goal ratio: ", round(eclair_goals/(eclair_goals + fritter_goals), 2))
print("Percentage of fritter throws to eclairs: ", round(fritter_to_eclair_pass/fritter_passes, 2))
print("Percentage of eclair throws to eclairs: ", round(eclair_to_eclair_pass/eclair_passes, 2))
print("Percentage of throws to eclairs: ", passes_to_eclairs_percentage)

for p_type in sorted(list(passes)):
    print(p_type)
    print("eclair_cutter_ratio",
        passes[p_type]["Female-matching Cutter"]/
            (passes[p_type]["Female-matching Cutter"]+passes[p_type]["Male-matching Cutter"]))

    print("eclair_handler_ratio",
        passes[p_type]["Female-matching Handler"]/
            (passes[p_type]["Female-matching Handler"]+passes[p_type]["Male-matching Handler"]))

