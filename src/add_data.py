import numpy as np
import matplotlib.pyplot as plt

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