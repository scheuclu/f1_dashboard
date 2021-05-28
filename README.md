# F1 betting dashboard

Me and a friend are strong Formula 1 fans.\
This dashboard is about finding out who's the bigger armchair expert.

## Usage
Before each race, each player makes a guess on what the race result will look like.\
Bet's have to be placed before qualifying starts.

When the race results are in, the bets are scored.
The scoring rewards unlikely bets.

## Architecture
The dashboard is built using [Plotly Dash](https://dash.plotly.com/).
There is no database yet, so a [Google Sheet](https://docs.google.com/spreadsheets/d/1x0zhN8QqieIfCI1y6zPilkL8od1rUjkinRN3XA0kBzE/edit#gid=1548037137) is used to place bets for the time bein.


## Hosting

The dashboard is dockerized and [published](https://f1-betting-313907-fo225mxnma-uc.a.run.app) on Google Cloud using Github workflows.
