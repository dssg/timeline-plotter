""" This file contains a class to plot event timelines for data exploration.
    Initialize the class with some optional graphical settings. Then pass a
    pandas.DataFrame, matplotlib.axes.Axes, and legend location (optional) to
    run().

    The DataFrame must have the following columns (with no missing data):

      - start_date: the start date for the event
      - end_date: the end date for the event
      - event_type: a categorical variable describing the event; will be used
                    to determine line color (with the color_lookup) and will be
                    displayed in the legend; this could be, for example, the
                    data source or program type for the event
      - y: the vertical axis position of the plotted line

    Additionally, you may include the following column to add annotations to
    the events:

      - event_text: a string to print to the right of each event on the
                    timeline; if you want nothing printed, send an empty string
"""

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
    "#a6761d",
    "#666666",
]


def _make_default_color_lookup(event_types):
    n_events = len(event_types)
    if n_events > len(DEFAULT_COLORS):
        raise LookupError(
            f"There are more event types ({n_events}) than default colors "
            + f"({len(DEFAULT_COLORS)}). Please provide a custom color lookup."
        )

    return {event_types[i]: DEFAULT_COLORS[i] for i in range(n_events)}


def _plot_lines(
    ax,
    df,
    x_value_range,
    y_value_range,
    custom_color_lookup,
    event_text_vertical_alignment,
    kwargs,
):
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
        x = (row.start_date, row.end_date)
        y = (row.y, row.y)
        ax.plot(x, y, color=color_lookup[row.event_type], **kwargs)
        if "event_text" in df:
            ax.text(
                row.end_date + (x_value_range / 60),
                row.y + (y_value_range * event_text_vertical_alignment),
                row.event_text,
            )

    return ax


def _configure_plot_aesthetics(
    ax,
    df,
    x_value_range,
    y_value_range,
    custom_color_lookup,
):
    ax.tick_params(
        axis="both",
        left=False,
        top=False,
        right=False,
        labeltop=False,
        labelleft=False,
        labelright=False,
    )

    # legend
    event_types = df.event_type.unique()
    if custom_color_lookup:
        color_lookup = custom_color_lookup
    else:
        color_lookup = _make_default_color_lookup(event_types)
    custom_lines = [
        Line2D([0], [0], color=color_lookup[event_type], lw=4)
        for event_type in event_types
    ]
    ax.legend(
        custom_lines,
        event_types,
    )


def plot_events_timelime(
    ax,
    df,
    custom_color_lookup=None,
    event_text_vertical_alignment=None,
    **kwargs,
):

    x_value_range = df.end_date.max() - df.start_date.min()
    y_value_range = df.y.max() - df.y.min()

    ax = _configure_plot_aesthetics(
        _plot_lines(
            ax,
            df,
            x_value_range,
            y_value_range,
            custom_color_lookup,
            event_text_vertical_alignment,
            kwargs,
        ),
        df,
        x_value_range,
        y_value_range,
        custom_color_lookup,
    )

    return ax
