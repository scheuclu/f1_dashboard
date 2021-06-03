import plotly.graph_objects as go

import config as conf


def get_driverstat_graph(stat):
    trace0 = go.Scatter(x=stat.columns, y=stat.loc['race result'], name='race result',
                        line=dict(color='white'),
                        )
    trace1 = go.Scatter(x=stat.columns, y=stat.loc['Patrick tip'], name='Patrick tip',
                        mode='markers',
                        marker=dict(size=20),
                        text=stat.loc['Patrick points'],
                        textposition='top center'
                        )

    trace2 = go.Scatter(x=stat.columns, y=stat.loc['Lukas tip'], name='Lukas tip',
                        mode='markers',
                        marker=dict(size=20),
                        text=stat.loc['Lukas points'],
                        textposition='bottom center'
                        )

    trace3 = go.Scatter(x=stat.columns, y=stat.loc['champoinship standing'],
                        name='champoinship standing', opacity=0.5,
                        line=dict(dash='dash'))

    trace_best = go.Scatter(x=stat.columns, y=[1 for i in stat.columns],
                            showlegend=False, opacity=0.0)

    trace_DNF = go.Scatter(x=stat.columns, y=[20 for i in stat.columns],
                           showlegend=False, opacity=0.0)

    traces = [trace3, trace0, trace1, trace2, trace_best, trace_DNF]

    layout = go.Layout(
        autosize=True,
        showlegend=True,
        legend=dict(
            yanchor='bottom',
            xanchor='left',
            x=0.05,
            y=1.05,
            orientation='h'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark",
        yaxis=dict(dtick=1, title='position')
    )

    fig = go.Figure(data=traces, layout=layout)
    return fig


def get_cumpoints_graph(cumpoints):
    traces = []
    import plotly.graph_objects as go
    for driver in conf.drivers:
        x = []
        y = []
        for race in conf.races:
            x.append(race)
            y.append(cumpoints[driver][race])
        t = go.Scatter(x=x, y=y, name=driver, stackgroup='one')
        traces.append(t)

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark",
        legend=dict(
            yanchor='bottom',
            xanchor='left',
            x=0.05,
            y=1.05,
            orientation='h'
        )
    )
    fig = go.Figure(data=traces, layout=layout)
    return fig


def get_overview(lukas_points, patrick_points, num_finished, num_remaining):
    colors = ['#FF1801', '#b38537']

    standings = go.Pie(
        values=[patrick_points, lukas_points],
        text=['Patrick', 'Lukas'],
        textinfo='text+value',
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2))
    )
    layout = go.Layout(
        title={
            'text': "Standings",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        autosize=True,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark"
    )
    fig_standings = go.Figure(data=standings, layout=layout)

    trace_races = go.Pie(
        values=[num_finished, num_remaining],
        text=['Finished races', 'Remaining races'],
        textinfo='text+value',
        marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2))
    )
    layout = go.Layout(
        title={
            'text': "Season progress",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        autosize=True,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark"
    )
    fig_races = go.Figure(data=trace_races, layout=layout)
    return fig_standings, fig_races


import scoring


def score2z(score):
    return score if score != 0 else None


def z2text(z):
    return str(int(z)) if z is not None else ''


def get_scoring():
    positions = list(range(1, 21))

    buttons = []
    for championship_position in range(1, 21):

        z = [[score2z(scoring.points(championship_position, race_result, race_guess)) for race_guess in positions] for
             race_result in positions]
        text = [[z2text(zz) for zz in row] for row in z]

        annotations = go.Annotations()
        for n, row in enumerate(z):
            for m, val in enumerate(row):
                annotations.append(go.layout.Annotation(text=text[n][m], x=m + 1, y=n + 1,
                                                        xref='x1', yref='y1', showarrow=False, font={'color': 'black'}))

        buttons.append(
            dict(
                label="Pos " + str(championship_position),
                method="update",
                args=[
                    {"z": [z]},
                    {"annotations": annotations}
                ]
            )
        )

    fig = go.Figure(go.Heatmap(z=z, x=positions, y=positions, colorscale='OrRd', xgap=2, ygap=2,
                               showscale=False))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template="plotly_dark",
        xaxis=dict(title='race guess', showgrid=False, dtick=1),
        yaxis=dict(title='race result', showgrid=False, dtick=1),
        annotations=annotations,
        height=600,
        width=600,
        title='Select championship position:'
    )

    fig.update_layout(
        updatemenus=[
            dict(active=19, buttons=buttons,
                 direction="down",
                 pad={"r": 10, "t": 10},
                 showactive=True,
                 x=0.02,
                 xanchor="left",
                 y=1.0,
                 yanchor="top",
                 )])

    return fig
