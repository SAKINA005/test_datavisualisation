# =============================================================================
# IMPORTS ET CONFIGURATION
# =============================================================================
from dash import html, Dash, dcc, dash_table, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

# Configuration du dataset
df = px.data.iris()
liste_variable_numeric = [col for col in df.columns if col not in ['species', 'species_id']]

# Palette futuriste
COLORS = {
    'setosa': '#FF00FF', 'versicolor': '#00FFFF', 'virginica': '#00FF00',
    'background': '#0a0a0a', 'card_bg': 'rgba(20, 20, 30, 0.6)',
    'text_primary': '#ffffff', 'text_secondary': '#a0a0a0', 'accent': '#FF00FF'
}

FONTS = {
    'title': 'Orbitron, sans-serif',
    'body': 'Space Grotesk, sans-serif'
}

# =============================================================================
# FONCTIONS UTILITAIRES (SANS CALLBACKS)
# =============================================================================
def neon_card(title, children, icon="⚡"):
    """Carte avec effet néon et glassmorphism"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Span(icon, style={
                    'font-size': '2rem', 'margin-right': '15px',
                    'filter': 'drop-shadow(0 0 8px currentColor)'
                }),
                html.H3(title, style={
                    'font-family': FONTS['title'], 'font-weight': '700',
                    'color': COLORS['text_primary'], 'margin': 0,
                    'text-shadow': '0 0 10px rgba(255,255,255,0.5)'
                })
            ], className='d-flex align-items-center mb-4'),
            children
        ])
    ], style={
        'background': COLORS['card_bg'], 'backdrop-filter': 'blur(20px)',
        'border': f'1px solid {COLORS["accent"]}33', 'border-radius': '20px',
        'box-shadow': f'0 0 30px {COLORS["accent"]}33, inset 0 0 20px rgba(255,255,255,0.05)',
        'transition': 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
        'overflow': 'hidden', 'position': 'relative'
    }, className='neon-card')

def animated_stat(value, label, color):
    """Statistique avec animation"""
    return html.Div([
        html.Div(f'{value}', style={
            'font-size': '2rem', 'font-weight': '800', 'color': color,
            'font-family': FONTS['title'], 'text-shadow': f'0 0 15px {color}',
            'animation': 'slideIn 0.6s ease-out'
        }),
        html.Div(label, style={
            'font-size': '0.9rem', 'color': COLORS['text_secondary'], 'margin-top': '5px'
        })
    ], style={'text-align': 'center', 'padding': '15px'})

def create_futuristic_scatter(x, y, title, z=None):
    """Crée un graphique scatter avec style néon"""
    fig = go.Figure()
    for species in df['species'].unique():
        species_data = df[df['species'] == species]
        if z:
            fig.add_trace(go.Scatter3d(
                x=species_data[x], y=species_data[y], z=species_data[z],
                mode='markers', name=species, marker=dict(
                    size=8, color=COLORS[species], opacity=0.9,
                    line=dict(width=2, color='white')
                ), text=species_data['species'], hovertemplate='<b>%{text}</b><br>' +
                f'{x}: %{{x}}<br>{y}: %{{y}}<br>{z}: %{{z}}<extra></extra>'
            ))
            fig.update_layout(scene=dict(
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=x.replace('_', ' ').title()),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=y.replace('_', ' ').title()),
                zaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=z.replace('_', ' ').title()),
                bgcolor='rgba(0,0,0,0.5)'
            ))
        else:
            fig.add_trace(go.Scatter(
                x=species_data[x], y=species_data[y], mode='markers',
                name=species, marker=dict(size=12, color=COLORS[species], opacity=0.8,
                line=dict(width=2, color='white')),
                text=species_data['species'], hovertemplate=f'<b>{species}</b><br>' +
                f'{x}: %{{x}}<br>{y}: %{{y}}<extra></extra>'
            ))
            fig.update_layout(
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True, zeroline=False),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True, zeroline=False)
            )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family=FONTS['title'], color=COLORS['text_primary']),
                   x=0.5, xanchor='center'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(family=FONTS['body'], color=COLORS['text_secondary']),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(color=COLORS['text_primary'])),
        margin=dict(t=80, b=50, l=50, r=50)
    )
    return fig

# =============================================================================
# CRÉATION DE L'APPLICATION DASH (ESSENTIEL : DOIT ÊTRE AVANT LES CALLBACKS)
# =============================================================================
app = Dash(__name__, external_stylesheets=[
    dbc.themes.DARKLY,
    'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600&display=swap'
], suppress_callback_exceptions=True)

server = app.server  # Requis pour Gunicorn

# =============================================================================
# LAYOUTS
# =============================================================================
layout_home = html.Div([
    html.Div([
        dbc.Container([
            html.Div([
                html.H1('IRIS DATASET 2077', style={
                    'font-family': FONTS['title'], 'font-size': '4rem', 'font-weight': '900',
                    'background': 'linear-gradient(135deg, #FF00FF 0%, #00FFFF 50%, #00FF00 100%)',
                    '-webkit-background-clip': 'text', '-webkit-text-fill-color': 'transparent',
                    'text-align': 'center', 'margin-bottom': '20px', 'animation': 'glow 3s ease-in-out infinite',
                    'position': 'relative', 'z-index': 2
                }),
                html.P('Analyse biométrique avancée des classifications florales', style={
                    'font-family': FONTS['body'], 'font-size': '1.3rem', 'color': COLORS['text_secondary'],
                    'text-align': 'center', 'max-width': '600px', 'margin': '0 auto', 'position': 'relative', 'z-index': 2
                })
            ], style={'padding': '100px 0', 'position': 'relative'})
        ], fluid=True),
        html.Div([
            *[html.Div(className='particle', style={
                '--x': f'{i*25}%', '--y': f'{i*20}%', '--delay': f'{i*0.5}s',
                '--color': ['#FF00FF', '#00FFFF', '#00FF00', '#FFFF00'][i]
            }) for i in range(4)]
        ], style={'position': 'absolute', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'overflow': 'hidden', 'z-index': 1})
    ], style={'background': 'radial-gradient(ellipse at center, #1a1a2e 0%, #0a0a0a 100%)', 'margin-bottom': '50px', 'position': 'relative', 'overflow': 'hidden'}),
    
    dbc.Container([
        dbc.Row([
            dbc.Col([neon_card('🧬 SETOSA', html.Div([
                dcc.Dropdown(options=[{'label': v.replace('_', ' ').title(), 'value': v} for v in liste_variable_numeric],
                            value='sepal_length', id='dropdown-setosa', style={
                                'background': 'rgba(255,0,255,0.1)', 'border': '1px solid rgba(255,0,255,0.3)',
                                'border-radius': '12px', 'margin-bottom': '20px'
                            }), html.Div(id='stats-setosa', style={'animation': 'fadeIn 0.5s ease'})
            ]), icon='🌺')], lg=4, md=12, className='mb-4'),
            
            dbc.Col([neon_card('⚡ VERSICOLOR', html.Div([
                dcc.Dropdown(options=[{'label': v.replace('_', ' ').title(), 'value': v} for v in liste_variable_numeric],
                            value='sepal_length', id='dropdown-versicolor', style={
                                'background': 'rgba(0,255,255,0.1)', 'border': '1px solid rgba(0,255,255,0.3)',
                                'border-radius': '12px', 'margin-bottom': '20px'
                            }), html.Div(id='stats-versicolor', style={'animation': 'fadeIn 0.5s ease'})
            ]), icon='🌼')], lg=4, md=12, className='mb-4'),
            
            dbc.Col([neon_card('🚀 VIRGINICA', html.Div([
                dcc.Dropdown(options=[{'label': v.replace('_', ' ').title(), 'value': v} for v in liste_variable_numeric],
                            value='sepal_length', id='dropdown-virginica', style={
                                'background': 'rgba(0,255,0,0.1)', 'border': '1px solid rgba(0,255,0,0.3)',
                                'border-radius': '12px', 'margin-bottom': '20px'
                            }), html.Div(id='stats-virginica', style={'animation': 'fadeIn 0.5s ease'})
            ]), icon='🌷')], lg=4, md=12, className='mb-4'),
        ], className='g-4'),
        
        neon_card('📡 Visualisations Dimensionnelles Avancées', html.Div([
            dbc.Row([dbc.Col([html.Label('Mode d\'affichage:', style={'font-family': FONTS['body'], 'color': COLORS['text_secondary']}),
            dbc.RadioItems(options=[{"label": "🌌 Standard", "value": "standard"}, {"label": "⚡ Néon", "value": "neon"}, {"label": "🌐 3D", "value": "3d"}],
                          id='graph-mode', value='neon', inline=True, style={'margin-bottom': '30px'})])]),
            html.Div(id='graph-container', style={'animation': 'fadeIn 0.8s ease'})
        ]), icon='📊'),
        
        neon_card('🗄️ Matrice de Données Biométriques', dash_table.DataTable(
            df.to_dict(orient='records'),
            columns=[{'name': col.replace('_', ' ').title(), 'id': col} for col in df.columns],
            page_size=10, style_table={'overflowX': 'auto', 'border-radius': '15px', 'overflow': 'hidden'},
            style_header={'background': 'linear-gradient(135deg, #FF00FF, #00FFFF)', 'color': 'white', 'fontWeight': '700',
                         'font-family': FONTS['title'], 'padding': '15px', 'border': 'none'},
            style_cell={'background': 'rgba(20, 20, 30, 0.8)', 'color': COLORS['text_primary'],
                       'font-family': FONTS['body'], 'padding': '12px', 'border': '1px solid rgba(255,255,255,0.05)'},
            style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgba(30, 30, 40, 0.6)'},
                                   {'if': {'state': 'selected'}, 'backgroundColor': 'rgba(255, 0, 255, 0.2)', 'border': '1px solid #FF00FF'}]
        ), icon='📋')
        
    ], fluid=True, style={'padding': '0 40px 50px 40px'})
], style={'background': COLORS['background'], 'min-height': '100vh', 'font-family': FONTS['body']})

# =============================================================================
# CALLBACKS (TOUS APRÈS LA CRÉATION DE 'app')
# =============================================================================
@app.callback(Output('stats-setosa', 'children'), Input('dropdown-setosa', 'value'))
def update_setosa_stats(var):
    return create_species_stats(var, 'setosa', COLORS['setosa'])

@app.callback(Output('stats-versicolor', 'children'), Input('dropdown-versicolor', 'value'))
def update_versicolor_stats(var):
    return create_species_stats(var, 'versicolor', COLORS['versicolor'])

@app.callback(Output('stats-virginica', 'children'), Input('dropdown-virginica', 'value'))
def update_virginica_stats(var):
    return create_species_stats(var, 'virginica', COLORS['virginica'])

@app.callback(Output('graph-container', 'children'), Input('graph-mode', 'value'))
def update_graphs(mode):
    if mode == '3d':
        fig = create_futuristic_scatter('petal_length', 'petal_width', 'sepal_length', 'Vue Tri-dimensionnelle')
        return dbc.Col(dcc.Graph(figure=fig, config={'displayModeBar': False}), width=12)
    else:
        fig1 = create_futuristic_scatter('sepal_length', 'sepal_width', 'Sepale: Longueur vs Largeur')
        fig2 = create_futuristic_scatter('petal_length', 'petal_width', 'Pétale: Longueur vs Largeur')
        return [dbc.Col(dcc.Graph(figure=fig1, config={'displayModeBar': False}), lg=6, md=12, className='mb-4'),
                dbc.Col(dcc.Graph(figure=fig2, config={'displayModeBar': False}), lg=6, md=12, className='mb-4')]

def create_species_stats(var, species, color):
    """Génère les statistiques pour une espèce"""
    data = df[df['species'] == species][var]
    return dbc.Row([
        dbc.Col(animated_stat(f'{data.mean():.2f}', 'Moyenne', color), md=6),
        dbc.Col(animated_stat(f'{data.std():.2f}', 'Écart-type', color), md=6),
    ], className='g-2') + dbc.Row([
        dbc.Col(animated_stat(f'{data.max():.2f}', 'Max', color), md=6),
        dbc.Col(animated_stat(f'{data.min():.2f}', 'Min', color), md=6),
    ], className='g-2')

# =============================================================================
# LAYOUT PRINCIPAL
# =============================================================================
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='navbar-container'),
    html.Div(id='page-container')
])

@app.callback(Output('navbar-container', 'children'), Output('page-container', 'children'), Input('url', 'pathname'))
def route(path):
    return create_navbar(path), layout_home

def create_navbar(pathname):
    """Navbar futuriste"""
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span('🌸', style={'font-size': '2.5rem', 'animation': 'pulse 2s infinite',
                                               'filter': 'drop-shadow(0 0 10px #FF00FF)'}),
                        html.Span('IRIS 2077', style={
                            'font-size': '2rem', 'font-weight': '900', 'font-family': FONTS['title'],
                            'background': 'linear-gradient(135deg, #FF00FF 0%, #00FFFF 100%)',
                            '-webkit-background-clip': 'text', '-webkit-text-fill-color': 'transparent',
                            'margin-left': '15px', 'text-shadow': '0 0 20px rgba(255,0,255,0.5)'
                        })
                    ], style={'display': 'flex', 'align-items': 'center'})
                ], width="auto"),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span(link['icon'], style={'margin-right': '8px'}),
                            link['label'],
                            html.Div(style={'height': '2px', 'background': COLORS['accent'],
                                           'width': '100%' if pathname == link['href'] else '0%',
                                           'transition': 'width 0.3s ease', 'marginTop': '5px',
                                           'boxShadow': f'0 0 10px {COLORS["accent"]}'})
                        ], style={'color': COLORS['text_primary'] if pathname == link['href'] else COLORS['text_secondary'],
                                 'font-weight': '600', 'cursor': 'pointer', 'padding': '10px 20px',
                                 'border': f'1px solid {COLORS["accent"]}4D' if pathname == link['href'] else '1px solid transparent',
                                 'border-radius': '12px', 'background': 'rgba(255,0,255,0.1)' if pathname == link['href'] else 'transparent',
                                 'transition': 'all 0.3s ease', 'text-decoration': 'none', 'display': 'inline-block', 'margin': '0 10px'})
                        for link in [{"label": "Accueil", "href": "/", "icon": "🏠"}, {"label": "Analyse FDA", "href": "/fda", "icon": "🧬"}]
                    ], style={'display': 'flex', 'justify-content': 'flex-end'})
                ])
            ], align='center', className='g-0')
        ], fluid=True)
    ], style={'background': 'rgba(10, 10, 10, 0.8)', 'backdrop-filter': 'blur(20px)', 'padding': '20px 0',
              'border-bottom': f'1px solid {COLORS["accent"]}4D', 'position': 'sticky', 'top': 0, 'z-index': 1000,
              'box-shadow': '0 5px 30px rgba(255, 0, 255, 0.1)'})

# =============================================================================
# CSS PERSONNALISÉ ET ANIMATIONS
# =============================================================================
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>Iris Dashboard 2077</title>
{%favicon%}
{%css%}
<style>
* { box-sizing: border-box; }
@keyframes glow { 0%, 100% { filter: brightness(1) drop-shadow(0 0 15px #FF00FF); }
                  50% { filter: brightness(1.2) drop-shadow(0 0 25px #00FFFF); } }
@keyframes slideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
.particle { position: absolute; width: 4px; height: 4px; background: var(--color); border-radius: 50%;
            animation: float 6s ease-in-out infinite; animation-delay: var(--delay); box-shadow: 0 0 10px var(--color); }
.neon-card:hover { transform: translateY(-10px) scale(1.02); box-shadow: 0 0 50px rgba(255, 0, 255, 0.4), inset 0 0 30px rgba(255,255,255,0.1) !important; border-color: rgba(255, 0, 255, 0.6) !important; }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #FF00FF, #00FFFF); border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #00FFFF, #FF00FF); }
.Select-control, .Select-menu-outer { background: rgba(20, 20, 30, 0.9) !important; border: 1px solid rgba(255,0,255,0.3) !important; color: white !important; }
.Select-value-label, .Select-option { color: white !important; }
.Select-option:hover { background: rgba(255,0,255,0.2) !important; }
.form-check-input:checked { background-color: #FF00FF !important; border-color: #FF00FF !important; box-shadow: 0 0 10px #FF00FF; }
.form-check-input:focus { box-shadow: 0 0 0 0.25rem rgba(255, 0, 255, 0.25); }
@media (max-width: 768px) { h1 { font-size: 2.5rem !important; } .neon-card { margin-bottom: 20px; } }
</style>
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''

# =============================================================================
# DÉMARRAGE
# =============================================================================
if __name__ == '__main__':
    app.run(debug=True, port=8050)# =============================================================================
# IMPORTS ET CONFIGURATION
# =============================================================================
from dash import html, Dash, dcc, dash_table, Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

# Configuration du dataset
df = px.data.iris()
liste_variable_numeric = [col for col in df.columns if col not in ['species', 'species_id']]

# Palette futuriste
COLORS = {
    'setosa': '#FF00FF', 'versicolor': '#00FFFF', 'virginica': '#00FF00',
    'background': '#0a0a0a', 'card_bg': 'rgba(20, 20, 30, 0.6)',
    'text_primary': '#ffffff', 'text_secondary': '#a0a0a0', 'accent': '#FF00FF'
}

FONTS = {
    'title': 'Orbitron, sans-serif',
    'body': 'Space Grotesk, sans-serif'
}

# =============================================================================
# FONCTIONS UTILITAIRES (SANS CALLBACKS)
# =============================================================================
def neon_card(title, children, icon="⚡"):
    """Carte avec effet néon et glassmorphism"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Span(icon, style={
                    'font-size': '2rem', 'margin-right': '15px',
                    'filter': 'drop-shadow(0 0 8px currentColor)'
                }),
                html.H3(title, style={
                    'font-family': FONTS['title'], 'font-weight': '700',
                    'color': COLORS['text_primary'], 'margin': 0,
                    'text-shadow': '0 0 10px rgba(255,255,255,0.5)'
                })
            ], className='d-flex align-items-center mb-4'),
            children
        ])
    ], style={
        'background': COLORS['card_bg'], 'backdrop-filter': 'blur(20px)',
        'border': f'1px solid {COLORS["accent"]}33', 'border-radius': '20px',
        'box-shadow': f'0 0 30px {COLORS["accent"]}33, inset 0 0 20px rgba(255,255,255,0.05)',
        'transition': 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
        'overflow': 'hidden', 'position': 'relative'
    }, className='neon-card')

