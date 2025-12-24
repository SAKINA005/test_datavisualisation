from dash import html, Dash, dcc, dash_table, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from nav_bar import navbar

df = px.data.iris()

colors = {
    'setosa': '#FF6B6B',
    'versicolor': '#4ECDC4',
    'virginica': '#A78BFA'
}

liste_variable_numeric = list(df.columns)
liste_variable_numeric.remove('species')
liste_variable_numeric.remove('species_id')

# ========================== Styles personnalisés ====================================
CARD_STYLE = {
    'border-radius': '16px',
    'box-shadow': '0 8px 32px rgba(0, 0, 0, 0.08)',
    'border': 'none',
    'transition': 'all 0.3s ease'
}

HEADER_STYLE = {
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'color': 'white',
    'border-radius': '16px 16px 0 0',
    'padding': '20px',
    'font-weight': '600'
}

STAT_CARD_STYLE = {
    'border-radius': '12px',
    'padding': '15px',
    'margin': '8px 0',
    'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
    'transition': 'transform 0.2s ease',
}

# ========================== Graphiques améliorés ====================================
def create_scatter_plot(x, y, title):
    fig = px.scatter(df, x=x, y=y, color='species', 
                     color_discrete_map=colors,
                     title=title,
                     height=350)
    
    fig.update_layout(
        template='plotly_white',
        font=dict(family="Inter, sans-serif", size=12),
        title=dict(font=dict(size=16, color='#2D3748', weight=600), x=0.5, xanchor='center'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=40, l=40, r=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#E2E8F0',
            borderwidth=1
        )
    )
    
    fig.update_traces(marker=dict(size=10, line=dict(width=1.5, color='white')))
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='#E2E8F0')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='#E2E8F0')
    
    return fig

scatter_plot = create_scatter_plot('sepal_length', 'sepal_width', 'Longueur vs Largeur Sépale')
scatter_plot2 = create_scatter_plot('petal_length', 'petal_width', 'Longueur vs Largeur Pétale')

scatter_plot3 = px.scatter_3d(df, x='petal_length', y='petal_width', z='sepal_length', 
                              color='species', color_discrete_map=colors,
                              title='Vue 3D - Dimensions Florales',
                              height=350)
scatter_plot3.update_layout(
    template='plotly_white',
    font=dict(family="Inter, sans-serif", size=11),
    title=dict(font=dict(size=16, color='#2D3748', weight=600), x=0.5, xanchor='center'),
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=60, b=20, l=20, r=20),
    scene=dict(
        xaxis=dict(gridcolor='#E2E8F0', showbackground=True, backgroundcolor='rgba(240,240,240,0.3)'),
        yaxis=dict(gridcolor='#E2E8F0', showbackground=True, backgroundcolor='rgba(240,240,240,0.3)'),
        zaxis=dict(gridcolor='#E2E8F0', showbackground=True, backgroundcolor='rgba(240,240,240,0.3)')
    )
)
scatter_plot3.update_traces(marker=dict(size=6, line=dict(width=1, color='white')))

# ========================== Table stylisée ====================================
table = dash_table.DataTable(
    df.to_dict(orient='records'),
    page_size=12,
    style_table={'overflowX': 'auto'},
    style_header={
        'backgroundColor': '#667eea',
        'color': 'white',
        'fontWeight': '600',
        'textAlign': 'center',
        'padding': '12px',
        'font-family': 'Inter, sans-serif'
    },
    style_cell={
        'textAlign': 'center',
        'padding': '12px',
        'font-family': 'Inter, sans-serif',
        'fontSize': '13px'
    },
    style_data={
        'border': '1px solid #E2E8F0'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#F7FAFC'
        },
        {
            'if': {'row_index': 'even'},
            'backgroundColor': 'white'
        }
    ]
)

# ========================== App initialization ====================================
app = Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
])
server = app.server

