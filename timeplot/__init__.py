""" Plot event timelines for data exploration. Pass a pandas.DataFrame and a
    matplotlib.axes.Axes to plot_events_timelime().

    The DataFrame must have the following columns (with no missing data):

      - start_date: the start date for the event
      - event_type: a categorical variable describing the event; will be used
                    to determine line color (with the color_lookup) and will be
                    displayed in the legend; this could be, for example, the
                    data source or program type for the event
      - y: the vertical axis position of the plotted event

    For events that have a duration, you may also include an additional column
    to plot the event as a line indicating its length:

      - end_date: the end date for the event
"""
from matplotlib.lines import Line2D
import matplotlib
from matplotlib import pyplot as plt
import pandas


__all__ = ["plot_events_timeline"]


matplotlib.use("agg")

DEFAULT_COLORS = [
    "#1b9e77",
    "#d95f02",
    "#7570b3",
    "#e7298a",
    "#66a61e",
    "#e6ab02",
    "#a6760d",
    "#666666",
]


def _make_default_color_lookup(event_types):
    """
    If no colors are supplied, create a default color mapping for event types.

    Parameters
    ----------
    event_types : array-like
        The event types observed in the dataset.

    Returns
    -------
    dict
    """
    n_events = len(event_types)
    if n_events > len(DEFAULT_COLORS):
        raise LookupError(
            f"There are more event types ({n_events}) than default colors "
            + f"({len(DEFAULT_COLORS)}). Please provide a custom color lookup."
        )

    return dict(zip(event_types, DEFAULT_COLORS))


def _validate_dataframe(df):
    """
    Validate the provided DataFrame meets the requirements

    Parameters
    ----------
    df: pandas.DataFrame
        The data to validate. Must have the columns start_date, event_type, and
        y. start_date and end_date (if provided) must be able to be converted
        to datetimes

    Returns
    -------
    None
    """
    if not all(name in df.columns for name in ["start_date", "event_type", "y"]):
        raise KeyError(
            "The provided DataFrame is missing at least one of the required columns: start_date, event_type, y"
        )
    try:
        pandas.to_datetime(df["start_date"])
    except ValueError:
        raise TypeError("start_date not convertible to datetime")
    if "end_date" in df.columns:
        try:
            pandas.to_datetime(df["end_date"])
        except ValueError:
            raise TypeError("end_date not convertible to datetime")


def plot_events_timeline(
    df,
    ax=None,
    custom_color_lookup=None,
    show_y_axis=False,
    **kwargs,
):
    """
    Make plots event series.

    Parameters
    ----------
    df : pandas.DataFrame
        The data to plot. Must have the following columns:
          - start_date: the start date for the event
          - event_type: a categorical variable describing the event; will be
                        used to determine line color (with the color_lookup)
                        and will be displayed in the legend; this could be, for
                        example, the data source or program type for the event
          - y: the vertical axis position of the plotted event

        For events that have a duration, you may also include an additional
        column to plot the event as a line indicating its length:

          - end_date: the end date for the event
    ax : matplotlib.axes.Axes, default None
        The axes on which to draw the plot.
    custom_color_lookup : dict, default None
        A dictionary containing event types (keys) and associated colors
        (values) for plotting; must contain all of the event types being
        plotted.
    show_y_axis : bool, default False
        Whether to show the y-axis ticks and tick labels.
    **kwargs
        Options to pass to matplotlib plotting method.

    Returns
    -------
    matplotlib.axes.Axes

    Notes
    -----
    - See matplotlib documentation for details about configuring the plots
    - If events do not have end times, set end_time = start_time
    """
    _validate_dataframe(df)

    if not ax:
        fig, ax = plt.subplots()

    kwargs.setdefault("linewidth", 4)
    kwargs.setdefault("linestyle", "-")
    kwargs.setdefault("marker", "s")
    kwargs.setdefault("markersize", 4)

    # get or assign colors for event types
    event_types = df.event_type.unique()
    if custom_color_lookup:
        color_lookup = custom_color_lookup
    else:
        color_lookup = _make_default_color_lookup(event_types)

    # plot the lines and event text
    for row in df.itertuples():
        if "end_date" in df:
            x = [row.start_date, row.end_date]
        else:
            x = [row.start_date]
        y = [row.y for date in x]
        ax.plot(x, y, color=color_lookup[row.event_type], **kwargs)

    ax.tick_params(
        axis="both",
        left=show_y_axis,
        top=False,
        right=False,
        labeltop=False,
        labelleft=show_y_axis,
        labelright=False,
    )

    custom_lines = [
        Line2D([0], [0], color=color_lookup[event_type], lw=4)
        for event_type in event_types
    ]
    ax.legend(
        custom_lines,
        event_types,
    )

    return ax
