import numpy as np
import pandas as pd
import datetime
import pytz
import matplotlib.pyplot as plt

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

def add_polarisation_mask(data):
    first_row = data["Wav1-1"][0]
    second_row = data["Wav1-1"][1]

    polarisation_mask = []
    if first_row > second_row:
        first_pol = "p"
        second_pol = "s"
    else:
        first_pol = "s"
        second_pol = "p"
    for i in range(len(data)):
        if i % 2 == False:
            polarisation_mask.append(first_pol)
        else:
            polarisation_mask.append(second_pol)
    data["PolMask"] = polarisation_mask
    return data

def find_zero_derivative_regions(curve, threshold):
    """
    Given a list of numbers representing a curve and a threshold for the minimum region length, 
    returns a list of tuples representing the regions where the derivative of the curve is zero 
    and has a length above the threshold.
    Each tuple contains the start and end indices of a region.
    """
    zero_regions = []
    start_idx = None
    for i in range(len(curve) - 1):
        if curve[i] == curve[i + 1]:
            if start_idx is None:
                start_idx = i
        elif start_idx is not None:
            region_length = i - start_idx
            if region_length >= threshold:
                zero_regions.append((start_idx, i))
            start_idx = None
    if start_idx is not None:
        region_length = len(curve) - 1 - start_idx
        if region_length >= threshold:
            zero_regions.append((start_idx, len(curve) - 1))
    return zero_regions