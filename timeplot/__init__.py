""" Plot event timelines for data exploration. Pass a pandas.DataFrame and a
    matplotlib.axes.Axes to plot_events_timelime().

    The DataFrame must have the following columns (with no missing data):

      - start_date: the start date for the event
      - end_date: the end date for the event
      - event_type: a categorical variable describing the event; will be used
                    to determine line color (with the color_lookup) and will be
                    displayed in the legend; this could be, for example, the
                    data source or program type for the event
      - y: the vertical axis position of the plotted event
"""
from .timelines import plot_events_timelime

__all__ = ["plot_events_timeline"]
