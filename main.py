"""
TODO
"""
import base64
import os
import pickle

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

import config as conf
import pages
import scoring

# Read data
cache = './races2data.pickle'
if os.path.isfile(cache):
    print("Loading from cache ...")
    races2data = pickle.load(open(cache, "rb"))
    print("... Done")
else:
    print("Reading data ...")
    races2data = {race: pd.read_excel(conf.path, sheet_name=race, usecols="A:U", index_col=0, header=19).iloc[0:12] for
                  race
                  in conf.races}
    with open(cache, 'wb') as f:
        pickle.dump(races2data, f)
    print("Done ...")

driver2image = {driver: base64.b64encode(open(f'./img/{driver}.png', 'rb').read()) for driver in conf.drivers}

# Compute driver statistics
driver2stat = {driver: pd.DataFrame(index=races2data["Imola"].index, columns=conf.races) for driver in conf.drivers}
for driver in conf.drivers:
    for race in conf.races:
        driver2stat[driver][race] = races2data[race][driver]

scoring.compute_scores(driver2stat)

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
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
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
        return pages.get_home(driver2stat)
    elif pathname == "/page-1":
        return pages.get_per_race_points(driver2stat)
    elif pathname == "/page-2":
        return pages.get_overview(driver2stat)
    elif pathname == "/page-scoring":
        return pages.get_scoring()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    import os

    app.run_server(host="0.0.0.0", debug=False, port=8080)
    # if 'DASH_DEBUG' in os.environ:
    #     app.run_server(host="0.0.0.0", debug=True, port=8050)
    # else:
    #     app.run_server(debug=False, port=8050)
    # debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
