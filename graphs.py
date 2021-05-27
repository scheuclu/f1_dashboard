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