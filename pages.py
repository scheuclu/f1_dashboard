import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table

import config as conf
import elements as elem
import graphs


def generate_graphs(driver2stat):
    return {driver: graphs.get_driverstat_graph(driver2stat[driver]) for driver in driver2stat.keys()}


def get_per_race_points(driver2stat):
    return [
        # dcc.Store(id="store", data=generate_graphs(driver2stat)),
        # dbc.Row(dbc.Col(elem.driver_buttons)),
        # html.H2(children='', id="button_selection"),
        # html.Hr(),
        # html.Div(id="tab-content", className="p-4"),
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
            src='https://raw.githubusercontent.com/scheuclu/f1_dashboard/main/img/tracks/Bahrain.png',
            width='50%')
        # dbc.Row([
        #     dbc.Col(dcc.Graph(figure=fig_standings)),
        #     dbc.Col(dcc.Graph(figure=fig_races)),
        # ]),
        # dbc.Row(dbc.Alert("Next race: Baku, 2021/06/04", color="secondary"))  # TODO(scheuclu) Automate this.
    ],
        fluid=True)


def get_scoring():
    return [
        html.P("The scoring system rewards 'unlikely' bets, if they work out."),
        html.P("For example, correctly guessing the driver on championship position 10 to win the race gives more points than guessing that the leader will win."),
        html.P("Points are given if the race result of a driver is guesses within 3 places. Being spot on or just one-off gives extra points."),
        html.P("Theres also a point bonus for the podium positions"),

        dcc.Graph(figure=graphs.get_scoring())]


def get_data(races2data):
    # race_selector = dbc.DropdownMenu(
    #     id='data_race_selector',
    #     label="Select the race",
    #     children=[dbc.DropdownMenuItem(children=race, id=race, key=race) for race in conf.races]
    # )

    race_selector =dcc.Dropdown(
        id='data_race_selector',
        options=[ {'label': race, 'value': race} for race in conf.races],
        value='Monaco',
        style={
            'backgroundColor': 'white', #selected bg
             'color': 'black', #dropdown text
             'foregroundColor': 'yellow',
            #'background': 'transparent'
            # 'text':{'color': 'green'},
            # 'input': {'color': 'blue'}

        }
    )

    df=races2data['Monaco']
    df=df.reset_index()

    style_header_conditional=[
        {
            'if': {
                'column_id': driver,
            },
            'backgroundColor': conf.teamcolor[conf.driver2team[driver]],
            'color': 'black' if conf.driver2team[driver]=='Haas' else 'white',
            'textAlign': 'center',
            'fontSize': 16
        } for driver in conf.drivers
    ]



    table =  dash_table.DataTable(
        id='table_data',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        #style_header={'backgroundColor': conf.players['lukas']['color']},
        style_cell={
            'backgroundColor': 'rgba(50, 50, 50, 0)',
            'color': 'white',
            'fontSize': 14
        },
        style_header_conditional=style_header_conditional,
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(50, 50, 50)'
        }] ,
    )

    return [
        race_selector,
        html.Hr(),
        table,
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Input(id="pw_input", placeholder="Enter access code...", type="text"),

            ),
            dbc.Col(
                dbc.Button("Save and recompute scores", id="recompute_button",  color="primary", block=True)
            ),
        ])

    ]