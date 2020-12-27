import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from timeplot import plot_events_timelime


def run():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-06-09/firsts.csv"
    achievements_df = pd.read_csv(url)
    achievements_df["start_date"] = pd.to_datetime(achievements_df["year"], format="%Y")
    achievements_df["end_date"] = pd.to_datetime(achievements_df["year"], format="%Y")
    achievements_df.rename(columns={"category": "event_type"}, inplace=True)

    # We'll plot each achievement category in a separate "band" on the y-axis.
    # The width of a band will be proportional to the maximum number of events
    # of the same type to occur in year. Figure out the floor and ceiling for
    # each of the bands.
    achievements_df["event_in_year"] = (
        achievements_df.groupby(["event_type", "year"]).cumcount() + 1
    )
    max_achievements_per_year = (
        achievements_df.groupby("event_type")["event_in_year"].max().sort_values()
    )
    ceiling_values = max_achievements_per_year.cumsum().rename("ceiling_value")
    floor_values = ceiling_values.shift(1, fill_value=0).rename("floor_value")
    achievements_df = (
        achievements_df.join(ceiling_values, "event_type")
        .join(floor_values, "event_type")
        .sort_values("floor_value")
    )

    # When events in subsequent years are plotted right next to each other,
    # they are hard to tell appart, so we will add some "jitter" within the
    # bands by randomizing the y-axis position within the band, leaving a small
    # buffer under the ceiling to give clean separation between the bands.
    rng = np.random.default_rng(321)
    achievements_df["y"] = achievements_df.apply(
        lambda x: rng.random() * (x.ceiling_value - 0.5 - x.floor_value)
        + x.floor_value,
        axis=1,
    )

    fig, ax = plt.subplots()
    plot_events_timelime(ax, achievements_df, None, linewidth=1, markersize=1)


    fig.savefig("african_american_achievements_timeline.png", bbox_inches="tight", dpi=600)


if __name__ == "__main__":
    run()
