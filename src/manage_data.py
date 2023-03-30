import pandas as pd
import numpy as np
import datetime
import pytz
import add_data, read_files
from tqdm import tqdm

def time_to_seconds(timestamp):
    try:
        date, time = timestamp.split("-")
        month, day, year = [int(x) for x in date.split("/")]
        h, m, s = [int(x) for x in time.split(":")]
        epoch = datetime.datetime(year, day, month, h, m, s).timestamp()
    except:
        try:
            start = datetime.datetime(1900, 1, 1, 0, 0, 0, 0, pytz.UTC)  # interrogator time epoch (time zero)
            time_arr = start + timestamp/1e6 * datetime.timedelta(milliseconds=1)
            epoch = time_arr.timestamp()
        except:
            date, time = timestamp.split(" ")
            year, month, day = [int(x) for x in date.split("-")]
            h, m, s = [int(x) for x in time.split(":")]
            epoch = datetime.datetime(year, month, day, h, m, s).timestamp()
    return epoch

def downsample_data(df, bin=1):
    df["Timestamp"] = df["Timestamp"].apply(lambda x: np.round(x/bin, 0))
    downsampled = []
    unique_times = df["Timestamp"].unique()
    progress_bar = tqdm(total=len(unique_times), desc="Downsampling data")
    for time in unique_times:
        chunk = df.loc[df["Timestamp"] == time]
        row = {}
        for col in chunk:
            if col == "Date" or col=="Time" or col=="Datetime" or col == "PolMask":
                continue
            if col == "Timestamp":
                row[col] = time
            if col != "Timestamp":
                row[col] = np.mean(chunk[col])
                row[col+"_err"] = np.std(chunk[col])
        downsampled.append(row)
        progress_bar.update(1)
    progress_bar.close()
    downsampled = pd.DataFrame(downsampled)
    return downsampled

def match_dataframes(df1, df2):
    min_df1 = np.min(df1["Timestamp"])
    min_df2 = np.min(df2["Timestamp"])
    if (min_df1 < min_df2):
        min_time = min_df2
    else:
        min_time = min_df1
    max_df1 = np.max(df1["Timestamp"])
    max_df2 = np.max(df2["Timestamp"])
    if (max_df1 < max_df2):
        max_time = max_df1
    else:
        max_time = max_df2
    
    df1 = df1[(df1["Timestamp"] >= min_time) & (df1["Timestamp"] <= max_time)].reset_index(drop=True)
    df2 = df2[(df2["Timestamp"] >= min_time) & (df2["Timestamp"] <= max_time)].reset_index(drop=True)

    df1 = df1.drop_duplicates(subset="Timestamp")
    df2 = df2.drop_duplicates(subset="Timestamp")

    df1 = df1.loc[(df1["Timestamp"].isin(df2["Timestamp"]))].reset_index(drop=True)
    df2 = df2.loc[(df2["Timestamp"].isin(df1["Timestamp"]))].reset_index(drop=True)

    return df1, df2