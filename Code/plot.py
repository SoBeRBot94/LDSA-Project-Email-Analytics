#!/usr/bin/env python3

import plotly as py
import plotly.graph_objs as go

Xvals=[]; Yvals=[]
f = open('./Counts.txt', 'r')

for line in f:
    a, b = line.split('\t', 1)
    Yvals.append(int(a))
    Xvals.append(b)

data = [go.Bar(
            x=Xvals,
            y=Yvals,
            text=Yvals,
            textposition = 'outside',
            opacity=0.8,
            marker=dict(
                color='rgb(124,238,102)',
                )
    )]

layout_a = go.Layout(
        xaxis = dict(range=[1975,1980]),
        yaxis = dict(range=[0, 500]),
        title='Number of Enron Email Transacions Grouped Yearwise',
        font=dict(color = "black", size = 16),
        )

fig_a = go.Figure(data=data, layout=layout_a)
py.offline.plot(fig_a, filename='emailTransactionsPlot_beforeThe90s')

layout_b = go.Layout(
        xaxis = dict(range=[1995,2005]),
        title='Number of Enron Email Transacions Grouped Yearwise',
        font=dict(color = "black", size = 16),
        )

fig_b = go.Figure(data=data, layout=layout_b)
py.offline.plot(fig_b, filename='emailTransactionsPlot_betweenThe1995_2005')
