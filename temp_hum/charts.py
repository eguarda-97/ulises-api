import plotly.graph_objects as go

import traceback

def scatter_plot(data, timestamps, color, legend, xaxis, yaxis) -> go.Figure:
    try:
        fig_list = []
        if len(data) != len(color) or len(data) != len(legend):
            raise Exception("List lengths must match")
        components = []

        # X-axis logic
        if "Date" in xaxis:
            components.append("<b>Date:</b> %{x|%d-%m-%Y}")
        else:
            components.append("<b>Hour:</b> %{x|%H:%M}")

        # Y-axis logic
        if "Temperature" in yaxis:
            components.append("<b>T:</b> %{y:.1f}°C")
        else:
            components.append("<b>H:</b> %{y:.1f}"+"%")

        # Join with line breaks and add the extra tag
        hovertemplate = "<br>".join(components) + "<extra></extra>"
        
        for i in range(len(data)):
            fig_data = go.Scatter(
                x=timestamps,
                y=data[i],
                mode="lines+markers",
                name=legend[i],
                line=dict(color=color[i]),
                marker=dict(color=color[i]),
                hovertemplate = hovertemplate
            )
            fig_list.append(fig_data)

        fig_layout = go.Layout(xaxis_title=xaxis, yaxis_title=yaxis, yaxis_range=[-5, 35] if "Temperature" in yaxis else [0,105])
        fig = go.Figure(data=fig_list, layout=fig_layout)

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=260,
            margin=dict(t=10, r=10, b=40, l=44),
        )

        return fig

    except:
        print(traceback.format_exc())
        return go.Figure()

def temperature_24h_chart(data: list, timestamps: list)->str:
    fig = scatter_plot(data, timestamps, color=["#ff0000"], legend=["Temperature"], xaxis="Hour", yaxis="Temperature [°C]", )
    return fig.to_json()

def temperature_weekly_chart(data: list, timestamps: list)->str:
    fig = scatter_plot(data, timestamps, color=["#ff0000", "#0000ff"], legend=["Max", "Min"], xaxis="Date", yaxis="Temperature [°C]")
    return fig.to_json()

def humidity_24h_chart(data: list, timestamps: list)->str:
    fig = scatter_plot(data, timestamps, color=["#ff0000"], legend=["Humidity"], xaxis="Hour", yaxis="Humidity [%]")
    return fig.to_json()

def humidity_weekly_chart(data: list, timestamps: list)->str:
    fig = scatter_plot(data, timestamps, color=["#ff0000", "#0000ff"], legend=["Max", "Min"], xaxis="Date", yaxis="Humidity [%]")
    return fig.to_json()
