import pandas as pd

df = pd.read_csv("athlete_events.csv")
df = df[df["Medal"].isin(["Gold", "Silver", "Bronze"])]
df.to_csv("athlete_events(1).csv", index=False)