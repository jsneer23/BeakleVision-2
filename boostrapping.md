# Bootstrapping Data for Local Development

## TBA Match Data

There are endpoints located at `api/v1/tba/` intended for bootstrapping data to your local development environment. You can ping `teams` which will fetch all FRC teams. Next ping `events/{year}` to get the list of events from a specific year. Finally ping `matches/{year}` to fetch matches for a year. The matches ping requires that the events for the year are already loaded.