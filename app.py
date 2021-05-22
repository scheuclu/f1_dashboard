"""
TODO
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

import graphs
import elements as elem
import pickle
import os
import config as conf
import base64


def generate_graphs(driver2stat):
    return {driver: graphs.get_driverstat_graph(driver2stat[driver]) for driver in driver2stat.keys()}

# Read data
cache = './races2data.pickle'
if os.path.isfile(cache):
    races2data = pickle.load(open(cache, "rb"))
    print("Loaded from cache")
else:
    races2data = {race: pd.read_excel(conf.path, sheet_name=race, usecols="A:U", index_col=0, header=19).iloc[0:9] for
                  race
                  in conf.races}
    with open(cache, 'wb') as f:
        pickle.dump(races2data, f)

driver2image = {driver: base64.b64encode(open(f'./img/{driver}.png', 'rb').read()) for driver in conf.drivers}

# Compute driver statistics
driver2stat = {driver: pd.DataFrame(index=races2data["Imola"].index, columns=conf.races) for driver in conf.drivers}
for driver in conf.drivers:
    for race in conf.races:
        driver2stat[driver][race] = races2data[race][driver]

# App layout
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
app.layout = dbc.Container(
    [
        dcc.Store(id="store", data=generate_graphs(driver2stat)),
        elem.header,
        html.Hr(),
        dbc.Row(dbc.Col(elem.driver_buttons)),
        html.H2(children='', id="button_selection"),
        html.Hr(),
        html.Div(id="tab-content", className="p-4"),
    ],
    fluid=True
)


@app.callback(
    Output(component_id='tab-content', component_property='children'),
    [Input("button-" + driver, "n_clicks") for driver in conf.drivers] + [Input("store", "data")]
)
def update_graph_on_driver_selection(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = "HAM"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == 'store':
        button_id = 'HAM'

    return dbc.Row(
        dbc.Col(
            dcc.Graph(
                figure=args[-1][button_id.replace('button-', '')],
                style={'width': '190vh', 'height': '70vh'},
            )))


if __name__ == "__main__":
    import os
    #debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
    debug = True
    app.run_server(host="0.0.0.0", debug=debug, port=8050)
