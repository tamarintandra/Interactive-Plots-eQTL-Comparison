import pandas as pd
import plotly.graph_objects as go
from math import floor, ceil

DATA = pd.read_csv('table5a.tsv', delimiter='\t')[['Symbol', 'rsID', 'Lineage', 'Condition', 'beta']]

# Get all the different conditions
CONDITION = set(DATA['Condition'])
# Get all the different cell types
CELL_TYPES = set(DATA['Lineage'])

def condition_plotter(condition, cell_type_1, cell_type_2):
    if cell_type_1 == cell_type_2:
        return go.Figure()
    subset_df = DATA.loc[(DATA['Condition'] == condition) & (DATA['Lineage'].isin([cell_type_1, cell_type_2]))]
    wide_df = (subset_df[['Symbol', 'rsID', 'Lineage', 'beta']]
               .pivot(index=['Symbol', 'rsID'], columns='Lineage', values='beta')
               .dropna()
               .reset_index())
    # Find the min and max for each axis
    min_axis = min([
        min(wide_df[cell_type_1]),
        min(wide_df[cell_type_2])
    ])
    min_axis = floor(min_axis/5)*5

    max_axis = max([
        max(wide_df[cell_type_1]),
        max(wide_df[cell_type_2])
    ])
    max_axis = ceil(max_axis/5)*5
    # Create plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=wide_df[cell_type_1],
            y=wide_df[cell_type_2],
            customdata=wide_df['Symbol'],
            text=wide_df['rsID'],
            mode="markers",
            marker=dict(size=10, opacity=0.7),
            hovertemplate="Gene: %{customdata}<br>"
                          "rsID: %{text}<br>"
                          "Y-axis Beta Value: %{y}<br>"
                          "X-axis Beta Value: %{x}<br>"
                          "<extra></extra>"
        )
    )
    fig.add_shape(
    type="line",
    # starting coordinates
    x0=min_axis, y0=min_axis,
    # ending coordinates
    x1=max_axis, y1=max_axis,
    # Make sure the points are on top of the line
    layer="below",
    # Style it like the axis lines
    line=dict(dash="dashdot", color="#C0C0C0", width=1)
    )
    fig.add_hline(y=0, line=dict(color="#C0C0C0", dash="dashdot", width=1))
    fig.add_vline(x=0, line=dict(color="#C0C0C0", dash="dashdot", width=1))
    fig.add_shape(
        type="rect",
        x0=min_axis,
        x1=0,
        y0=0,
        y1=max_axis,
        fillcolor="Gray",
        line_color="Crimson",
        opacity=0.1
    )
    fig.add_shape(
        type="rect",
        x0=0,
        x1=max_axis,
        y0=0,
        y1=max_axis,
        fillcolor="LightGreen",
        line_color="Crimson",
        opacity=0.1
    )
    fig.add_shape(
        type="rect",
        x0=0,
        x1=max_axis,
        y0=min_axis,
        y1=0,
        fillcolor="LightBlue",
        line_color="Crimson",
        opacity=0.1
    ),
    fig.add_shape(
        type="rect",
        x0=min_axis,
        x1=0,
        y0=min_axis,
        y1=0,
        fillcolor="rosybrown",
        line_color="Crimson",
        opacity=0.1
    )
    fig.update_layout(
    xaxis=dict(
        range=[min_axis, max_axis],
        title="%s Beta Value" % cell_type_1,
        # Hide the grid
        showgrid=False,
    ),
    yaxis=dict(
        range=[min_axis, max_axis],
        title="%s Beta Value" % cell_type_2,
        # Hide the grid
        showgrid=False,
    ),
    # Background color
    plot_bgcolor="white",
    height=800,
    title='{} - {} vs {}'.format(condition, cell_type_1, cell_type_2)
    )
    return fig
