import pandas as pd
import json

# Load JSON file
with open("Scrapped/Con_Dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert JSON to DataFrame
df = pd.DataFrame(data)

# Save as CSV
df.to_csv("JSON_Con_CSV.csv", index=False, encoding="utf-8")

print("✅ JSON converted to CSV successfully!")
