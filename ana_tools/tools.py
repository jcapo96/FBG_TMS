import numpy as np
import pandas as pd

def get_offsets(data):
    timestamp = data["Timestamp"]
    offsets = {}
    for ref in data.columns:
        if "Timestamp" in ref:
            continue
        doff = data.sub(data[ref], axis=0)
        doff["Timestamp"] = timestamp
        offsets[ref] = doff
    return offsets