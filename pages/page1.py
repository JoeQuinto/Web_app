from dash import dcc, html, Input, Output, callback
from Datasets.datasets import datasets

def generate_table(df, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ])


layout = html.Div([
    html.H3('Sample datasets'),
    html.P("Select a sample dataset"),
    dcc.Dropdown(
            ['Country values dataset', 'Iris dataset'],
            id='page-1-dropdown', value='Country values dataset'
        ),
    
                

    html.Div(id='page-1-display-value'),
    html.Br(),
    html.Div([
        html.H4(id='name-dataset'),
        html.Br(),
        html.Div(id='selected-dataset')
    ])
    
])


@callback(
    Output('selected-dataset', 'children'),
    Output('name-dataset', 'children'),
    Input('page-1-dropdown', 'value'))
def display_value(value):
    if value == 'Country values dataset':
        df_gen = generate_table(datasets[0])
    if value == 'Iris dataset':
        df_gen = generate_table(datasets[1])
    else:
        df_gen = generate_table(datasets[0])
        
    return df_gen, value