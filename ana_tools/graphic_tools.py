import matplotlib.pyplot as plt

def make_figure(ncols=2, nrows=2):
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, constrained_layout=True)
    try:
        axises = []
        for i in axes:
            for j in i:
                axises.append(j)
    except:
        axises = axes
    return fig, axises

def get_twin_axes(axes):
    twin_axes = []
    for ax in axes:
        twin_axes.append(ax.twinx())
    return twin_axes