def navbar(pathname):
    return html.Div([
        dcc.Link(
            "Accueil",
            href="/",
            className="nav-item" + (" nav-item-active" if pathname == "/" else "")
        ),
        dcc.Link(
            "Dashboard",
            href="/dashboard",
            className="nav-item" + (" nav-item-active" if pathname == "/dashboard" else "")
        ),
    ], className="navbar")