def animated_stat(value, label, color):
    """Statistique avec animation"""
    return html.Div([
        html.Div(f'{value}', style={
            'font-size': '2rem', 'font-weight': '800', 'color': color,
            'font-family': FONTS['title'], 'text-shadow': f'0 0 15px {color}',
            'animation': 'slideIn 0.6s ease-out'
        }),
        html.Div(label, style={
            'font-size': '0.9rem', 'color': COLORS['text_secondary'], 'margin-top': '5px'
        })
    ], style={'text-align': 'center', 'padding': '15px'})

def create_futuristic_scatter(x, y, title, z=None):
    """Crée un graphique scatter avec style néon"""
    fig = go.Figure()
    for species in df['species'].unique():
        species_data = df[df['species'] == species]
        if z:
            fig.add_trace(go.Scatter3d(
                x=species_data[x], y=species_data[y], z=species_data[z],
                mode='markers', name=species, marker=dict(
                    size=8, color=COLORS[species], opacity=0.9,
                    line=dict(width=2, color='white')
                ), text=species_data['species'], hovertemplate='<b>%{text}</b><br>' +
                f'{x}: %{{x}}<br>{y}: %{{y}}<br>{z}: %{{z}}<extra></extra>'
            ))
            fig.update_layout(scene=dict(
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=x.replace('_', ' ').title()),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=y.replace('_', ' ').title()),
                zaxis=dict(gridcolor='rgba(255,255,255,0.1)', title=z.replace('_', ' ').title()),
                bgcolor='rgba(0,0,0,0.5)'
            ))
        else:
            fig.add_trace(go.Scatter(
                x=species_data[x], y=species_data[y], mode='markers',
                name=species, marker=dict(size=12, color=COLORS[species], opacity=0.8,
                line=dict(width=2, color='white')),
                text=species_data['species'], hovertemplate=f'<b>{species}</b><br>' +
                f'{x}: %{{x}}<br>{y}: %{{y}}<extra></extra>'
            ))
            fig.update_layout(
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True, zeroline=False),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', showgrid=True, zeroline=False)
            )
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, family=FONTS['title'], color=COLORS['text_primary']),
                   x=0.5, xanchor='center'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
        font=dict(family=FONTS['body'], color=COLORS['text_secondary']),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5,
                    font=dict(color=COLORS['text_primary'])),
        margin=dict(t=80, b=50, l=50, r=50)
    )
    return fig

