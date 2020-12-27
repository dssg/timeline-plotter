import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from timeplot import plot_events_timelime


def run():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-02-26/full_trains.csv"
    delays_df = pd.read_csv(url)
    delays_df["start_date"] = pd.to_datetime(
        delays_df[["year", "month"]].astype(str).agg("-".join, axis=1),
        format="%Y-%m",
    )
    delays_df["end_date"] = delays_df["start_date"]
    delays_df.rename(
        columns={"arrival_station": "event_type", "avg_delay_all_departing": "y"},
        inplace=True,
    )
    rng = np.random.default_rng(1)
    station_indices = rng.integers(delays_df["departure_station"].nunique(), size=4)
    selected_stations = (
        delays_df["departure_station"].value_counts().iloc[station_indices].index.values
    )

    fig, axes = plt.subplots(4, sharex=True, sharey=True)
    for station, ax in zip(selected_stations, axes):
        station_df = delays_df.loc[delays_df["departure_station"] == station]
        plot_events_timelime(station_df, ax, show_y_axis=True, marker="+")
        ax.grid(axis="y")
        ax.set_title(station, loc="left")
    fig.tight_layout()

    fig.savefig("delays_timeline.png", bbox_inches="tight", dpi=600)


if __name__ == "__main__":
    run()
