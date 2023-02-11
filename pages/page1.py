from dash import dcc, html, Input, Output, callback, State, ctx, dash_table
from Datasets.datasets import datasets, dataset_dict, dataset_names




def generate_table(df, max_rows=10):
    return dash_table.DataTable(df.to_dict('records'),
        fixed_rows={'headers' : True},
        style_table={'height': '300px', 'overflowY': 'auto', 'overflowX': 'auto'},
        style_data= {'whitespace':'normal', 'height' : 'auto',
                    'border': '1px solid black'},
        style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0,
                    'textAlign' : 'left'
                    },
        style_header={'backgroundColor': 'rgb(10, 30, 40)'},
        

        tooltip_data= [{
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
        ], tooltip_duration=None
        )

   

layout = html.Div([
    html.H3('Sample datasets'),
    html.P("Select a sample dataset"),
    dcc.Dropdown(
            dataset_names,
            id='page-1-dropdown', value='Country_indicators'
        ),
    html.Div(id='page-1-display-value'),
    html.Br(),
    html.Div([
        html.H4(id='name-dataset'),
        html.Br(),
        html.Div(id='selected-dataset')
    ]),
    html.Br(),
    html.Div([
        html.Div([
            html.Button('Estimate NaNs', id='est_nan', n_clicks=0),
            html.Br(),
            html.Button('Delete NaNs', id='del_nan', n_clicks=0),
            
        ],style={ 'padding-right' :20}),
        html.Div([
                        
            html.P(children= 'Estimate number of NaNs', id= 'Number_nans'),
                        
        ])
    ],style={ 'padding-left' :10 ,'display':'flex', 'flex-direction': 'row'}),

    html.Div([

        html.Button('Dataset Information', id='info-button', n_clicks=0),
        html.Button('Dataset Statistics', id='stats-button', n_clicks=0),
        html.Br(),
        html.P("Dataset Information"),
        html.Br(),
        html.Div(id='dataset-info'),


    ])
    
])


@callback(
    Output('selected-dataset', 'children'),
    Output('name-dataset', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    df_gen = generate_table(dataset_dict[str(value)])
       
        
    return df_gen, value




@callback(
    Output('Number_nans', 'children'),
    Input('est_nan', 'n_clicks'),
    Input('page-1-dropdown', 'value')
    )
def nans(n_clicks, name):

    if ctx.triggered_id != "est_nan":
        return
    df = dataset_dict[str(name)]

    n_nans =''

    a = df.isna().sum()
    for na in a: 
        if na > 0:
            n_nans+= n_nans
            n_nans = f"There are {na} NaNs in column: {a[a == na].index[0]} \n "

    if n_nans == '':
        n_nans = 'There are no NaNs'

    return n_nans

"""
@callback(
    Output('dataset-info', 'children'),
    Input('info-button', 'n_clicks'),
    Input('stats-button', 'n_clicks'),
    Input('page-1-dropdown', 'value')
    )
def info (click_info, click_stats, name):

    result = 'Select what kind of info about the dataset you want to see'

    if "info-button" == ctx.triggered_id:

        df = dataset_dict[str(name)]
        result = generate_table(df.info())
        

    elif "info-button" == ctx.triggered_id:

        df = dataset_dict[str(name)]
        result = generate_table(df.describe())

    return result 
"""