# =============================================================================
# CRÉATION DE L'APPLICATION DASH (ESSENTIEL : DOIT ÊTRE AVANT LES CALLBACKS)
# =============================================================================
app = Dash(__name__, external_stylesheets=[
    dbc.themes.DARKLY,
    'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600&display=swap'
], suppress_callback_exceptions=True)

server = app.server  # Requis pour Gunicorn

# =============================================================================
# LAYOUTS
# =============================================================================
layout_home = html.Div([
    html.Div([
        dbc.Container([
            html.Div([
                html.H1('IRIS DATASET 2077', style={
                    'font-family': FONTS['title'], 'font-size': '4rem', 'font-weight': '900',
                    'background': 'linear-gradient(135deg, #FF00FF 0%, #00FFFF 50%, #00FF00 100%)',
                    '-webkit-background-clip': 'text', '-webkit-text-fill-color': 'transparent',
                    'text-align': 'center', 'margin-bottom': '20px', 'animation': 'glow 3s ease-in-out infinite',
                    'position': 'relative', 'z-index': 2
                }),
                html.P('Analyse biométrique avancée des classifications florales', style={
                    'font-family': FONTS['body'], 'font-size': '1.3rem', 'color': COLORS['text_secondary'],
                    'text-align': 'center', 'max-width': '600px', 'margin': '0 auto', 'position': 'relative', 'z-index': 2
                })
            ], style={'padding': '100px 0', 'position': 'relative'})
        ], fluid=True),
        html.Div([
            *[html.Div(className='particle', style={
                '--x': f'{i*25}%', '--y': f'{i*20}%', '--delay': f'{i*0.5}s',
                '--color': ['#FF00FF', '#00FFFF', '#00FF00', '#FFFF00'][i]
            }) for i in range(4)]
        ], style={'position': 'absolute', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'overflow': 'hidden', 'z-index': 1})
    ], style={'background': 'radial-gradient(ellipse at center, #1a1a2e 0%, #0a0a0a 100%)', 'margin-bottom': '50px', 'position': 'relative', 'overflow': 'hidden'}),
    
    dbc.Container([
        dbc.Row([
            dbc.Col([neon_card('🧬 SETOSA', html.Div([
                dcc.Dropdown(options=[{'label': v.replace('_', ' ').title(), 'value': v} for v in liste_variable_numeric],
                            value='sepal_length', id='dropdown-setosa', style={
                                'background': 'rgba(255,0,255,0.1)', 'border': '1px solid rgba(255,0,255,0.3)',
                                'border-radius': '12px', 'margin-bottom': '20px'
                            }), html.Div(id='stats-setosa', style={'animation': 'fadeIn 0.5s ease'})
            ]), icon='🌺')], lg=4, md=12, className='mb-4'),
            
            dbc.Col([neon_card('⚡ VERSICOLOR', html.Div([
                dcc.Dropdown(options=[{'label': v.replace('_', ' ').title(), 'value': v} for v in liste_variable_numeric],
                            value='sepal_length', id='dropdown-versicolor', style={
                                'background': 'rgba(0,255,255,0.1)', 'border': '1px solid rgba(0,255,255,0.3)',
                                'border-radius': '12px', 'margin-bottom': '20px'
                            }), html.Div(id='stats-versicolor', style={'animation': 'fadeIn 0.5s ease'})
            ]), icon='🌼')], lg=4, md=12, className='mb-4'),
            
            dbc.Col([neon_card('🚀 VIRGINICA', html.Div([
                dcc.Dropdown(options=[{'label': v.replace('_', ' ').title(), 'value': v} for v in liste_variable_numeric],
                            value='sepal_length', id='dropdown-virginica', style={
                                'background': 'rgba(0,255,0,0.1)', 'border': '1px solid rgba(0,255,0,0.3)',
                                'border-radius': '12px', 'margin-bottom': '20px'
                            }), html.Div(id='stats-virginica', style={'animation': 'fadeIn 0.5s ease'})
            ]), icon='🌷')], lg=4, md=12, className='mb-4'),
        ], className='g-4'),
        
        neon_card('📡 Visualisations Dimensionnelles Avancées', html.Div([
            dbc.Row([dbc.Col([html.Label('Mode d\'affichage:', style={'font-family': FONTS['body'], 'color': COLORS['text_secondary']}),
            dbc.RadioItems(options=[{"label": "🌌 Standard", "value": "standard"}, {"label": "⚡ Néon", "value": "neon"}, {"label": "🌐 3D", "value": "3d"}],
                          id='graph-mode', value='neon', inline=True, style={'margin-bottom': '30px'})])]),
            html.Div(id='graph-container', style={'animation': 'fadeIn 0.8s ease'})
        ]), icon='📊'),
        
        neon_card('🗄️ Matrice de Données Biométriques', dash_table.DataTable(
            df.to_dict(orient='records'),
            columns=[{'name': col.replace('_', ' ').title(), 'id': col} for col in df.columns],
            page_size=10, style_table={'overflowX': 'auto', 'border-radius': '15px', 'overflow': 'hidden'},
            style_header={'background': 'linear-gradient(135deg, #FF00FF, #00FFFF)', 'color': 'white', 'fontWeight': '700',
                         'font-family': FONTS['title'], 'padding': '15px', 'border': 'none'},
            style_cell={'background': 'rgba(20, 20, 30, 0.8)', 'color': COLORS['text_primary'],
                       'font-family': FONTS['body'], 'padding': '12px', 'border': '1px solid rgba(255,255,255,0.05)'},
            style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgba(30, 30, 40, 0.6)'},
                                   {'if': {'state': 'selected'}, 'backgroundColor': 'rgba(255, 0, 255, 0.2)', 'border': '1px solid #FF00FF'}]
        ), icon='📋')
        
    ], fluid=True, style={'padding': '0 40px 50px 40px'})
], style={'background': COLORS['background'], 'min-height': '100vh', 'font-family': FONTS['body']})

