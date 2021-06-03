import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import config as conf
import elements as elem
import graphs
import dash_daq as daq


def generate_graphs(driver2stat):
    return {driver: graphs.get_driverstat_graph(driver2stat[driver]) for driver in driver2stat.keys()}


def get_per_race_points(driver2stat):
    return [
        dcc.Store(id="store", data=generate_graphs(driver2stat)),
        dbc.Row(dbc.Col(elem.driver_buttons)),
        html.H2(children='', id="button_selection"),
        html.Hr(),
        html.Div(id="tab-content", className="p-4"),
    ]


def get_overview(driver2stat):
    cumpoints = pd.DataFrame(columns=conf.drivers, index=conf.races)
    for driver in conf.drivers:
        cumsum = 0
        for race in conf.races:
            cumsum += driver2stat[driver][race]['Lukas points']
            cumpoints[driver][race] = cumsum
    return [dcc.Graph(id='test', figure=graphs.get_cumpoints_graph(cumpoints), style={'height': '40rem'})]


def get_home(driver2stat):
    lukas_points = sum([stat.loc['Lukas points'].sum() for driver, stat in driver2stat.items()])
    patrick_points = sum([stat.loc['Patrick points'].sum() for driver, stat in driver2stat.items()])
    lisa_points = sum([stat.loc['Lisa points'].sum() for driver, stat in driver2stat.items()])
    max_points=max(lukas_points, patrick_points, lisa_points)
    style={'height': '1rem'}


    #fig_standings, fig_races = graphs.get_overview(lukas_points, patrick_points, 5, 18)
    common_args = dict(striped=False, style=style, max=max_points, className="mb-3")
    return dbc.Container([
        html.H4("Standings"),

        dbc.Progress(f'Lukas: {lukas_points}', value=lukas_points, color=conf.players['lukas']['color'], **common_args),
        dbc.Progress(f'Patrick: {patrick_points}', value=patrick_points, color=conf.players['patrick']['color'], **common_args),
        dbc.Progress(f'Lisa: {lisa_points}', value=lisa_points, color=conf.players['lisa']['color'], **common_args),
        html.Hr(),
        html.H4("Season Progress"),
        dbc.Progress("Finished: 5/23", value=40, color="#FF1801", striped=True, style=style),

        html.Hr(),
        html.H4("Next Race: Azerbaijan"),
        html.Img(
            src='https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Baku_Circuit.png.transform/7col-retina/image.png',
            width='50%')
        # dbc.Row([
        #     dbc.Col(dcc.Graph(figure=fig_standings)),
        #     dbc.Col(dcc.Graph(figure=fig_races)),
        # ]),
        # dbc.Row(dbc.Alert("Next race: Baku, 2021/06/04", color="secondary"))  # TODO(scheuclu) Automate this.
    ],
        fluid=True)


def get_scoring():
    return [dcc.Graph(figure=graphs.get_scoring())]