# ========================== Layout principal ====================================
layout1 = html.Div([
    # Hero Section
    dbc.Container([
        html.Div([
            html.H1('🌸 Iris Dataset Explorer', 
                   className='text-center mb-2',
                   style={
                       'font-weight': '700',
                       'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                       '-webkit-background-clip': 'text',
                       '-webkit-text-fill-color': 'transparent',
                       'font-size': '2.8rem',
                       'margin-top': '30px'
                   }),
            html.P('Analyse interactive des espèces d\'iris avec visualisations avancées',
                  className='text-center text-muted mb-4',
                  style={'font-size': '1.1rem'})
        ]),
        
        # Statistics Cards Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Span('🌺', style={'font-size': '2rem', 'margin-right': '10px'}),
                            html.H5('Setosa', className='d-inline-block mb-0',
                                   style={'color': colors['setosa'], 'font-weight': '600'})
                        ], className='d-flex align-items-center mb-3'),
                        dcc.Dropdown(
                            options=[{'label': v.replace('_', ' ').title(), 'value': v} 
                                    for v in liste_variable_numeric],
                            value=liste_variable_numeric[0],
                            id='liste_pour_setosa',
                            style={'margin-bottom': '15px'},
                            className='shadow-sm'
                        ),
                        html.Div(id='stats_setosa')
                    ])
                ], style=CARD_STYLE)
            ], lg=4, md=12, className='mb-4'),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Span('🌼', style={'font-size': '2rem', 'margin-right': '10px'}),
                            html.H5('Versicolor', className='d-inline-block mb-0',
                                   style={'color': colors['versicolor'], 'font-weight': '600'})
                        ], className='d-flex align-items-center mb-3'),
                        dcc.Dropdown(
                            options=[{'label': v.replace('_', ' ').title(), 'value': v} 
                                    for v in liste_variable_numeric],
                            value=liste_variable_numeric[0],
                            id='liste_pour_versicolor',
                            style={'margin-bottom': '15px'},
                            className='shadow-sm'
                        ),
                        html.Div(id='stats_versicolor')
                    ])
                ], style=CARD_STYLE)
            ], lg=4, md=12, className='mb-4'),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Span('🌷', style={'font-size': '2rem', 'margin-right': '10px'}),
                            html.H5('Virginica', className='d-inline-block mb-0',
                                   style={'color': colors['virginica'], 'font-weight': '600'})
                        ], className='d-flex align-items-center mb-3'),
                        dcc.Dropdown(
                            options=[{'label': v.replace('_', ' ').title(), 'value': v} 
                                    for v in liste_variable_numeric],
                            value=liste_variable_numeric[0],
                            id='liste_pour_virginica',
                            style={'margin-bottom': '15px'},
                            className='shadow-sm'
                        ),
                        html.Div(id='stats_virginica')
                    ])
                ], style=CARD_STYLE)
            ], lg=4, md=12, className='mb-4'),
        ]),
        
        # Graphiques Section
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H4('📊 Visualisations Interactives', 
                           style={'font-weight': '600', 'color': '#2D3748', 'margin-bottom': '5px'}),
                    html.P('Explorez les relations entre les différentes dimensions', 
                          className='text-muted mb-3')
                ]),
                
                dbc.Row([
                    dbc.Col([
                        html.Label('Style des graphiques:', 
                                  style={'font-weight': '500', 'color': '#4A5568', 'margin-bottom': '8px'}),
                    ], width='auto'),
                    dbc.Col([
                        dbc.RadioItems(
                            options=[
                                {"label": "🎨 Plotly", "value": "plotly"},
                                {"label": "⚪ White", "value": "plotly_white"},
                                {"label": "⚫ Dark", "value": "plotly_dark"},
                                {"label": "📈 GGPlot2", "value": "ggplot2"},
                                {"label": "🌊 Seaborn", "value": "seaborn"},
                                {"label": "✨ Simple", "value": "simple_white"},
                            ],
                            id='style_graph',
                            inline=True,
                            value='plotly_white',
                            className='mb-3'
                        ),
                    ]),
                ], align='center', className='mb-4'),
                
                dbc.Row(id='graphs', className='g-4')
            ], className='p-4')
        ], style={**CARD_STYLE, 'margin-bottom': '30px'}),
        
        # Table Section
        dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.H4('📋 Données Complètes', 
                           style={'font-weight': '600', 'color': '#2D3748', 'margin-bottom': '5px'}),
                    html.P('Tableau complet des mesures du dataset Iris', 
                          className='text-muted mb-3')
                ]),
                table
            ], className='p-4')
        ], style=CARD_STYLE),
        
    ], fluid=True, style={'padding': '0 30px 50px 30px', 'background': '#F7FAFC', 'min-height': '100vh'})
], style={'background': '#F7FAFC'})

