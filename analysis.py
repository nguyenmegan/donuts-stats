import pandas as pd

eclair_receives = 0
fritter_receives = 0
eclair_goals = 0
fritter_goals = 0
eclair_passes = 0
fritter_passes = 0
fritter_to_fritter_pass = 0
eclair_to_fritter_pass = 0
eclair_to_eclair_pass = 0
fritter_to_eclair_pass = 0

stats = pd.read_csv('Donuts-stats.csv')
gender = pd.read_csv('gender.csv')
player_names = []

for index, row in gender.iterrows():
    name = row['Name']
    player_names.append(name)

total_passes_to_eclairs = dict.fromkeys(player_names, 0)
total_passes = dict.fromkeys(player_names, 0)
passes_to_eclairs_percentage = dict.fromkeys(player_names, 0)

stats = stats[["Date/Time", "Tournamemnt", "Opponent", "Line", "Event Type", "Action", "Passer", "Receiver"]]
stats = stats[stats.Tournamemnt == "SFI 2023"]
# stats = stats[(stats.Opponent == "BW") | (stats.Opponent == "Lights Out") | (stats.Opponent == "ABBQ")]
# stats = stats[(stats.Opponent == "LIT") | (stats.Opponent == "Tower") | (stats.Opponent == "Robot")]
stats = stats[(stats.Action == "Catch") | (stats.Action == "Goal")]
stats = stats[stats['Event Type'] == "Offense"]
for index, row in stats.iterrows():
    gen = ""
    passer = row['Passer']
    receiver = row['Receiver']
    is_fritter = True
    p = gender[gender.Name == passer]
    r = gender[gender.Name == receiver]
    total_passes[passer] += 1
    for p in p.itertuples():
        gen = getattr(p, 'Role')
        if gen == "Female-matching": 
            is_fritter = False
            eclair_passes += 1
        elif gen == "Male-matching":
            fritter_passes += 1
    for r in r.itertuples():
        gen = getattr(r, 'Role')
        if gen == "Female-matching":
            eclair_receives += 1
            total_passes_to_eclairs[passer] += 1
            if is_fritter:
                fritter_to_eclair_pass += 1
            else:
                eclair_to_eclair_pass += 1
            if row['Action'] == "Goal":
                eclair_goals += 1
        elif gen == "Male-matching":
            fritter_receives += 1
            if is_fritter:
                fritter_to_fritter_pass += 1
            else:
                eclair_to_fritter_pass += 1
            if row['Action'] == "Goal":
                fritter_goals += 1

for name in passes_to_eclairs_percentage.keys():
    if total_passes[name] == 0:
        continue
    passes_to_eclairs_percentage[name] = round(total_passes_to_eclairs[name]/total_passes[name], 2)

print("Eclair touches: ", eclair_receives)
print("Fritter touches: ", fritter_receives)
print("Eclair touch ratio: ", round(eclair_receives/(eclair_receives + fritter_receives) , 2))
print("Eclair goals: ", eclair_goals)
print("Fritter goals: ", fritter_goals)
print("Eclair goal ratio: ", round(eclair_goals/(eclair_goals + fritter_goals), 2))
print("Percentage of fritter throws to eclairs: ", round(fritter_to_eclair_pass/fritter_passes, 2))
print("Percentage of eclair throws to eclairs: ", round(eclair_to_eclair_pass/eclair_passes, 2))
print("Percentage of throws to eclairs: ", passes_to_eclairs_percentage)
