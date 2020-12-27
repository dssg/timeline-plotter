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

    return ax


def _configure_plot_aesthetics(
    ax,
    df,
    custom_color_lookup,
    show_y_axis,
):
    ax.tick_params(
        axis="both",
        left=show_y_axis,
        top=False,
        right=False,
        labeltop=False,
        labelleft=show_y_axis,
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
    show_y_axis=False,
    **kwargs,
):
    ax = _configure_plot_aesthetics(
        _plot_lines(
            ax,
            df,
            custom_color_lookup,
            event_text_vertical_alignment,
            kwargs,
        ),
        df,
        custom_color_lookup,
        show_y_axis,
    )

    return ax
