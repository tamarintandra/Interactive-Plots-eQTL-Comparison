from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from utils_mod_table5 import cell_types, condition_combination, create_scatter, cell_type_dfs
from utils_table5a import CONDITION, CELL_TYPES, condition_plotter

"""
Constants and Parameters

Description
"""
app = Dash(__name__)
app.config.external_stylesheets = [dbc.themes.BOOTSTRAP]
APP_TITLE = "Comparison between different Condition Types across rsID and Genes"

"""
Page Layout and Contents

Description
"""
NAVBAR = dbc.Navbar(
    children=[
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavbarBrand(
                        APP_TITLE, className="ms-2",
                        style = {"font-weight": "bold"}
                    )
                ),
            ],
            align="center",
            className="g-0",
            style={"margin-left": "1rem"}
        ),
    ],
    color="#F2F2F2",
    dark=False,
    sticky="top",
)

COL_1 = html.Div(
        children=[
            html.Div(children=[
                html.Div('Cell Type'),
                dcc.Dropdown(
                    id='cell_types_col1',
                    options=[
                        {'label': cell, 'value': cell} for cell in cell_types
                    ],
                    value=list(cell_types)[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='50%')),
            html.Div(children=[
                html.Div('Condition'),
                dcc.Dropdown(
                    id='condition_comparison1',
                    options=[
                        {'label': pair, 'value': pair}
                         for pair in condition_combination
                    ],
                    value=list(condition_combination.keys())[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='50%'))
        ], style=dict(display='flex'))

CONTENT_1 = html.Div(children=[dcc.Graph(id='graph1')])

COLUMN_1 = dbc.Col(
                    [COL_1, CONTENT_1]
                )

COL_2 = html.Div(
        children=[
            html.Div(children=[
                html.Div('Cell Type'),
                dcc.Dropdown(
                    id='cell_types_col2',
                    options=[
                        {'label': cell, 'value': cell} for cell in cell_types
                    ],
                    value=list(cell_types)[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='50%')),
            html.Div(children=[
                html.Div('Condition'),
                dcc.Dropdown(
                    id='condition_comparison2',
                    options=[
                        {'label': pair, 'value': pair}
                         for pair in condition_combination
                    ],
                    value=list(condition_combination.keys())[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='50%'))
        ], style=dict(display='flex'))

CONTENT_2 = html.Div(children=[dcc.Graph(id='graph2')])

COLUMN_2 = dbc.Col(
                    [COL_2, CONTENT_2]
                )

CONTENT_A = html.Div(
    [
        dbc.Row(
            [
                COLUMN_1,
                COLUMN_2,
            ],
        align="center",),
    ]
)

CONTENT_B = html.Div(
    children=[
        html.Div(children=[
                html.Div('Condition'),
                dcc.Dropdown(
                    id='condition',
                    options=[
                        {'label': cond, 'value': cond} for cond in CONDITION
                    ],
                    value=list(CONDITION)[0],
                    clearable=False,
                    searchable=False,
                )]),
        html.Div(
            children=[
            html.Div(children=[
                html.Div('Cell Type 1'),
                dcc.Dropdown(
                    id='cell_type_1',
                    options=[
                        {'label': ct, 'value': ct} for ct in CELL_TYPES
                    ],
                    value=list(CELL_TYPES)[0],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='50%')),
            html.Div(children=[
                html.Div('Cell Type 2'),
                dcc.Dropdown(
                    id='cell_type_2',
                    options=[
                        {'label': ct, 'value': ct} for ct in CELL_TYPES
                    ],
                    value=list(CELL_TYPES)[1],
                    clearable=False,
                    searchable=False,
                )], style=dict(width='50%'))
        ], style=dict(display='flex')
        )
    ]
)

TABS = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(CONTENT_A, 
                        label="Condition", tab_style={"marginLeft": "auto"}),
                dbc.Tab([
                    CONTENT_B,
                    dcc.Graph(id='graph_tab_2')
                ], label="Cell Type"),
            ]
        ),
    ]
)

APP_CONTAINER = html.Div(
    id="page-content", children=[TABS],
    style={"position": "fixed", 
           "top": 85, 
           "left": 30, 
           "bottom": 0,
           "right": 30}
)

app.layout = html.Div(children=[NAVBAR,
                                dcc.Interval(id="interval-component",
                                             interval=2*1000,
                                             n_intervals=50, disabled=True),
                                APP_CONTAINER])

@callback(
    Output('graph1', 'figure'),
    Input('cell_types_col1', 'value'),
    Input('condition_comparison1', 'value')
)
def update_graph1(cell_type, condition_vs):
    return create_scatter(cell_type_dfs[cell_type], cell_type, condition_vs)

@callback(
    Output('graph2', 'figure'),
    Input('cell_types_col2', 'value'),
    Input('condition_comparison2', 'value')
)
def update_graph2(cell_type, condition_vs):
    return create_scatter(cell_type_dfs[cell_type], cell_type, condition_vs)

@callback(
    Output('graph_tab_2', 'figure'),
    Input('condition', 'value'),
    Input('cell_type_1', 'value'),
    Input('cell_type_2', 'value')
)
def update_graph_tab2(condition, cell_type_1, cell_type_2):
    return condition_plotter(condition, cell_type_1, cell_type_2)

if __name__ == '__main__':
    app.run(debug=False)
