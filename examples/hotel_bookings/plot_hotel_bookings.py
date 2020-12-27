import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from timeplot import plot_events_timelime


COLORS = {"Canceled": "orange", "Check-Out": "green", "No-Show": "red"}


def run():
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-02-11/hotels.csv"
    bookings_df = pd.read_csv(url)
    bookings_df["start_date"] = pd.to_datetime(
        bookings_df[
            ["arrival_date_year", "arrival_date_month", "arrival_date_day_of_month"]
        ]
        .astype(str)
        .agg("-".join, axis=1),
        format="%Y-%B-%d",
    )
    bookings_df["end_date"] = pd.to_datetime(
        bookings_df[
            ["arrival_date_year", "arrival_date_month", "arrival_date_day_of_month"]
        ]
        .astype(str)
        .agg("-".join, axis=1),
        format="%Y-%B-%d",
    ) + pd.to_timedelta(
        bookings_df["stays_in_weekend_nights"] + bookings_df["stays_in_week_nights"],
        "days",
    )
    bookings_df = bookings_df.loc[bookings_df["agent"].notnull()]
    bookings_df.rename(columns={"reservation_status": "event_type"}, inplace=True)
    rng = np.random.default_rng(321)
    agent_indices = rng.integers(bookings_df["agent"].nunique(), size=4)
    selected_agents = (
        bookings_df["agent"].value_counts().iloc[agent_indices].index.values
    )

    fig, axes = plt.subplots(4, sharex=True)
    for agent, ax in zip(selected_agents, axes):
        agent_df = bookings_df.loc[bookings_df["agent"] == agent].assign(
            y=rng.integers(40, size=len(bookings_df.loc[bookings_df["agent"] == agent]))
        )
        plot_events_timelime(
            agent_df, ax, custom_color_lookup=COLORS, markersize=2, linewidth=1
        )
        ax.get_legend().remove()
        ax.set_title(f"Agent {int(agent)}", loc="left")
    custom_lines = [
        Line2D([0], [0], color=COLORS[event_type], lw=4)
        for event_type in bookings_df["event_type"].unique()
    ]
    fig.legend(
        custom_lines,
        bookings_df["event_type"].unique(),
        loc="upper center",
        ncol=3,
    )
    fig.tight_layout()

    fig.savefig("bookings_timeline.png", bbox_inches="tight", dpi=600)


if __name__ == "__main__":
    run()
