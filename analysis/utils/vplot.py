import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import random

def barh(series, title, bar_height=0.5, fontsize=10):
	# Figure Size
    fig, ax = plt.subplots(figsize=(25, int(len(series.values) * bar_height)))
    # Horizontal Bar Plot
    ax.barh(series.keys(), series.values)
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:ax.spines[s].set_visible(False)
    # tick fontsize
    # Remove x, y Ticks
    # ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 0)
    ax.yaxis.set_tick_params(pad = 5)
    # Add x, y gridlines
    ax.grid(b = True, color ='grey',linestyle ='-.', linewidth = 0.5,alpha = 0.5)
    # Show top values
    ax.invert_yaxis()
    # Add annotation to bars
    annotation_y_offset = 0.5 + fontsize * 0.01 * 0.5
    for i in ax.patches:plt.text(i.get_width()+0.2, i.get_y()+annotation_y_offset,str(round((i.get_width()), 2)),fontsize = fontsize, fontweight ='bold',color ='grey')
    # Set tick font size
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    # Add Plot Title
    ax.set_title(title,loc ='left', fontsize=fontsize)
    # Show Plot
    plt.show()


def multi_barh(df, col_names, title, fontsize=12, fig_yscale=1):
    # Figure Size
    n_bar = len(col_names)
    sub_bar_height = 0.85/n_bar

    fig, ax = plt.subplots(figsize=(25, fig_yscale * int(len(df.index) * n_bar * sub_bar_height)))
    # Horizontal Bar Plot
    x_axis = np.arange(len(df.index))
    
    offsets = (np.linspace(0, 1, num=n_bar) - 0.5) * (n_bar-1) * sub_bar_height
    for i, col_name in enumerate(col_names):
        ax.barh(x_axis+offsets[i], df[col_name], height=sub_bar_height, align='center', label=col_name, alpha=0.90)
    
    plt.yticks(x_axis, np.array(df.index))
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:ax.spines[s].set_visible(False)
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 0)
    ax.yaxis.set_tick_params(pad = 5)
    # Add x, y gridlines
    ax.grid(b = True, color ='grey',linestyle ='-.', linewidth = 0.5,alpha = 0.5)
    # Show top values
    ax.invert_yaxis()
    # Add annotation to bars
    annotation_y_offset = sub_bar_height * 0.5 + fontsize * 0.01 * 0.5
    for i in ax.patches:plt.text(i.get_width()+0.2, i.get_y()+annotation_y_offset,str(round((i.get_width()), 2)),fontsize = fontsize, fontweight ='bold',color ='grey')
    # Add Plot Title
    ax.set_title(title,loc ='left', fontsize=fontsize)
     # Set tick font size
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)
    plt.legend(fontsize=fontsize)
    # Show Plot
    plt.show()