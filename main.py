"""
TODO
"""
import base64
import hashlib

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

import config as conf
import pages
import scoring
import storage

races2data = storage.load_races2data()

# # Read data
# cache = './races2data.pickle'
# if os.path.isfile(cache):
#     print("Loading from cache ...")
#     races2data = pickle.load(open(cache, "rb"))
#     for df in races2data.values():
#       df.loc['base points']=float('NaN')
#       df.loc['Lukas points']=float('NaN')
#       df.loc['Patrick points']=float('NaN')
#       df.loc['Lisa points']=float('NaN')
#       df.loc['Lukas multiplicator']=float('NaN')
#       df.loc['Patrick multiplicator']=float('NaN')
#       df.loc['Lisa multiplicator']=float('NaN')
#
#     print("... Done")
# else:
#     print("Reading data ...")
#     races2data = {race: pd.read_excel(conf.path, sheet_name=race, usecols="A:U", index_col=0, header=19).iloc[0:5] for
#                   race
#                   in conf.races}
#     for df in races2data.values():
#       df.loc['base points']=float('NaN')
#       df.loc['Lukas points']=float('NaN')
#       df.loc['Patrick points']=float('NaN')
#       df.loc['Lisa points']=float('NaN')
#       df.loc['Lukas multiplicator']=float('NaN')
#       df.loc['Patrick multiplicator']=float('NaN')
#       df.loc['Lisa multiplicator']=float('NaN')
#     with open(cache, 'wb') as f:
#         pickle.dump(races2data, f)
#     print("Done ...")

driver2image = {driver: base64.b64encode(open(f'./img/{driver}.png', 'rb').read()) for driver in conf.drivers}

# Compute driver statistics
driver2stat = {driver: pd.DataFrame(index=races2data["Imola"].index, columns=conf.races) for driver in conf.drivers}
for driver in conf.drivers:
    for race in conf.races:
        driver2stat[driver][race] = races2data[race][driver]

scoring.compute_scores2(races2data)
###scoring.compute_scores(driver2stat)#TODO(scheuclu) redoc this function

# with blob.open('wb') as f:
#     pickle.dump(races2data, f)
# print("Writen scored data to file")

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 20,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    # "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Img(src='https://i.ibb.co/KKq7R1L/F1-2.png',
                 style={"width": "16rem"}),
        html.H3(" ", className="display-4"),
        html.Hr(),
        html.P(
            "There's a number of visualizations availiable", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Per race points", href="/page-1", active="exact"),
                dbc.NavLink("Overview", href="/page-2", active="exact"),
                dbc.NavLink("Scoring", href="/page-scoring", active="exact"),
                dbc.NavLink("Data (debug)", href="/page-data", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = dcc.Loading(html.Div(
    id="page-content",
    children=pages.get_per_race_points(driver2stat),
    style=CONTENT_STYLE))

# App layout
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
app.layout = html.Div([
    html.Div([dcc.Location(id="url"), sidebar, content,
              html.Footer(
                  children=[
                      html.Hr(),
                      dcc.Markdown("""
                      ###### Code at: [github.com/scheuclu/f1_dashboard](https://www.github.com/scheuclu/f1_dashboard)
                      ###### created by: [scheuclu@gmail.com](mailto:scheuclu@gmail.com)
                      """)
                  ], style={'position': 'fixed', 'width': '100%', 'textAlign': 'center'}
              )])
])


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
                # style={'width': '190vh', 'height': '70vh'},
            )))


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return pages.get_home(races2data)
    elif pathname == "/page-1":
        return pages.get_per_race_points(driver2stat)
    elif pathname == "/page-2":
        return pages.get_overview(races2data)
    elif pathname == "/page-scoring":
        return pages.get_scoring()
    elif pathname == "/page-data":
        return pages.get_data(races2data)

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# @app.callback(Output("table_data", "data"), [Input("data_race_selector", "value")], State("data_race_selector", "value"))
# def update_race_data(race_name, state):
#     print(f"Selected {race_name}")
#     print(f'state:{state}')
#     if race_name==None:
#         return state
#     df = races2data[race_name].copy()
#     df = df.reset_index()
#     return df.to_dict('records')


@app.callback(
    [Output('table_data', 'data'), Output('dialog_success', 'displayed'), Output('dialog_failure', 'displayed')],
    Input('recompute_button', 'n_clicks'),
    Input("data_race_selector", "value"),
    # State('data_race_selector', 'value'),
    State('pw_input', 'value'),
    State('table_data', 'data')
)
def display_output(nclicks, racename, access_code, data):
    print(nclicks, racename)

    # First, we need to figure out which input was triggered
    ctx = dash.callback_context
    if not ctx.triggered:
        return data, False, False

    inp_name = ctx.triggered[0]['prop_id'].split('.')[0]

    # The race selector changed
    if inp_name == 'data_race_selector':
        print(f"Selected {racename}")
        if racename == None:
            return data
        df = races2data[racename].copy()
        df = df.reset_index()
        return df.to_dict('records'), False, False
    else:
        print(access_code)
        print(hash(access_code))
        if access_code is not None and hashlib.md5(
                access_code.encode()).hexdigest() == 'a12dee9a4f0cd316e4fedd0788889acd':

            df = races2data[racename]
            # Only allow updating race_result for now
            for row in data:
                # print(row['index'])
                if row['index'] == 'race result':
                    print(row)
                    for driver in conf.drivers:
                        # df[driver]['race result'] = int(row[driver]) if row[driver].isdigit() else row[driver]
                        df[driver]['race result'] = row[driver]
                    df.replace(to_replace=[None], value=float('NaN'), inplace=True)
            # Now redo the computation. This should later only be done for the relevant race
            ###print(df.loc['race result'])
            scoring.score_race(df)  # TODO(scheuclu) This need to be done on df level.
            storage.save_races2data(races2data)
            ndf = df.copy()
            ndf = ndf.reset_index()
            return ndf.to_dict('records'), True, False
        else:
            df = races2data[racename]
            ndf = df.copy()
            ndf = ndf.reset_index()
            return ndf.to_dict('records'), False, True


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False, port=8080)
    # if 'DASH_DEBUG' in os.environ:
    #     app.run_server(host="0.0.0.0", debug=True, port=8050)
    # else:
    #     app.run_server(debug=False, port=8050)
    # debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
