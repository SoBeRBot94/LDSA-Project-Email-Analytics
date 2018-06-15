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

layout = go.Layout(
        title='Number of Enron Email Transacions Grouped Yearwise',
        font=dict(color = "black", size = 16),
        )

fig= go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename='emailTransactionsPlot')
