import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

import dash_bootstrap_components as dbc
import config as conf

header = html.Div(
    children=[
        html.H2(children='F1 2021 betting :)', style={"text-align": "center"}),
        html.H3("This is work in progress"),
        html.Hr()],
    style={"text-align": "center"})

driver_buttons = dbc.Row(
    [dbc.Col(html.Button(driver, style={'background-color': conf.teamcolor[conf.driver2team[driver]]},
                         id="button-" + driver)) for driver in conf.drivers],
    no_gutters=True
)

teamcolor = {
    'Mercedes': '#00D2BE',
    'Ferrari': '#DC0000',
    'Red Bull Racing': '#0600EF',
    'Alpine': '#0090FF',
    'Haas': '#FFFFFF',
    'Aston Martin': '#006F62',
    'Alpha Tauri': '#2B4562',
    'McLaren': '#FF8700',
    'Alfa Romeo Racing': '#900000',
    'Williams': '#005AFF'
}

buttons = dbc.Row(
    [
        dbc.Col(html.Button("HAM", style={'background-color': teamcolor['Mercedes']}, id="button-driver-ham")),
        dbc.Col(html.Button("BOT", style={'background-color': teamcolor['Mercedes']})),
        dbc.Col(html.Button("VER", style={'background-color': teamcolor['Red Bull Racing']}, id="button-driver-ver")),
        dbc.Col(html.Button("PER", style={'background-color': teamcolor['Red Bull Racing']})),
        dbc.Col(html.Button("RIC", style={'background-color': teamcolor['McLaren']})),
        dbc.Col(html.Button("NOR", style={'background-color': teamcolor['McLaren']})),
        dbc.Col(html.Button("VET", style={'background-color': teamcolor['Aston Martin']})),
        dbc.Col(html.Button("STR", style={'background-color': teamcolor['Aston Martin']})),
        dbc.Col(html.Button("OCO", style={'background-color': teamcolor['Alpine']})),
        dbc.Col(html.Button("ALO", style={'background-color': teamcolor['Alpine']})),
        dbc.Col(html.Button("LEC", style={'background-color': teamcolor['Ferrari']})),
        dbc.Col(html.Button("SAI", style={'background-color': teamcolor['Ferrari']})),
        dbc.Col(html.Button("GAS", style={'background-color': teamcolor['Alpha Tauri']})),
        dbc.Col(html.Button("TSU", style={'background-color': teamcolor['Alpha Tauri']})),
        dbc.Col(html.Button("RAI", style={'background-color': teamcolor['Alfa Romeo Racing']})),
        dbc.Col(html.Button("GIO", style={'background-color': teamcolor['Alfa Romeo Racing']})),
        dbc.Col(html.Button("MSC", style={'background-color': teamcolor['Haas']})),
        dbc.Col(html.Button("MZP", style={'background-color': teamcolor['Haas']})),
        dbc.Col(html.Button("RUS", style={'background-color': teamcolor['Williams']})),
        dbc.Col(html.Button("LAT", style={'background-color': teamcolor['Williams']})),
    ],
    no_gutters=True

)

radio = dcc.RadioItems(
    options=[
        {'label': 'HAM', 'value': 'NYC'},
        {'label': 'BOT', 'value': 'BOT'},
        {'label': 'PER', 'value': 'VER'}
    ],
    value='MTL',
    labelStyle={'display': 'inline-block'}
)
