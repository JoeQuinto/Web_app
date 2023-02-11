#back up
from dash import dcc, html, Input, Output, callback, State, ctx, dash_table
from Datasets.datasets import datasets, dataset_dict

PAGE_SIZE = 5
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


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
        page_current=0, 
        page_size= PAGE_SIZE,
        page_action='custom',

        filter_action='custom',
        filter_query='',
        sort_action='custom',
        sort_mode='multi',
        sort_by=[],


        tooltip_data= [{
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df.to_dict('records')
        ], tooltip_duration=None
        )


    
def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') +1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0= value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                return name, operator_type[0].strip(), value
    return [None] * 3

layout = html.Div([
    html.H3('Sample datasets'),
    html.P("Select a sample dataset"),
    dcc.Dropdown(
            ['Country values dataset', 'Iris dataset', 'GDP dataset'],
            id='page-1-dropdown', value='Country values dataset'
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

"""

@callback(
    Output('selected-dataset', 'children'),
    Output('name-dataset', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    if value == 'Country values dataset':
        df_gen = generate_table(datasets[0])
        
    if value == 'Iris dataset':
        df_gen = generate_table(datasets[1])
    if value == 'GDP dataset':
        df_gen = generate_table(datasets[2])
        
    else:
        df_gen = generate_table(datasets[0])
    
    
        
    return df_gen, value

"""

@callback(
    Output('selected-dataset', 'children'),
    Input('page-1-dropdown', 'value'),
    Input('selected_dataset', "page_current"),
    Input('selected_dataset', "page_size"),
    Input('selected_dataset', 'sort_by'),
    Input('selected_dataset', 'filter_query')
)
def update_table(name, page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = dataset_dict[str(name)]
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]
    
    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace = False
        )

    page = page_current
    size = page_size
    return generate_table(dff.iloc[page * size: (page+1) * size])






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


@callback(
    Output('dataset-info', 'children'),
    Input('info-button', 'n_clicks'),
    Input('stats-button', 'n_clicks'),
    Input('page-1-dropdown', 'value')
    )
def info(click_info, click_stats, name):

    result = 'Select what kind of info about the dataset you want to see'

    if ctx.triggered_id == "info-button":

        df = dataset_dict[str(name)]
        result = generate_table(df.info())


    return result