""" This file contains a class to plot event timelines for data exploration.
    Initialize the class with some optional graphical settings. Then pass a
    pandas.DataFrame, plot title, filename (optional), and legend location
    (optional) to run().

    The DataFrame must have the following columns (with no missing data):

      - start_date: the start date for the event
      - end_date: the end date for the event
      - event_text: a string to print to the right of each event on the
                    timeline; if you want nothing printed, send an empty string
      - event_type: a categorical variable describing the event; will be used
                    to determine line color (with the color_lookup) and will be
                    displayed in the legend; this could be, for example, the
                    data source or program type for the event
      - y: the vertical axis position of the plotted line
"""

import os,sys,inspect
import datetime

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
from datetime import timedelta 


DEFAULT_COLORS = [
    '#1b9e77',
    '#d95f02',
    '#7570b3',
    '#e7298a',
    '#66a61e',
    '#e6ab02',
    '#a6761d',
    '#666666'
]


def make_default_color_lookup(event_types):
    n_events = len(event_types)
    if n_events > len(DEFAULT_COLORS):
        raise LookupError(
            f'There are more event types ({n_events}) than default colors ' +
            f'({len(default_colors)}). Please provide a custom color lookup.'
        )
    
    return {event_types[i]:DEFAULT_COLORS[i] for i in range(n_events)}


def set_image_filepath(filepath=None, title=None):
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    if filepath:
        filepath = filepath
    elif title:
        filepath = os.path.join(currentdir, f'{title}.png')
    else:
        filepath = os.path.join(currentdir, 'timeline_plot.png')


class TimelinePlotter():
    def __init__(
        self,
        custom_color_lookup=None,
        linewidth=4,
        linestyle='-',
        marker='s',
        markersize=4,
        x_axis_margins=(.05, .05),
        display_vertical_grid=True,
        vertical_grid_color='lightgray',
        display_y_axis=False,
        y_axis_label='',
        y_axis_margins=(.05, .05),
        event_text_vertical_alignment=-.01,
        figure_size_horizontal=6,
        figure_size_vertical=None
    ):
        self.custom_color_lookup = custom_color_lookup
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.marker = marker
        self.markersize = markersize
        self.x_axis_margins = x_axis_margins
        self.display_vertical_grid = display_vertical_grid
        self.vertical_grid_color = vertical_grid_color
        self.display_y_axis = display_y_axis
        self.y_axis_label = y_axis_label
        self.y_axis_margins = y_axis_margins
        self.event_text_vertical_alignment = event_text_vertical_alignment
        self.figure_size_horizontal = figure_size_horzontal
        self.figure_size_vertial = figure_size_vertical

    def _get_plotting_attribute(self, attribute, row):
            if attribute in row._fields:
                return getattr(row, attribute)
            else:
                return getattr(self, attribute)

    def _plot_lines(seld, df, x_value_range, y_value_range):
        # get or assign colors for event types
        event_types = df.event_type.unique()
        if self.custom_color_lookup:
            color_lookup = self.custom_color_lookup
        else:
            color_lookup = make_default_color_lookup(event_types)

        # make the axes
        figure_size_vertical = self.figure_size_vertical
        if figure_size_vertical is None:
            figure_size_vertical = len(df.y) / 3.5)
        fig, ax = plt.subplots(figsize=(self.figure_size_horizontal, figure_size_vertical))

        # plot the lines and event text
        for row in df.itertuples():
            x = (row.start_date, row.end_date)
            y = (row.y, row.y)
            ax.plot(
                x,
                y,
                lw=self._get_plotting_attribute('linewidth', row),
                linestyle=self._get_plotting_attribute('linestyle', row),
                marker=self._get_plotting_attribute('marker', row),
                markersize=self._get_plotting_attribute('markersize', row),
                color=color_lookup[row.event_type]
            )
            ax.text(
                row.end_date + (x_value_range / 60),
                row.y + (y_value_range * self.event_text_vertical_alignment),
                row.event_text
            )

        return ax

    def _configure_plot_aesthetics(self, ax, df, x_value_range, y_value_range, title=None):
        # x -axis
        ax.set_xlim(
            df.start_date.min() - (x_value_range * self.x_axis_margins[0]),
            df.end_date.max() + (x_value_range * self.x_axis_margins[1])
        )
        ax.xaxis.grid(self.display_vertical_grid, color=self.vertical_grid_color)
        
        # y-axis
        ax.set_ylim(
            df.y.min() - (y_value_range * self.y_axis_margins[0]),
            df.y.max() + (y_value_range * self.y_axis_margins[1])
        )
        ax.set_ylabel(self.y_axis_label)
        ax.tick_params(
            axis='both',
            left=self.display_y_axis,
            top=False,
            right=False,
            labeltop=False,
            labelleft=self.display_y_axis,
            labelright=False
        )

        # title
        ax.set_title(title)

        # legend
        custom_lines = [Line2D([0], [0], color=color_lookup[event_type], lw=4) for event_type in event_types]
        ax.legend(custom_lines, event_types, loc=legend_position, bbox_to_anchor=bbox_to_anchor)

    def run(
            self,
            df,
            title=None,
            filepath=None,
            legend_position='upper left',
            bbox_to_anchor=None
        ):

        x_value_range = df.end_date.max() - df.start_date.min()
        y_value_range = df.y.max() - df.y.min()
        
        ax = self._configure_plot_aesthetics(
            self._plot_lines(df, x_value_range, y_value_range),
            df,
            x_value_range,
            y_value_range,
            title
        )

        if filepath is not None:
            plt.savefig(filepath, bbox_inches='tight', pad_inches=0.1, dpi=300)

        return ax

