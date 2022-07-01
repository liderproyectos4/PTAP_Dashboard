import dash
import dash_table
from dash import html
from dash import dcc
from dash import Dash, html, Input, Output, callback_context
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from datetime import datetime
import dash_daq as daq
# Importar hojas de trabajo de google drive     https://bit.ly/3uQfOvs
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

# This stylesheet makes the buttons and table pretty.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

badgeFecha = dbc.Button(
    [
        "Fecha:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeHoraInicial = dbc.Button(
    [
        "Hora Inicial:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeHoraFinal = dbc.Button(
    [
        "Hora Final:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeAlturaInicial = dbc.Button(
    [
        "Altura Inicial [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeAlturaFinal = dbc.Button(
    [
        "Altura Final [m]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeFase = dbc.Button(
    [
        "Fase:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

app.layout = dbc.Container([
    #html.Div([
    # The memory store reverts to the default on every page refresh
    dcc.Store(id='memory'),
    # The local store will take the initial data
    # only the first time the page is loaded
    # and keep it until it is cleared.
    dcc.Store(id='local', storage_type='local'),
    # Same as the local store but will lose the data
    # when the browser/tab closes.
    dcc.Store(id='session', storage_type='session'),
    html.Table([
        html.Thead([
            html.Tr(html.Th('Click to store in:', colSpan="3")),
            html.Tr([
                html.Th(html.Button('memory', id='memory-button')),
                html.Th(html.Button('localStorage', id='local-button')),
                html.Th(html.Button('sessionStorage', id='session-button'))
            ]),
            html.Tr([
                html.Th('Memory clicks'),
                html.Th('Local clicks'),
                html.Th('Session clicks')
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(0, id='memory-clicks'),
                html.Td(0, id='local-clicks'),
                html.Td(0, id='session-clicks')
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Bombeo de Lodos']), style={'color': '#082255', 'font-family': "Franklin Gothic"})
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeFecha
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='fecha-lodos',
                                    type='text',
                                    placeholder="DD/MM/AAAA",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=10,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=False,  # Require user to insert something into input box
                                    size="11",  # Number of characters that will be visible inside box

                                )
                            ]),
                        ]),
                        dbc.Col([
                            badgeFase
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='fase-lodos',
                                    type='number',
                                    placeholder="1 o 2 o 3",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=1, max=10, step=1,  # Ranges of numeric value. Step refers to increments
                                   minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=False,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box

                                )
                            ]),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeHoraInicial
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='hora-inicial-lodos',
                                    type='text',
                                    placeholder="HH:mm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=False,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box

                                )
                            ]),
                        ]),
                        dbc.Col([
                            badgeHoraFinal
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='hora-final-lodos',
                                    type='text',
                                    placeholder="HH:mm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    # min=2015, max=2019, step=1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=False,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box

                                )
                            ]),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            badgeAlturaInicial
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='altura-inicial-lodos',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=False,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box

                                )
                            ]),
                        ]),
                        dbc.Col([
                            badgeAlturaFinal
                        ]),
                        dbc.Col([
                            html.Div([
                                dcc.Input(
                                    id='altura-final-lodos',
                                    type='number',
                                    placeholder="m.cm",
                                    # A hint to the user of what can be entered in the control
                                    debounce=True,
                                    # Changes to input are sent to Dash server only on enter or losing focus
                                    min=0, max=3, step=0.1,  # Ranges of numeric value. Step refers to increments
                                    minLength=0, maxLength=5,  # Ranges for character length inside input box
                                    autoComplete='off',
                                    disabled=False,  # Disable input box
                                    readOnly=False,  # Make input box read only
                                    required=False,  # Require user to insert something into input box
                                    size="6",  # Number of characters that will be visible inside box

                                )
                            ]),
                        ]),

                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Button('Registrar', id='registro-lodos', n_clicks=0),
                        ]),
                    ]),
                    dbc.Row(
                        dash_table.DataTable(
                            id='datatable-interactivity-lodos',
                            columns=[
                                {"name": "Fecha", "id": 0, "deletable": False, "selectable": False, "hideable": False},
                                {"name": "Hora Inicial [m]", "id": 1, "deletable": False, "selectable": False,
                                 "hideable": False},
                                {"name": "Hora Final [m]", "id": 2, "deletable": False, "selectable": False,
                                 "hideable": False},
                                {"name": "Altura Inicial [m]", "id": 3, "deletable": False, "selectable": False,
                                 "hideable": False},
                                {"name": "Altura Final [m]", "id": 4, "deletable": False, "selectable": False,
                                 "hideable": False},
                                {"name": "Fase", "id": 5, "deletable": False, "selectable": False, "hideable": False},

                            ],
                            data=[],  # the contents of the table NO INICIALIZAR CON [] SINO CON EL ID!!!

                            editable=True,  # allow editing of data inside all cells
                            filter_action="none",  # allow filtering of data by user ('native') or not ('none')
                            sort_action="none",  # enables data to be sorted per-column by user or not ('none')
                            sort_mode="none",  # sort across 'multi' or 'single' columns
                            column_selectable="none",  # allow users to select 'multi' or 'single' columns
                            row_selectable="multi",  # allow users to select 'multi' or 'single' rows
                            row_deletable=True,  # choose if user can delete a row (True) or not (False)
                            selected_columns=[],  # ids of columns that user selects
                            selected_rows=[],  # indices of rows that user selects
                            page_action="native",  # all data is passed to the table up-front or not ('none')
                            page_current=0,  # page number that user is on
                            page_size=6,  # number of rows visible per page
                            style_cell={  # ensure adequate header width when text is shorter than cell's text
                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                            },
                            style_data={  # overflow cells' content into multiple lines
                                'whiteSpace': 'normal',
                                'height': 'auto'
                            }

                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            #html.Button('Enviar', id='enviar-lodos', n_clicks=0),
                            dcc.ConfirmDialogProvider(
                                children=html.Button('Enviar', ),
                                id='enviar-lodos',
                                message='¿Está seguro que desea enviar los datos de agua lodosa bombeada?'
                                        'No olvide borrar los datos después del envío.'
                            ),
                        ]),
                        dbc.Col([
                            dbc.Accordion([
                                dbc.AccordionItem(
                                    html.Button('Borrar', id='borrar-lodos', n_clicks=0), title="Borrar"
                                ),
                            ], start_collapsed=True),

                        ])

                    ]),
                    dbc.Row([
                        html.Div(id='Hola3', style={'font-family': "Franklin Gothic"})
                    ]),
                    dbc.Row([
                        html.Div(id='Hola4', style={'font-family': "Franklin Gothic"})
                    ]),

                ])
            ])
        ])
    ]),

    #])



])



# add a click to the appropriate store.
@app.callback(Output('session', 'data'),
              Input('session-button'.format('session'), 'n_clicks'),
              State('session', 'data'))
def on_click(n_clicks, data):
    if n_clicks is None:
        # prevent the None callbacks is important with the store component.
        # you don't want to update the store for nothing.
        raise PreventUpdate

    # Give a default data dict with 0 clicks if there's no data.
    data = data or {'clicks': 0}

    data['clicks'] = data['clicks'] + 1
    return data

# output the stored clicks in the table cell.
@app.callback(Output('session-clicks'.format('session'), 'children'),
              # Since we use the data prop in an output,
              # we cannot get the initial data on load with the data prop.
              # To counter this, you can use the modified_timestamp
              # as Input and the data as State.
              # This limitation is due to the initial None callbacks
              # https://github.com/plotly/dash-renderer/pull/81
              Input('session', 'modified_timestamp'),
              State('session', 'data'))
def on_data(ts, data):
    print(data)
    if ts is None:
        raise PreventUpdate

    data = data or {}

    return data.get('clicks', 0)


if __name__ == '__main__':
    app.run_server(debug=True, port=8077, threaded=True)