# =============================================================================
# CALLBACKS (TOUS APRÈS LA CRÉATION DE 'app')
# =============================================================================
@app.callback(Output('stats-setosa', 'children'), Input('dropdown-setosa', 'value'))
def update_setosa_stats(var):
    return create_species_stats(var, 'setosa', COLORS['setosa'])

@app.callback(Output('stats-versicolor', 'children'), Input('dropdown-versicolor', 'value'))
def update_versicolor_stats(var):
    return create_species_stats(var, 'versicolor', COLORS['versicolor'])

@app.callback(Output('stats-virginica', 'children'), Input('dropdown-virginica', 'value'))
def update_virginica_stats(var):
    return create_species_stats(var, 'virginica', COLORS['virginica'])

@app.callback(Output('graph-container', 'children'), Input('graph-mode', 'value'))
def update_graphs(mode):
    if mode == '3d':
        fig = create_futuristic_scatter('petal_length', 'petal_width', 'sepal_length', 'Vue Tri-dimensionnelle')
        return dbc.Col(dcc.Graph(figure=fig, config={'displayModeBar': False}), width=12)
    else:
        fig1 = create_futuristic_scatter('sepal_length', 'sepal_width', 'Sepale: Longueur vs Largeur')
        fig2 = create_futuristic_scatter('petal_length', 'petal_width', 'Pétale: Longueur vs Largeur')
        return [dbc.Col(dcc.Graph(figure=fig1, config={'displayModeBar': False}), lg=6, md=12, className='mb-4'),
                dbc.Col(dcc.Graph(figure=fig2, config={'displayModeBar': False}), lg=6, md=12, className='mb-4')]

