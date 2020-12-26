import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from timeplot import plot_events_timelime


np.random.seed(1234)


def run():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-06-09/firsts.csv"
    achievements_df = pd.read_csv(url)
    achievements_df["start_date"] = pd.to_datetime(achievements_df["year"], format="%Y")
    achievements_df["end_date"] = pd.to_datetime(achievements_df["year"], format="%Y")
    achievements_df.rename(columns={"category": "event_type"}, inplace=True)
    achievements_df["decade"] = (achievements_df["year"] / 10).astype(int)
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
    achievements_df["y"] = achievements_df.apply(
        lambda x: np.random.random() * (x.ceiling_value - 0.5 - x.floor_value)
        + x.floor_value,
        axis=1,
    )
    achievements_df.to_csv("test.csv")
    fig, ax = plt.subplots()
    plot_events_timelime(ax, achievements_df, None, linewidth=1, markersize=1)

    fig.savefig("african_american_achievements_timeline.png")


if __name__ == "__main__":
    run()