layout2 = html.Div([
    dbc.Container([
        html.H1('Page 2 - En construction', className='text-center mt-5')
    ])
])

app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='navbar_content'),
    html.Div(id='page_content')
])

# ========================== Callbacks ====================================
@app.callback(
    Output('navbar_content', 'children'),
    Output('page_content', 'children'),
    Input('url', 'pathname')
)
def switch_page(path):
    actual_navbar = navbar(lien=path)
    if path == '/':
        page_content = layout1
    elif path == '/fda':
        page_content = layout2
    else:
        page_content = html.H3('404 - Page non trouvée')
    
    return actual_navbar, page_content

@app.callback(
    Output('graphs', 'children'),
    Input('style_graph', 'value')
)
def update_graph_layout(stl):
    scatter_plot.update_layout(template=stl)
    scatter_plot2.update_layout(template=stl)
    scatter_plot3.update_layout(template=stl)
    
    return [
        dbc.Col(dcc.Graph(figure=scatter_plot, config={'displayModeBar': False}), 
                lg=4, md=12, className='mb-3 mb-lg-0'),
        dbc.Col(dcc.Graph(figure=scatter_plot2, config={'displayModeBar': False}), 
                lg=4, md=12, className='mb-3 mb-lg-0'),
        dbc.Col(dcc.Graph(figure=scatter_plot3, config={'displayModeBar': False}), 
                lg=4, md=12, className='mb-3 mb-lg-0'),
    ]

def create_stat_display(val, species_name, color):
    species_data = df.loc[df['species'] == species_name, val]
    moyenne = round(species_data.mean(), 2)
    variance = round(species_data.std(), 2)
    max_val = species_data.max()
    min_val = species_data.min()
    
    stats = [
        {'icon': '📊', 'label': 'Moyenne', 'value': moyenne},
        {'icon': '📈', 'label': 'Écart-type', 'value': variance},
        {'icon': '⬆️', 'label': 'Maximum', 'value': max_val},
        {'icon': '⬇️', 'label': 'Minimum', 'value': min_val},
    ]
    
    return [
        html.Div([
            html.Div([
                html.Span(stat['icon'], style={'font-size': '1.3rem', 'margin-right': '10px'}),
                html.Span(stat['label'], 
                         style={'font-weight': '500', 'color': '#4A5568', 'flex': '1'}),
                html.Span(str(stat['value']), 
                         style={'font-weight': '700', 'color': color, 'font-size': '1.1rem'})
            ], style={
                'display': 'flex',
                'align-items': 'center',
                'padding': '12px 16px',
                'background': 'white',
                'border-radius': '10px',
                'margin-bottom': '8px',
                'box-shadow': '0 2px 8px rgba(0,0,0,0.05)',
                'transition': 'all 0.2s ease'
            })
        ]) for stat in stats
    ]

@app.callback(
    Output('stats_setosa', 'children'),
    Input('liste_pour_setosa', 'value')
)
def stats_setosa(val):
    return create_stat_display(val, 'setosa', colors['setosa'])

@app.callback(
    Output('stats_versicolor', 'children'),
    Input('liste_pour_versicolor', 'value')
)
def stats_versicolor(val):
    return create_stat_display(val, 'versicolor', colors['versicolor'])

@app.callback(
    Output('stats_virginica', 'children'),
    Input('liste_pour_virginica', 'value')
)
def stats_virginica(val):
    return create_stat_display(val, 'virginica', colors['virginica'])

app.title = 'Iris Dashboard - Analyse Interactive'

if __name__ == '__main__':
    app.run(debug=True, port=8050)