def create_species_stats(var, species, color):
    """Génère les statistiques pour une espèce"""
    data = df[df['species'] == species][var]
    return dbc.Row([
        dbc.Col(animated_stat(f'{data.mean():.2f}', 'Moyenne', color), md=6),
        dbc.Col(animated_stat(f'{data.std():.2f}', 'Écart-type', color), md=6),
    ], className='g-2') + dbc.Row([
        dbc.Col(animated_stat(f'{data.max():.2f}', 'Max', color), md=6),
        dbc.Col(animated_stat(f'{data.min():.2f}', 'Min', color), md=6),
    ], className='g-2')

# =============================================================================
# LAYOUT PRINCIPAL
# =============================================================================
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='navbar-container'),
    html.Div(id='page-container')
])

@app.callback(Output('navbar-container', 'children'), Output('page-container', 'children'), Input('url', 'pathname'))
def route(path):
    return create_navbar(path), layout_home

def create_navbar(pathname):
    """Navbar futuriste"""
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Span('🌸', style={'font-size': '2.5rem', 'animation': 'pulse 2s infinite',
                                               'filter': 'drop-shadow(0 0 10px #FF00FF)'}),
                        html.Span('IRIS 2077', style={
                            'font-size': '2rem', 'font-weight': '900', 'font-family': FONTS['title'],
                            'background': 'linear-gradient(135deg, #FF00FF 0%, #00FFFF 100%)',
                            '-webkit-background-clip': 'text', '-webkit-text-fill-color': 'transparent',
                            'margin-left': '15px', 'text-shadow': '0 0 20px rgba(255,0,255,0.5)'
                        })
                    ], style={'display': 'flex', 'align-items': 'center'})
                ], width="auto"),
                dbc.Col([
                    html.Div([
                        html.Div([
                            html.Span(link['icon'], style={'margin-right': '8px'}),
                            link['label'],
                            html.Div(style={'height': '2px', 'background': COLORS['accent'],
                                           'width': '100%' if pathname == link['href'] else '0%',
                                           'transition': 'width 0.3s ease', 'marginTop': '5px',
                                           'boxShadow': f'0 0 10px {COLORS["accent"]}'})
                        ], style={'color': COLORS['text_primary'] if pathname == link['href'] else COLORS['text_secondary'],
                                 'font-weight': '600', 'cursor': 'pointer', 'padding': '10px 20px',
                                 'border': f'1px solid {COLORS["accent"]}4D' if pathname == link['href'] else '1px solid transparent',
                                 'border-radius': '12px', 'background': 'rgba(255,0,255,0.1)' if pathname == link['href'] else 'transparent',
                                 'transition': 'all 0.3s ease', 'text-decoration': 'none', 'display': 'inline-block', 'margin': '0 10px'})
                        for link in [{"label": "Accueil", "href": "/", "icon": "🏠"}, {"label": "Analyse FDA", "href": "/fda", "icon": "🧬"}]
                    ], style={'display': 'flex', 'justify-content': 'flex-end'})
                ])
            ], align='center', className='g-0')
        ], fluid=True)
    ], style={'background': 'rgba(10, 10, 10, 0.8)', 'backdrop-filter': 'blur(20px)', 'padding': '20px 0',
              'border-bottom': f'1px solid {COLORS["accent"]}4D', 'position': 'sticky', 'top': 0, 'z-index': 1000,
              'box-shadow': '0 5px 30px rgba(255, 0, 255, 0.1)'})

