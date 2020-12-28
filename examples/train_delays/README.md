# Train Delays

This example uses
[data on delays for French train routes](https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-02-26).
The data are aggregated by train route and month and contain information about
the departure station, arrival station, departure delay, arrival delay, the
number of trips, and the distribution of delay causes, among other variables.
For this exploration, we will look at departure delays (in minutes) for trains
leaving four randomly selected stations by their destination station.

![Departure delay timelines for four stations](delays_timeline.png)

We can see that the stations vary amongst themselves in their tendencies for
trains to leave late. Whereas passengers at Tours will typically leave on time
or only a minute or two late, passengers at Nimes and Toulon will often leave
a few minutes or more late, even though they are headed to the same
destination. We can also see that departure delays from Paris Nord to different
destinations are correlated: Delay increases and decreases seem to affect all
routes. Finally, we observe at least one *negative* delay at Tours. Is this an
error, or does this indicate that trains departed on average early in December
2017.

Discussion of these observations with station owners, train operators, etc.
could be informative for model building and illuminate issues with data quality
and interpretation.
