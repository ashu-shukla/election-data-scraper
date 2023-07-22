import pandas as pd
import json
import locale



round_wise = 'roundWise.json'
with open(round_wise, 'r') as file:
    round_json = json.load(file)

constituency_list = 'constituencyList.json'
with open(constituency_list, 'r') as file:
    constituency_json = json.load(file)


for key, value in constituency_json.items():
    table_data = round_json[value]
    df = pd.concat([pd.DataFrame(v) for k, v in table_data.items()], keys=table_data.keys(
    )).reset_index(level=0).rename(columns={"level_0": "Round"})
    # Remove leading/trailing whitespaces from column names
    df = df.rename(columns=lambda x: x.strip())

    # Convert numerical columns to numeric data type
    numeric_columns = [
        "Votes Brought From Previous Rounds (EVM Votes)", "Current Round (EVM Votes)", "Total"]
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

    # Convert "Round" column to numeric and sort the DataFrame
    df["Round"] = df["Round"].astype(int)
    df = df.sort_values("Round")

    # Format numeric columns with Indian-style commas
    df[numeric_columns] = df[numeric_columns].applymap(
    lambda x: locale.format_string("%d", x, grouping=True))

    # Pivot the DataFrame
    pivot_df = df.pivot(index=["Candidate", "Party"],
                        columns="Round", values="Total").reset_index()
    
    # Filter out the row with empty "Candidate" and "Party" values
    pivot_df = pivot_df[(pivot_df["Candidate"] != "") &
                    (pivot_df["Party"] != "Total")]

    # Add prefix to the round columns
    pivot_df.columns = ["Candidate", "Party"] + \
        ["Round-" + str(col) for col in pivot_df.columns[2:]]
    # Display the DataFrame
    print(pivot_df)
    # Save the DataFrame to CSV
    pivot_df.to_csv(f'csv-roundwise/roundwise-{value}.csv', index=False)



