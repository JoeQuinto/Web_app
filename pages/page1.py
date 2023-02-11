from dash import dcc, html, Input, Output, callback, State, ctx, dash_table
from Datasets.datasets import dataset_dict
from dash.exceptions import PreventUpdate
import pandas as pd


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
    dcc.Store(id='memory-dict'),
    dcc.Store(id='current-dict'),
    html.H3('Sample datasets'),
    html.P("Select a sample dataset"),
    dcc.Dropdown(
            options= list(dataset_dict.keys()),
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
            html.Button('Delete NaNs', id='del-nan', n_clicks=0)
        ],style={ 'padding-right' :20}),
        html.Div([
                        
            html.P(children= 'Estimate number of NaNs', id= 'Number_nans'),
                        
        ]),
        
    ],style={ 'padding-left' :10 ,'display':'flex', 'flex-direction': 'row'}),
    
    html.Div([
            
        html.H3('Modified datasets'),
        dcc.Dropdown(
                options= [],
                id='mod-dropdown'
            )
        ]),
    html.Div([
        html.H4(id='name-mod-dataset'),
        html.Br(),
        html.Div(id='selected-mod-dataset')
    ]),
    html.Div([

        html.Button('Dataset Information', id='info-button', n_clicks=0),
        html.Button('Dataset Statistics', id='stats-button', n_clicks=0),
        html.Br(),
        html.P("Dataset Information"),
        html.Br(),
        html.Div(id='dataset-info')
    ])    
])



@callback(
    Output('selected-dataset', 'children'),
    Output('name-dataset', 'children'), 
    Output('current-dict', 'children'),   
    State('memory-dict', 'children'),
    Input('page-1-dropdown', 'value'),
    
)
def display_value(memory_dict,name):    
       
    
    if memory_dict: 
        for key, value in memory_dict.items():
            if type(value) != dict:
                memory_dict[key] = pd.DataFrame.from_dict(value)
        
                
        if len(memory_dict.keys()) > len(dataset_dict.keys()):
            df_gen = generate_table(memory_dict[str(name)])
        current_dict = memory_dict.copy()
    else: 
        df_gen = generate_table(dataset_dict[str(name)])
        current_dict = dataset_dict.copy()

    for key, value in current_dict.items():
        if type(value) != dict:
            current_dict[key] = value.to_dict('records') 
    
    return df_gen, name, current_dict

@callback(
    Output('mod-dropdown', 'options'),
    Output('page-1-dropdown', 'options'),
    Output('memory-dict', 'children'),
    Input('del-nan', 'n_clicks'),
    Input('page-1-dropdown', 'value')
)
def upd_dd(n_clicks, name):
    
    mod_dict = {}
    if 'del-nan' != ctx.triggered_id:
        raise PreventUpdate
        
    else:        
        mod_dict = dataset_dict.copy()
        df_nan = mod_dict[str(name)].dropna()  
        new_name = str(name) +'_noNaNs'
        mod_dict[new_name]  = df_nan
        
    for key, value in mod_dict.items():
        if type(value) != dict:
            mod_dict[key] = value.to_dict('records') 
           
    return list(mod_dict.keys()),list(mod_dict.keys()),  mod_dict


@callback(
    Output('Number_nans', 'children'),
    Input('est_nan', 'n_clicks'),
    State('page-1-dropdown', 'value'),
    State('current-dict', 'children')
    ) 
def nans (n_clicks, name, current_dict):

    if current_dict:
        for key, value in current_dict.items():
                if type(value) != dict:
                    current_dict[key] = pd.DataFrame.from_dict(value)

    if "est_nan" == ctx.triggered_id:
        df = current_dict[str(name)]
        
        n_nans =''            
        a = df.isna().sum()
        for na in a: 
            if na > 0:
                n_nans+= n_nans
                n_nans = f"There are {na} NaNs in column: {a[a == na].index[0]} \n "            
        if n_nans == '':
            n_nans = 'There are no NaNs'        
        return n_nans

        
@callback(
    Output('dataset-info', 'children'),
    Input('stats-button', 'n_clicks'),
    Input('page-1-dropdown', 'value')
    )
def info (click_stats, name):

    result = 'Select what kind of info about the dataset you want to see'
       

    if "stats-button" == ctx.triggered_id:

        df = dataset_dict[str(name)]
        result = generate_table(df.describe())
        

    return result