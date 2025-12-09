from dash import html, Dash, dcc, dash_table, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
from nav_bar import navbar

df = px.data.iris()

colors = {
    'setosa': 'red',
    'versicolor': 'darkgreen',
    'virginica': 'lightpink'
}


liste_variable_numeric = list(df.columns)
liste_variable_numeric.remove('species')
liste_variable_numeric.remove('species_id')

#mean_setosa = round(df.loc[df['species']=='setosa' ,'sepal_length'].mean(), 2)
#mean_versicolor = round(df.loc[df['species']=='versicolor' ,'sepal_length'].mean(), 2)
#mean_viginica = round(df.loc[df['species']=='virginica' ,'sepal_length'].mean(), 2)

# ========================== Graph ====================================
scatter_plot = px.scatter(df, x='sepal_length', y='sepal_width', color='species', color_discrete_map=colors)
scatter_plot2 = px.scatter(df,x='petal_length', y='petal_width', color='species',color_discrete_map=colors )
scatter_plot3 = px.scatter_3d(df,x='petal_length', y='petal_width', z='sepal_length', color='species', color_discrete_map=colors)

scatter_plot.update_layout(template='plotly_white')
scatter_plot2.update_layout(template='plotly_dark')

# ========================== Table ====================================
table =  dash_table.DataTable(df.to_dict(orient='records'), page_size=10)

# ========================== Liste dÃ©roulante ====================================

liste_deroulante1 = dcc.Dropdown(options=liste_variable_numeric,
                                 value=liste_variable_numeric[0],
                                 id='liste_pour_setosa')
liste_deroulante2 = dcc.Dropdown(options=liste_variable_numeric,
                                 value=liste_variable_numeric[0],
                                 id='liste_pour_versicolor')
liste_deroulante3 = dcc.Dropdown(options=liste_variable_numeric,
                                 value=liste_variable_numeric[0],
                                 id='liste_pour_virginica')
# ==========================  ====================================
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


layout1 = html.Div(children=[
    #Statistics
    dbc.Row([
        dbc.Col(
            dbc.Card([
                    dbc.CardHeader(html.H4('Setosa', style={'text-align': 'center',})),
                    dbc.CardBody([
                        liste_deroulante1,
                        html.Div(id='stats_setosa',
                            style={'display': 'flex', 'flex-direction': 'column'}),
                    ])
                ]),
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4('Versicolor', style={'text-align': 'center'})),
                dbc.CardBody([
                    liste_deroulante2,
                    html.Div(id='stats_versicolor',
                             style={'display': 'flex', 'flex-direction': 'column'}),
                ])
            ]),
        ),

        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H4('Virginica', style={'text-align': 'center'})),
                dbc.CardBody([
                    liste_deroulante3,
                    html.Div(id='stats_virginica',
                             style={'display': 'flex', 'flex-direction': 'column'}),
                ])
            ]),
        ),
    ], style={'margin-bottom': '10px'}),

    #Grapgh
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H5("Sélection du thème", className="mb-0"),
                ]),
                dbc.Col([
                    dbc.RadioItems(
                        options=[
                            {"label": "Plotly", "value": "plotly"},
                            {"label": "White", "value": "plotly_white"},
                            {"label": "Dark", "value": "plotly_dark"},
                            {"label": "GGPlot2", "value": "ggplot2"},
                            {"label": "Seaborn", "value": "seaborn"},
                            {"label": "Simple", "value": "simple_white"},
                        ],
                        id='style_graph',
                        inline=True,
                        value='plotly_white',
                        className="mb-0"
                    ),
                ]),
            ], justify="between", align="center", className="g-0")
        ], className="bg-light"),

        dbc.CardBody([
            dbc.Row([
                dbc.Col(dcc.Graph(figure=scatter_plot, config={'displayModeBar': False}), lg=4, md=12,
                        className="mb-3 mb-lg-0"),
                dbc.Col(dcc.Graph(figure=scatter_plot2, config={'displayModeBar': False}), lg=4, md=12,
                        className="mb-3 mb-lg-0"),
                dbc.Col(dcc.Graph(figure=scatter_plot3, config={'displayModeBar': False}), lg=4, md=12,
                        className="mb-3 mb-lg-0"),
            ], id='graphs', className="g-3")
        ], className="p-4")
    ], className="shadow-sm mb-4"),


    dbc.Card([
        dbc.CardBody(table, className="p-0")
    ], className="shadow-sm"),

    #Table
    table
])

layout2 = html.Div([
    html.H1('Page 2')
])

app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='navbar_content'),
    html.Div(layout1, id='page_content')
])

@app.callback(
    Output('navbar_content', 'children'),
    Output('page_content', 'children'),
    Input(component_id='url', component_property='pathname')
)
def swtich_page(path):
    actual_navbar = navbar(lien=path)
    if path=='/':
        page_content = layout1
    elif path=='/fda':
        page_content = layout2
    else:
        page_content = html.H3('404 page not found')

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
            dbc.Col(dcc.Graph(figure=scatter_plot)),
            dbc.Col(dcc.Graph(figure=scatter_plot2),),
            dbc.Col(dcc.Graph(figure=scatter_plot3),),
                ]

#===================Affichage des infos sur setosa ================
@app.callback(
    Output(component_id='stats_setosa', component_property='children'),
    Input(component_id='liste_pour_setosa', component_property='value')
)
def statsSetosa(val):

    moyenne = round(df.loc[df['species']=='setosa', val].mean(), 2)
    variance = round(df.loc[df['species']=='setosa', val].std(), 2)
    max = df.loc[df['species']=='setosa', val].max()
    min = df.loc[df['species']=='setosa', val].min()

    return [
            html.Label('Moyenne : ' + str(moyenne)),
            html.Label('Variance : ' + str(variance)),
            html.Label('Max : ' + str(max) ),
            html.Label('Min : ' + str(min)),
            ]
#===================Affichage des infos sur versicolor ================
@app.callback(
    Output(component_id='stats_versicolor', component_property='children'),
    Input(component_id='liste_pour_versicolor', component_property='value')
)
def statsVersicolor(val):

    moyenne = round(df.loc[df['species']=='versicolor', val].mean(), 2)
    variance = round(df.loc[df['species']=='versicolor', val].std(), 2)
    max = df.loc[df['species']=='versicolor', val].max()
    min = df.loc[df['species']=='versicolor', val].min()

    return [
            html.Label('Moyenne : ' + str(moyenne)),
            html.Label('Variance : ' + str(variance)),
            html.Label('Max : ' + str(max) ),
            html.Label('Min : ' + str(min)),
            ]
#===================Affichage des infos sur virginica ================
@app.callback(
    Output(component_id='stats_virginica', component_property='children'),
    Input(component_id='liste_pour_virginica', component_property='value')
)
def statsVirginica(val):

    moyenne = round(df.loc[df['species']=='virginica', val].mean(), 2)
    variance = round(df.loc[df['species']=='virginica', val].std(), 2)
    max = df.loc[df['species']=='virginica', val].max()
    min = df.loc[df['species']=='virginica', val].min()

    return [
            html.Label('Moyenne : ' + str(moyenne)),
            html.Label('Variance : ' + str(variance)),
            html.Label('Max : ' + str(max) ),
            html.Label('Min : ' + str(min)),
            ]

app.title = 'Iris Dashboard'

if __name__=='__main__':
    app.run(debug=True)

# Templates disponibles : plotly, plotly_white, plotly_dark, ggplot2, seaborn, simple_white
#fig.update_layout(template='plotly_white')