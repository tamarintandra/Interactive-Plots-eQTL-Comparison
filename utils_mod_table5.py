import pandas as pd
import plotly.graph_objects as go
from math import ceil, floor

# Read the data into a pandas DataFrame
data = pd.read_csv('mod_table5.txt', delimiter='\t', header=0)

# Sort the DataFrame based on cell types, rsID, and gene names
sorted_data = data.sort_values(by=['CellType', 'rsID', 'Symbol'])

# Group the data by 'rsID' and filter for groups with three unique conditions
filtered_data = sorted_data.groupby(['Symbol', 'rsID', 'CellType'])['Condition'].transform('nunique') == 3

# Use the filtered mask to select rows
selected_rows = sorted_data[filtered_data]

# Create one DataFrame for each cell type
cell_types = set(selected_rows['CellType'])
cell_type_dfs = {cell_type: selected_rows.loc[selected_rows['CellType'] == cell_type]
                 for cell_type in cell_types}

condition_combination = {'NS vs COV': ('NS', 'COV'),
                         'COV vs IAV': ('COV', 'IAV'),
                         'NS vs IAV': ('NS', 'IAV')}

def create_scatter(df, cell_type, combination):
    condition1, condition2 = condition_combination[combination]
    wide_df = (df[['Symbol', 'rsID', 'Condition', 'beta']]
               .drop_duplicates()
               .pivot(index=['Symbol', 'rsID'], columns='Condition', values='beta')
               .reset_index())
    # Find the min and max for each axis
    min_axis = min([
        min(wide_df[condition1]),
        min(wide_df[condition2])
    ])
    min_axis = floor(min_axis/5)*5

    max_axis = max([
        max(wide_df[condition1]),
        max(wide_df[condition2])
    ])
    max_axis = ceil(max_axis/5)*5
    # Create plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=wide_df[condition1],
            y=wide_df[condition2],
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
        title="%s Beta Value" % condition1,
        # Hide the grid
        showgrid=False,
    ),
    yaxis=dict(
        range=[min_axis, max_axis],
        title="%s Beta Value" % condition2,
        # Hide the grid
        showgrid=False,
    ),
    # Background color
    plot_bgcolor="white",
    height=800,
    title='{} - {} eQTL vs {} eQTL'.format(cell_type, condition1, condition2)
    )
    return fig
