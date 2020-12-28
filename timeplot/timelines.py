from matplotlib.lines import Line2D
import matplotlib

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

    return {event_types[i]: DEFAULT_COLORS[i] for i in range(n_events)}


def plot_events_timelime(
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
        The data to plot.
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
    if not ax:
        fig, ax = matplotlib.pyplot.subplots()

    if "linewidth" not in kwargs:
        kwargs["linewidth"] = 4
    if "linestyle" not in kwargs:
        kwargs["linestyle"] = "-"
    if "marker" not in kwargs:
        kwargs["marker"] = "s"
    if "markersize" not in kwargs:
        kwargs["markersize"] = 4

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
