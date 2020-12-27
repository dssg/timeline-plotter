# Plotting Event Series Timelines

`timeplot` is a simple Python package for plotting events on a timeline. It
arose from a common exploratory data analysis task in developing predictive
models: generating data stories about individual entities (people, buildings,
etc.). Some very basic examples are available in the [examples](examples/)
directory. The goal is to bring analysts in closer contact with their data by
allowing them to see how people (or other entities) change over time, move
among/across systems, or transition between states.

## Installation

Install the package by cloning the repository to your local disk and then
either running setup.py or installing with your favorite package manager. For
example:

```
git clone https://github.com/dssg/timeline-plotter
cd timeline-plotter
pip install .
```

## Usage

The package is simple and has a single function `plot_events_timeline()`. The
only required argument is a pandas DataFrame (`df`) that has one row per event
you would like to plot with the following columns:

  - `start_date`: the start date for the event
  - `end_date`: the end date for the event (if your events do not have end
    dates, set this equal to the `start_date`)
  - `event_type`: a categorical variable describing the event; will be used
        to determine line/marker color and will be displayed in the legend;
        this could be, for example, be the class someone is enrolling in for
        education data
  - `y`: the vertical axis position of the plotted event; sometimes, this will
    be a meaniningful value associated with the event (see the
    [train delays example](examples/train_delays)); sometimes, it is simply
    useful separate multiple overlapping events (see the
    [hotel bookings example](examples/hotel_bookings)

The function will return a `matplotlib.axes.Axes` object for display, aesthetic
refinement and/or saving.

### Optional arguments

- `ax` : You may pass in a matplotlib Axes object to plot on (`ax`).
- `custom_color_lookup` : a dictionary associating event types (keys) with
  colors(values); this is required if you have more than 8 event types, though
  you may want to reconsider your plotting strategy if you have more than 8
  categories to color).
- `show_y_axis` : By default, it is assumed that the y-values are not
  meaningful, and the y-axis is not shown. To show the y-axis, pass `True`.
- `**kwargs` : Keyword arguments to pass to `matplotlib.axes.Axes.plot()`