# =============================================================================
# CSS PERSONNALISÉ ET ANIMATIONS
# =============================================================================
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>Iris Dashboard 2077</title>
{%favicon%}
{%css%}
<style>
* { box-sizing: border-box; }
@keyframes glow { 0%, 100% { filter: brightness(1) drop-shadow(0 0 15px #FF00FF); }
                  50% { filter: brightness(1.2) drop-shadow(0 0 25px #00FFFF); } }
@keyframes slideIn { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
.particle { position: absolute; width: 4px; height: 4px; background: var(--color); border-radius: 50%;
            animation: float 6s ease-in-out infinite; animation-delay: var(--delay); box-shadow: 0 0 10px var(--color); }
.neon-card:hover { transform: translateY(-10px) scale(1.02); box-shadow: 0 0 50px rgba(255, 0, 255, 0.4), inset 0 0 30px rgba(255,255,255,0.1) !important; border-color: rgba(255, 0, 255, 0.6) !important; }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #FF00FF, #00FFFF); border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #00FFFF, #FF00FF); }
.Select-control, .Select-menu-outer { background: rgba(20, 20, 30, 0.9) !important; border: 1px solid rgba(255,0,255,0.3) !important; color: white !important; }
.Select-value-label, .Select-option { color: white !important; }
.Select-option:hover { background: rgba(255,0,255,0.2) !important; }
.form-check-input:checked { background-color: #FF00FF !important; border-color: #FF00FF !important; box-shadow: 0 0 10px #FF00FF; }
.form-check-input:focus { box-shadow: 0 0 0 0.25rem rgba(255, 0, 255, 0.25); }
@media (max-width: 768px) { h1 { font-size: 2.5rem !important; } .neon-card { margin-bottom: 20px; } }
</style>
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''

# =============================================================================
# DÉMARRAGE
# =============================================================================
if __name__ == '__main__':
    app.run(debug=True, port=8080)