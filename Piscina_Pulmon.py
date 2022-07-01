import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from datetime import datetime
import dash_daq as daq
# Importar hojas de trabajo de google drive     https://bit.ly/3uQfOvs
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.css.append_css({'external_url': '/static/reset.css'})
app.server.static_folder = 'static'
server = app.server


app.layout = dbc.Container([
    dcc.Interval(
        id='my_interval',
        disabled=False,
        interval=1 * 1000,
        n_intervals=0,
        max_intervals=1
    ),
    dbc.Row([
        dbc.Col([dbc.CardImg(
            src="/assets/Logo.jpg",

            style={"width": "6rem",
                   'text-align': 'right'},
        ),

        ], align='right', width=2),
        dbc.Col(html.H5(
            '"Cualquier tecnología lo suficientemente avanzada, es indistinguible de la magia." - Arthur C. Clarke '),
                style={'color': "green", 'font-family': "Franklin Gothic"}, width=7),
        dbc.Col([dbc.CardImg(
            src="/assets/Logo-Ecopetrol.png",

            style={
                "width": "16rem",
                'text-align': 'left'},
        ),

        ], align='left', width=3),
    ]),
    dbc.Row([
        dbc.Col(html.H1(
            "Resumen del Sistema de Deshidratación de Lodos - Piscina Pulmón & SEP 3054 - Refinería de Barrancabermeja",
            style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"}), width=12, )
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Accordion([
                dbc.AccordionItem([
                    html.H5([
                                'El siguiente tablero interactivo presenta los resultados obtenidos por Geosoluciones SAS y Veolia al operar el sistema de deshidratación de lodos mediante la tecnología de Geotube para proveer el servicio de mantenimiento técnico de la Piscina Pulmón y separador SEP 3054 en la Gerencia Refinería de Barrancabermeja de Ecopetrol S. A., Ubicada en Barrancabermeja, Santander, Colombia.'])

                ], title="Introducción"),
            ], start_collapsed=True, style={'textAlign': 'left', 'color': '#082255', 'font-family': "Franklin Gothic"}),

        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
    ]),
    dbc.Row([
        dbc.Tabs(
            [
                dbc.Tab(dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Resumen Diario']), style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"})
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Seleccionar Unidades:",
                                id="selec-uni-dia-target",
                                color="info",
                                style={'font-family': "Franklin Gothic"},
                                # className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos.",
                                target="selec-uni-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),

                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[
                                    {"label": "Galones", "value": True},
                                    {"label": "Metros cúbicos", "value": False},
                                ],
                                value=True,
                                id="unidades-dia-input", style={'font-family': "Franklin Gothic"}
                            ),
                        ], xs=2, sm=2, md=2, lg=2, xl=2, ),
                        dbc.Col([
                            dbc.Button(
                                "Seleccionar Día:",
                                id="selec-dia-dia-target",
                                color="info",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el día introducido por el usuario para conocer el resumen de la operación para el día seleccionado. Formato DD/MM/AAAA.",
                                target="selec-dia-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            dcc.Dropdown(id='Dia',
                                         options=[],
                                         #value='4/2/2020',
                                         style={'font-family': "Franklin Gothic"}
                                         )
                        ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Programado:",
                                id="prog-dia-target",
                                color="secondary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la fracción del proyecto que se tiene programada para ser ejecutada en un día seleccionado.",
                                target="prog-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='prog-dia', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Ejecución:",
                                id="ejec-dia-target",
                                color="secondary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la fracción del proyecto que ha sido ejecutada para un día seleccionado.",
                                target="ejec-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='ejec-dia', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),

                        dbc.Col([
                            dbc.Row([daq.GraduatedBar(
                                id='barra-prct-dia',
                                color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6], "green": [6.6, 10]}},
                                showCurrentValue=True,
                                step=0.25,
                                value=0,
                                size=230,
                                style={'color': '#082255', 'font-family': "Franklin Gothic"}

                            )]),
                        ], xs=2, sm=2, md=2, lg=2, xl=2)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Desviación:",
                                id="desv-dia-target",
                                color="secondary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la magnitud de la diferencia entre el progreso y la ejecución.",
                                target="desv-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='var-dia', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Horómetro Motor:",
                                id="motor-dia-target",
                                color="success",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Muestra el tiempo que el motor de la draga ha estado encendido para un día seleccionado.",
                                target="motor-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='motor-dia', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Horómetro Cortador:",
                                id="cort-dia-target",
                                color="success",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Muestra el tiempo que el cortador de la draga ha estado encendido para un día seleccionado.",
                                target="cort-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='cort-dia', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Horómetro Bomba:",
                                id="bomba-dia-target",
                                color="success",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Muestra el tiempo que la bomba de la draga ha estado encendida para un día seleccionado.",
                                target="bomba-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='bomba-dia', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),

                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Volumen Bombeado:",
                                id="vol-bomb-dia-target",
                                color="primary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el volumen de agua lodosa que es bombeada de la piscina pulmón o el separador SEP 3054 al sistema de deshidratación mediante Geotube en un día seleccionado. Se calcula como el caudal de la bomba multiplicado el tiempo de operación (horómetro de la bomba).",
                                target="vol-bomb-dia-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col(
                        dbc.Spinner(children=[html.Div(id='aguaLDS-dia', style={'font-family': "Franklin Gothic"})], size="lg",
                                    color="primary", type="border", fullscreen=True, )
                        , xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),

                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Accordion([
                                dbc.AccordionItem([
                                    html.H5([
                                        'Barra de Ejecución: es el cociente entre la ejecución y lo programado. Rojo de 0-33%, amarillo de 33-66% y verde de 66-100%.']),
                                                                ], title="Descripción de Íconos"),
                                                            ], start_collapsed=True,
                                                                style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                                                        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                                                    ]),
                ])
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
        ], xs=3, sm=3, md=3, lg=2, xl=2, ),
    ]),



]), label="Resumen Diario", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                dbc.Tab(dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Resumen Total']),
                                    style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"})
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Seleccionar Unidades:",
                                id="selec-uni-acum-target",
                                color="info",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos",
                                target="selec-uni-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[
                                    {"label": "Galones", "value": True},
                                    {"label": "Metros cúbicos", "value": False},
                                ],
                                value=True,
                                id="unidades-acum-input",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], xs=3, sm=3, md=3, lg=2, xl=2, ),
                    dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    "Día Inicial:",
                                    id="dia-inicial-acum-target",
                                    color="primary",
                                    className="me-1",
                                    n_clicks=0,
                                    style={'font-family': "Franklin Gothic"},
                                ),
                                dbc.Popover(
                                    "Es el día de inicio de operación.",
                                    target="dia-inicial-acum-target",
                                    body=True,
                                    trigger="hover",
                                    style={'font-family': "Franklin Gothic"}
                                ),

                            ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col([
                                html.Div(id='dia-inicial-acum', style={'font-family': "Franklin Gothic"})
                            ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"),
                            dbc.Col([
                                dbc.Button(
                                    "Día Final:",
                                    id="dia-final-acum-target",
                                    color="primary",
                                    className="me-1",
                                    n_clicks=0,
                                    style={'font-family': "Franklin Gothic"},
                                ),
                                dbc.Popover(
                                    "Es el último día operado hasta la fecha.",
                                    target="dia-final-acum-target",
                                    body=True,
                                    trigger="hover",
                                    style={'font-family': "Franklin Gothic"}
                                ),

                            ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col([
                                html.Div(id='dia-final-acum', style={'font-family': "Franklin Gothic"})
                            ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Programado:",
                                id="prog-acum-target",
                                color="secondary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la fracción del proyecto que se tiene programada para ser ejecutada hasta la fecha.",
                                target="prog-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='prog-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Ejecución:",
                                id="ejec-acum-target",
                                color="secondary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la fracción del proyecto que ha sido ejecutada hasta la fecha.",
                                target="ejec-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='ejec-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),

                        dbc.Col([
                            dbc.Row([daq.GraduatedBar(
                                id='barra-prct-acum',
                                color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6], "green": [6.6, 10]}},
                                showCurrentValue=True,
                                step=0.25,
                                value=0,
                                size=220,
                                style={'color': '#082255', 'font-family': "Franklin Gothic"}

                            )]),
                        ], width=2)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Desviación:",
                                id="desv-acum-target",
                                color="secondary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la magnitud de la diferencia entre el progreso y la ejecución.",
                                target="desv-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='var-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Horómetro Motor:",
                                id="motor-acum-target",
                                color="success",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el tiempo que el motor de la draga ha estado encendido en todo el proyecto.",
                                target="motor-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='motor-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),

                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Horómetro Cortador:",
                                id="cort-acum-target",
                                color="success",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el tiempo que el cortador de la draga ha estado encendido durante todo el proyecto.",
                                target="cort-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='cort-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Horómetro Bomba:",
                                id="bomb-acum-target",
                                color="success",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el tiempo que la bomba de la draga ha estado encendida durante todo el proyecto.",
                                target="bomb-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='bomba-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                            ]),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Frac. Hidrocarburo:",
                                id="HC-acum-target",
                                color="dark",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la fracción másica de hidrocarburo de los lodos deshidratados en el interior del Geotube. Se calcula como el promedio de la última medición de retorta de todos los Geotubes.",
                                target="HC-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='HC-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Frac. Sólidos:",
                                id="soli-acum-target",
                                color="dark",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la fracción másica de sólidos totales de los lodos deshidratados en el interior del Geotube. Se calcula como el promedio de la última medición de retorta de todos los Geotubes.",
                                target="soli-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='sol-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),

                    ]),

                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Días Operados:",
                                id="dias-acum-target",
                                color="primary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la cantidad de días operados durante el proyecto.",
                                target="dias-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='dias-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Humedad:",
                                id="hume-acum-target",
                                color="primary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la fracción másica de agua de los lodos deshidratados en el interior del Geotube. Se calcula como el promedio de la última medición de retorta de todos los Geotubes.",
                                target="hume-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='agua-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Row([daq.GraduatedBar(
                                id='barra-agua-acum',
                                color={"ranges": {"green": [0, 8.5], "yellow": [8.5, 9.25], "red": [9.25, 10]}},
                                showCurrentValue=False,
                                step=0.25,
                                value=0,
                                size=220,
                                style={'color': '#082255', 'font-family': "Franklin Gothic"}

                            )]),
                        ], width=2)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Volumen Bombeado:",
                                id="vol-bomb-acum-target",
                                color="primary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el volumen de agua lodosa que es bombeada de la piscina pulmón o el separador SEP 3054 al sistema de deshidratación mediante Geotube en todo el proyecto. Se calcula como el caudal de la bomba multiplicado el tiempo de operación (horómetro de la bomba).",
                                target="vol-bomb-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='vol-bomb-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Button(
                                "Peso de Lodos Extraídos:",
                                id="lodos-acum-target",
                                color="dark",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la suma del peso de todos los lodos deshidratados en el interior de los Geotubes.",
                                target="lodos-acum-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                        dbc.Col([
                            html.Div(id='peso-GT-acum', style={'font-family': "Franklin Gothic"})
                        ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),
                        dbc.Col([
                            dbc.Row([daq.GraduatedBar(
                                id='barra-LDS-acum',
                                color={"ranges": {"green": [0, 4.2], "yellow": [4.2, 8.33], "red": [8.33, 10]}},
                                showCurrentValue=True,
                                step=0.25,
                                value=0,
                                size=220,
                                style={'color': '#082255', 'font-family': "Franklin Gothic"}

                            )]),
                        ], width=2)
                    ]),
                    dbc.Row(dbc.Col(
                        dbc.Spinner(children=[dcc.Graph(id="fig-curva-S")], size="lg",
                                    color="primary", type="border", fullscreen=True, ),
                        width={'size': 12, 'offset': 0}),
                    ),
                    dbc.Row(dbc.Col(
                        dbc.Spinner(children=[dcc.Graph(id="fig-horómetro")], size="lg",
                                    color="primary", type="border", fullscreen=True, ),
                        width={'size': 12, 'offset': 0}),
                    ),
                    dbc.Row([
                        dbc.Col([
                            dbc.Accordion([
                                dbc.AccordionItem([

                                    html.H5([
                                        'Barra de Ejecución: es el cociente entre la ejecución y lo programado. Rojo de 0-33%, amarillo de 33-66% y verde de 66-100%.']),

                                    html.H5([
                                        ' Barra de Humedad: representa la humedad objetivo para retirar los lodos del Geotube. Color verde de 0-55% de humedad, color amarillo de 55-60% de humedad y color rojo de 60-65% de humedad.']),

                                    html.H5([
                                        'Barra de Peso de Lodos Extraídos: representa el objetivo (hasta 3600 ton) de lodos a extraer en toda la operación. Color rojo de 0-1500 ton, color amarillo de 1500-3000 ton y color verde de 3000-3600 ton.']),


                                ], title="Descripción de Íconos"),
                            ], start_collapsed=True,
                                style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                    ]),
                ])
            ])
        ])
    ]), label="Resumen Total", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                dbc.Tab(dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Resumen Geotube']),
                                style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"})
                            ]),
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Seleccionar Unidades:",
                                id="unidades-GT-target",
                                color="info",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Son las unidades de volumen que son seleccionadas por el usuario. Se tiene como opciones galones y metros cúbicos",
                                target="unidades-GT-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col(dbc.RadioItems(
                                options=[
                                    {"label": "Galones", "value": True},
                                    {"label": "Metros cúbicos", "value": False},
                                ],
                                value=True,
                                id="unidades-GT-input",
                                style={'font-family': "Franklin Gothic"}
                            ), xs=2, sm=2, md=2, lg=2, xl=2,),
                        dbc.Col([
                            dbc.Button(
                                "Número:",
                                id="numero-GT-target",
                                color="info",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el número del Geotube ingresado por el usuario.",
                                target="numero-GT-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col([
                                dcc.Dropdown(id='numGTDD',
                                             options=[],
                                             #value='1',
                                             style={'font-family': "Franklin Gothic"}
                                             )
                            ], xs=1, sm=1, md=1, lg=2, xl=2, ),
                        dbc.Col([
                            dbc.Button(
                                "Seleccionar Día:",
                                id="dia-GT-target",
                                color="info",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el día introducido por el usuario para conocer el resumen de la operación del Geotube para el día seleccionado. Formato DD/MM/AAAA.",
                                target="dia-GT-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col([
                                dcc.Dropdown(id='fechaGTDD',
                                             options=[],
                                             style={'font-family': "Franklin Gothic"}
                                             )
                            ], xs=3, sm=3, md=3, lg=2, xl=2,),

                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Capacidad:",
                                id="cap-GT-target",
                                color="primary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es la capacidad máxima del Geotube seleccionado.",
                                target="cap-GT-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col(html.Div(id='cap-GT'), xs=6, sm=6, md=6, lg=5, xl=5, style={'font-family': "Franklin Gothic"}),
                            dbc.Col(daq.Tank(   id="tanque-GT",
                                                height=75,
                                                width=400,
                                                value=0,
                                                min=0,
                                                max=100,
                                                color="brown",
                                                showCurrentValue=True,
                                                units="%",
                                                #style={'margin-left': '50px'},
                                                style={'color': '#082255', 'font-family': "Franklin Gothic", 'margin-left': '50px'}
                                            ), xs=4, sm=4, md=4, lg=4, xl=4,)
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Volumen:",
                                id="vol-GT-target",
                                color="primary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el volumen del Geotube para el día seleccionado.",
                                target="vol-GT-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col(html.Div(id='vol-GT'), xs=3, sm=3, md=3, lg=2, xl=2, style={'font-family': "Franklin Gothic"}),
                            dbc.Col([
                                dbc.Row([daq.GraduatedBar(
                                    id='barra-vol-GT',
                                    color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6], "green": [6.6, 10]}},
                                    showCurrentValue=False,
                                    step=0.2,
                                    value=0,
                                    style={'color': '#082255', 'font-family': "Franklin Gothic"}

                                )]),
                            ], width=2)
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                                "Peso:",
                                id="peso-GT-target",
                                color="primary",
                                style={'font-family': "Franklin Gothic"},
                                className="me-1",
                                n_clicks=0,
                            ),
                            dbc.Popover(
                                "Es el peso del Geotube para el día seleccionado.",
                                target="peso-GT-target",
                                body=True,
                                trigger="hover",
                                style={'font-family': "Franklin Gothic"}
                            ),
                        ], width=2, align='center', className="d-grid gap-2"),
                            dbc.Col(html.Div(id='peso-GT'), xs=3, sm=3, md=3, lg=2, xl=2, style={'font-family': "Franklin Gothic"}),
                            dbc.Col([
                                dbc.Row([daq.GraduatedBar(
                                    id='barra-peso-GT',
                                    color={"ranges": {"red": [0, 3.3], "yellow": [3.3, 6.6], "green": [6.6, 10]}},
                                    showCurrentValue=False,
                                    step=0.2,
                                    value=0,
                                    style={'color': '#082255', 'font-family': "Franklin Gothic"}

                                )]),
                            ], width=2)
                                        ]),
                    dbc.Row(dbc.Col(
                        dbc.Spinner(children=[dcc.Graph(id="fig-peso-vol")], size="lg",
                                    color="primary", type="border", fullscreen=True, ),
                        width={'size': 12, 'offset': 0}),
                    ),
                    dbc.Row(dbc.Col(
                        dbc.Spinner(children=[dcc.Graph(id="fig-agua-LDS")], size="lg",
                                    color="primary", type="border", fullscreen=True, ),
                        width={'size': 12, 'offset': 0}),
                    ),
                    dbc.Row(dbc.Col(
                        dbc.Spinner(children=[dcc.Graph(id="fig-retorta")], size="lg",
                                    color="primary", type="border", fullscreen=True, ),
                        width={'size': 12, 'offset': 0}),
                    ),
                    dbc.Row([
                        dbc.Col([
                            dbc.Accordion([
                                dbc.AccordionItem([

                                    html.H5([
                                        ' Barra volumen: es la fracción del volumen máximo de llenado del Geotube. Rojo de 0-33%, amarillo de 33-66% y verde de 66-100%.']),

                                    html.H5([
                                        ' Barra peso: es la fracción del peso máximo del Geotube. Rojo de 0-33%, amarillo de 33-66% y verde de 66-100%.']),

                                    html.H5([
                                        'Geotube con Porcentaje: es el porcentaje de llenado del Geotube para el día seleccionado.']),


                                ], title="Descripción de Íconos"),
                            ], start_collapsed=True,
                                style={'color': '#082255', 'font-family': "Franklin Gothic"}),

                        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
                    ]),
                ])
            ])
        ])
    ]), label="Resumen Geotube", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),

            ])
    ]),
])


@app.callback(
    Output(component_id='numGTDD', component_property='options'),
    Output(component_id='Dia', component_property='options'),
    Output(component_id='Dia', component_property='value'),
    Output(component_id='numGTDD', component_property='value'),
    Output(component_id='dia-inicial-acum', component_property='children'),
    Output(component_id='dia-final-acum', component_property='children'),

    Input('my_interval', 'n_intervals'),
)

def dropdownTiempoReal(value_intervals):
    SERVICE_ACCOUNT_FILE = 'keys_piscina_pulmon.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1p64dwGH2PdE6ncILajAd95C3P-rzdVCWtEVyVn4wSwQ'

    SAMPLE_RANGE_COMBINADO = "Principal"

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_COMBINADO = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                          range=SAMPLE_RANGE_COMBINADO).execute()

    dfCOMBINADO = result_COMBINADO.get('values', [])
    names = ["Fecha", "Programado", "Ejecutado", "", "", "", "Geotube", "Fecha", "Tiempo de operación [hr]",
             "Horómetro",
             "Caudal [GPM]", "", "", "", "Geotube", "Fecha", "Hora", "Volumen [m3]", "Uso", "Peso [ton]", "Capacidad [m3]",
             "", "", "", "Geotube", "Fecha", "Frac Agua", "Frac HC", "Frac sólidos", "pH"]
    dfCOMBINADO = pd.DataFrame(dfCOMBINADO, columns=names)
    dfCOMBINADO.drop([0], inplace=True)
    dfCOMBINADO = dfCOMBINADO.rename(index=lambda x: x - 1)

    dfCurvaS = dfCOMBINADO.iloc[:, [0, 1, 2]]
    dfDragado = dfCOMBINADO.iloc[:, [6, 7, 8, 9, 10]]
    dfGeotube = dfCOMBINADO.iloc[:, [14, 15, 16, 17, 18, 19, 20]]
    dfRetorta = dfCOMBINADO.iloc[:, [24, 25, 26, 27, 28, 29]]

    dfCurvaS = dfCurvaS.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfDragado = dfDragado.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfGeotube = dfGeotube.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfRetorta = dfRetorta.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")

    dfCurvaS = dfCurvaS.replace(to_replace='', value=np.nan).dropna(axis=0, how="any")

    numGT = dfGeotube["Geotube"]
    numGT = list(map(lambda x: float(x), numGT))
    numGT = list(dict.fromkeys(numGT))
    numGT.sort(reverse=True)

    dia = dfCurvaS["Fecha"]
    dia = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), dia))
    dia = list(dict.fromkeys(dia))
    dia.sort(reverse=True)
    dia = list(map(lambda fecha: str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year), dia))

    # Calcula primer día operado
    diaPrimer = dia[-1]

    # Calcula último día operado
    diaHoy = dia[0]

    # Devuelve último geotube utilizado
    GTHoy = numGT[0]



    return numGT, dia, diaHoy, GTHoy, diaPrimer, diaHoy


@app.callback(
    Output('fechaGTDD', 'options'),
    Input(component_id='numGTDD', component_property='value'),
)
def Num_Geotube_interactivo(value_numGT):
    SERVICE_ACCOUNT_FILE = 'keys_piscina_pulmon.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1p64dwGH2PdE6ncILajAd95C3P-rzdVCWtEVyVn4wSwQ'

    SAMPLE_RANGE_COMBINADO = "Principal"

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_COMBINADO = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                          range=SAMPLE_RANGE_COMBINADO).execute()

    dfCOMBINADO = result_COMBINADO.get('values', [])
    names = ["Fecha", "Programado", "Ejecutado", "", "", "", "Geotube", "Fecha", "Tiempo de operación [hr]",
             "Horómetro",
             "Caudal [GPM]", "", "", "", "Geotube", "Fecha", "Hora", "Volumen [m3]", "Uso", "Peso [ton]",
             "Capacidad [m3]",
             "", "", "", "Geotube", "Fecha", "Frac Agua", "Frac HC", "Frac sólidos", "pH"]
    dfCOMBINADO = pd.DataFrame(dfCOMBINADO, columns=names)
    dfCOMBINADO.drop([0], inplace=True)
    dfCOMBINADO = dfCOMBINADO.rename(index=lambda x: x - 1)

    dfCurvaS = dfCOMBINADO.iloc[:, [0, 1, 2]]
    dfDragado = dfCOMBINADO.iloc[:, [6, 7, 8, 9, 10]]
    dfGeotube = dfCOMBINADO.iloc[:, [14, 15, 16, 17, 18, 19, 20]]
    dfRetorta = dfCOMBINADO.iloc[:, [24, 25, 26, 27, 28, 29]]

    dfCurvaS = dfCurvaS.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfDragado = dfDragado.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfGeotube = dfGeotube.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfRetorta = dfRetorta.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")

    dff = dfGeotube[dfGeotube["Geotube"] == str(value_numGT)]
    dff = dff["Fecha"]
    dff = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), dff))
    dff = list(dict.fromkeys(dff))
    dff.sort(reverse=True)
    dff = list(map(lambda fecha: str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year), dff))

    return [{'label': c, 'value': c} for c in dff]


@app.callback(
    Output('fechaGTDD', 'value'),
    Input('fechaGTDD', 'options'),
)
def set_Geotube_fecha_value(fecha_selec):
    x = fecha_selec[0]
    x = x["value"]
    return x

@app.callback(
    Output(component_id='fig-curva-S', component_property="figure"),
    Output(component_id='fig-retorta', component_property="figure"),
    Output(component_id='fig-horómetro', component_property="figure"),
    Output(component_id='fig-peso-vol', component_property="figure"),
    Output(component_id='fig-agua-LDS', component_property="figure"),
    Output(component_id='prog-dia', component_property='children'),
    Output(component_id='ejec-dia', component_property='children'),
    Output(component_id='var-dia', component_property='children'),
    Output(component_id='cort-dia', component_property='children'),
    Output(component_id='motor-dia', component_property='children'),
    Output(component_id='bomba-dia', component_property='children'),
    Output(component_id='aguaLDS-dia', component_property='children'),
    Output(component_id='prog-acum', component_property='children'),
    Output(component_id='ejec-acum', component_property='children'),
    Output(component_id='var-acum', component_property='children'),
    Output(component_id='cort-acum', component_property='children'),
    Output(component_id='motor-acum', component_property='children'),
    Output(component_id='bomba-acum', component_property='children'),
    Output(component_id='agua-acum', component_property='children'),
    Output(component_id='HC-acum', component_property='children'),
    Output(component_id='sol-acum', component_property='children'),
    Output(component_id='dias-acum', component_property='children'),
    Output(component_id='vol-bomb-acum', component_property='children'),
    Output(component_id='peso-GT-acum', component_property='children'),
    Output(component_id='cap-GT', component_property='children'),
    Output(component_id='vol-GT', component_property='children'),
    Output(component_id='peso-GT', component_property='children'),
    Output(component_id='tanque-GT', component_property='value'),
    Output(component_id='barra-prct-dia', component_property="value"),
    Output(component_id='barra-prct-acum', component_property="value"),
    Output(component_id='barra-agua-acum', component_property="value"),
    Output(component_id='barra-LDS-acum', component_property="value"),
    Output(component_id='barra-vol-GT', component_property="value"),
    Output(component_id='barra-peso-GT', component_property="value"),

    Input('my_interval', 'n_intervals'),
    Input('numGTDD', 'value'),
    Input('Dia', 'value'),
    Input('fechaGTDD', 'value'),
    Input('unidades-dia-input', 'value'),
    Input('unidades-acum-input', 'value'),
    Input('unidades-GT-input', 'value'),
)

def pulmon(value_intervals, value_numGT, value_dia, value_fechaGT, value_unidades_dia, value_unidades_acum, value_unidades_GT):
    SERVICE_ACCOUNT_FILE = 'keys_piscina_pulmon.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1p64dwGH2PdE6ncILajAd95C3P-rzdVCWtEVyVn4wSwQ'

    SAMPLE_RANGE_COMBINADO = "Principal"

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_COMBINADO = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                          range=SAMPLE_RANGE_COMBINADO).execute()

    dfCOMBINADO = result_COMBINADO.get('values', [])
    names = ["Fecha", "Programado", "Ejecutado", "", "", "", "Geotube", "Fecha", "Tiempo de operación [hr]",
             "Horómetro",
             "Caudal [GPM]", "", "", "", "Geotube", "Fecha", "Hora", "Volumen [m3]", "Uso", "Peso [ton]", "Capacidad [m3]",
             "", "", "", "Geotube", "Fecha", "Frac Agua", "Frac HC", "Frac sólidos", "pH"]
    dfCOMBINADO = pd.DataFrame(dfCOMBINADO, columns=names)
    dfCOMBINADO.drop([0], inplace=True)
    dfCOMBINADO = dfCOMBINADO.rename(index=lambda x: x - 1)

    dfCurvaS = dfCOMBINADO.iloc[:, [0, 1, 2]]
    dfDragado = dfCOMBINADO.iloc[:, [6, 7, 8, 9, 10]]
    dfGeotube = dfCOMBINADO.iloc[:, [14, 15, 16, 17, 18, 19, 20]]
    dfRetorta = dfCOMBINADO.iloc[:, [24, 25, 26, 27, 28, 29]]

    dfCurvaS = dfCurvaS.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfDragado = dfDragado.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfGeotube = dfGeotube.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")
    dfRetorta = dfRetorta.replace(to_replace='None', value=np.nan).dropna(axis=0, how="all")

    ############################### Resumen Diario ##########################################################
    #print(value_unidades_dia)
    # gal = true
    # m3 = false
    unidades_dia = ' gal'


    # Calcula el progreso, ejecución y variación del tiempo en el día
    dia = value_dia
    dfCurvaS = dfCurvaS.replace(to_replace='', value=np.nan).dropna(axis=0, how="any")
    dfCurvaSdia = dfCurvaS[dfCurvaS["Fecha"] == dia]
    progDia = round(float(dfCurvaSdia["Programado"])*100, 2)
    ejecDia = round(float(dfCurvaSdia["Ejecutado"])*100, 2)
    prctDia = ejecDia / progDia * 100

    varDia = round(abs(float(progDia) - float(ejecDia)), 2)

    progDia = str(progDia) + ' %'
    ejecDia = str(ejecDia) + ' %'
    varDia = str(varDia) + ' %'


    # Obtiene horómetro de motor, cortador y bomba en un día
    a = set(dfCurvaS["Fecha"])
    b = set(dfDragado["Fecha"])
    prueba = a ^ (a&b)

    if (value_dia not in prueba) == True:
        boool = True
        dfDragadoDia = dfDragado[dfDragado["Fecha"] == dia]
        horoCortDia = dfDragadoDia[dfDragadoDia["Horómetro"] == "Cortador"]
        horoMotorDia = dfDragadoDia[dfDragadoDia["Horómetro"] == "Motor"]
        horoBombaDia = dfDragadoDia[dfDragadoDia["Horómetro"] == "Bomba"]

        horoCortDia = horoCortDia["Tiempo de operación [hr]"]
        horoMotorDia = horoMotorDia["Tiempo de operación [hr]"]
        horoBombaDia = horoBombaDia["Tiempo de operación [hr]"]

        horoCortDia = horoCortDia.rename(index=lambda z: 0)
        horoMotorDia = horoMotorDia.rename(index=lambda z: 0)
        horoBombaDia = horoBombaDia.rename(index=lambda z: 0)

        horoCortDia = str(horoCortDia[0]) + ' hr.'
        horoMotorDia = str(horoMotorDia[0]) + ' hr.'
        horoBombaDia = str(horoBombaDia[0]) + ' hr.'

        # Calcula volumen de agua lodosa en un día
        dfDragadoDia = dfDragado[(dfDragado["Fecha"] == dia) & (dfDragado["Horómetro"] == "Bomba")]
        Qdia = dfDragadoDia["Caudal [GPM]"]
        Tdia = dfDragadoDia["Tiempo de operación [hr]"]
        aguaLDSdia = round(float(Qdia) * float(Tdia) * 60, 0)

        if value_unidades_dia == True:
            aguaLDSdia = str(int(aguaLDSdia)) + unidades_dia
        else:
            unidades_dia = ' m3'
            aguaLDSdia = round(float(Qdia) * float(Tdia) * 60 / 264.172, 0)
            aguaLDSdia = str(int(aguaLDSdia)) + unidades_dia
    else:
        boool = False
        horoCortDia = 'N.R.'
        horoMotorDia = 'N.R.'
        horoBombaDia = 'N.R.'
        aguaLDSdia = 'N.R.'



    ############################### Resumen Acumulado ########################################################
    unidades_acum = ' gal'

    # Cálculo porcentaje programado, ejecutado y varianza acumulado
    dfCurvaS = dfCurvaS.replace(to_replace='', value=np.nan).dropna(axis=0, how="all")

    progAcum = dfCurvaS["Programado"]
    ejecAcum = dfCurvaS["Ejecutado"]
    ejecAcum = ejecAcum.dropna(axis=0, how="all")

    progAcum = round(float(progAcum[len(progAcum)-1])*100, 2)
    ejecAcum = round(float(ejecAcum[len(ejecAcum) - 1])*100, 2)
    varAcum = round(abs(progAcum-ejecAcum), 2)
    prctAcum = ejecAcum

    progAcum = str(progAcum) + ' %'
    ejecAcum = str(ejecAcum) + ' %'
    varAcum = str(varAcum) + ' %'

    # Cálculo horas acumuladas de motor, cortador y bomba acumulado
    cortAcum = dfDragado[dfDragado["Horómetro"] == "Cortador"]
    cortAcum = cortAcum["Tiempo de operación [hr]"]
    cortAcum = sum(list(map(lambda x: float(x), cortAcum)))
    cortAcum = str(cortAcum) + ' hr.'

    motorAcum = dfDragado[dfDragado["Horómetro"] == "Motor"]
    motorAcum = motorAcum["Tiempo de operación [hr]"]
    motorAcum = sum(list(map(lambda x: float(x), motorAcum)))
    motorAcum = str(motorAcum) + ' hr.'

    bombaAcum = dfDragado[dfDragado["Horómetro"] == "Bomba"]
    bombaAcum = bombaAcum["Tiempo de operación [hr]"]
    bombaAcum = sum(list(map(lambda x: float(x), bombaAcum)))
    bombaAcum = str(bombaAcum) + ' hr.'

    # Cálculo promedio de frac. HC, frac. agua, frac. sólidos acumulado
    numGT9 = dfGeotube["Geotube"]
    numGT9 = list(map(lambda x: float(x), numGT9))
    numGT9 = list(dict.fromkeys(numGT9))

    print(numGT9)
    print(dfRetorta)
    aguaAcum0 = 0
    HCAcum0 = 0
    solAcum0 = 0
    for i in numGT9:
        dfRetGT = dfRetorta[dfRetorta["Geotube"] == str(int(i))]
        aguaAcum00 = np.array(dfRetGT["Frac Agua"])
        aguaAcum0 = float(aguaAcum00[-1]) + aguaAcum0

        HCAcum00 = np.array(dfRetGT["Frac HC"])
        HCAcum0 = float(HCAcum00[-1]) + HCAcum0

        solAcum00 = np.array(dfRetGT["Frac sólidos"])
        solAcum0 = float(solAcum00[-1]) + solAcum0


    aguaAcum = round(aguaAcum0/len(numGT9)*100, 2)
    HCAcum = round(HCAcum0 / len(numGT9)*100, 2)
    solAcum = round(solAcum0 / len(numGT9)*100, 2)
    print(aguaAcum)
    #aguaAcum = dfRetorta["Frac Agua"]
    #aguaAcum = list(map(lambda x: float(x), aguaAcum))
    #aguaAcum = round(sum(aguaAcum)*100/len(aguaAcum), 2)

    aguaAcum = str(aguaAcum) + ' %'

    #HCAcum = dfRetorta["Frac HC"]
    #HCAcum = list(map(lambda x: float(x), HCAcum))
    #HCAcum = round(sum(HCAcum) * 100 / len(HCAcum), 2)
    HCAcum = str(HCAcum) + ' %'

    #solAcum = dfRetorta["Frac sólidos"]
    #solAcum = list(map(lambda x: float(x), solAcum))
    #solAcum = round(sum(solAcum) * 100 / len(solAcum), 2)
    solAcum = str(solAcum) + ' %'

    # Cálculo días operados acumulado
    dfCurvaS2 = dfCurvaS.dropna(axis=0, how="any")
    fechaDiaOper = dfCurvaS2["Fecha"]
    diasOper = len(fechaDiaOper)
    diasOper = str(diasOper) + ' días'

    # Cálculo volumen bombeado a Geotube
    dfBomba = dfDragado[dfDragado["Horómetro"] == "Bomba"]
    tiempoBomba = dfBomba["Tiempo de operación [hr]"]
    caudalBomba = dfBomba["Caudal [GPM]"]

    tiempoBomba = list(map(lambda x: float(x), tiempoBomba))
    caudalBomba = list(map(lambda x: float(x), caudalBomba))
    volBombGT = np.array(tiempoBomba) * np.array(caudalBomba) * 60
    #volBombGT = round(sum(volBombGT), 0)
    #volBombGT = str(volBombGT) + ' gal'

    if value_unidades_acum == True:
        volBombGT = int(round(sum(volBombGT), 0))
        volBombGT = str(volBombGT) + unidades_acum
    else:
        unidades_acum = ' m3'
        volBombGT = np.array(tiempoBomba) * np.array(caudalBomba) * 60 / 264.172
        volBombGT = int(round(sum(volBombGT), 0))
        volBombGT = str(volBombGT) + unidades_acum

    # Cálculo peso de lodos extraídos
    numGTvec = list(dict.fromkeys(dfGeotube["Geotube"]))


    pesoLDSextAcum = 0
    for i in numGTvec:
        dfPeso = dfGeotube[dfGeotube["Geotube"] == i]
        pesoLDSext = np.array(dfPeso["Peso [ton]"])
        pesoLDSext = pesoLDSext[-1]
        pesoLDSextAcum = pesoLDSextAcum + float(pesoLDSext)

    pesoLDSextAcum9 = pesoLDSextAcum
    pesoLDSextAcum = str(round(pesoLDSextAcum, 0)) + ' ton'

    ############################### Resumen Geotube ########################################################

    dfResGT = dfGeotube[dfGeotube["Fecha"] == value_fechaGT]
    capGTRes = np.array(dfResGT["Capacidad [m3]"])


    volGTRes = np.array(dfResGT["Volumen [m3]"])


    pesoGTRes = np.array(dfResGT["Peso [ton]"])
    pesoGTRes = int(round(float(pesoGTRes[0]), 0))
    pesoGTRes = str(pesoGTRes) + ' ton'


    if value_unidades_GT == True:
        capGTRes = round(float(capGTRes[-1])*264.172, 0)
        volGTRes = round(float(volGTRes[0]) * 264.172, 0)
        prctUso = volGTRes / capGTRes * 100


        capGTRes = str(capGTRes) + ' gal'
        volGTRes = str(volGTRes) + ' gal'

    else:
        capGTRes = round(float(capGTRes[-1]), 0)
        volGTRes = round(float(volGTRes[0]), 0)
        prctUso = volGTRes / capGTRes * 100

        capGTRes = str(capGTRes) + ' m3'
        volGTRes = str(volGTRes) + ' m3'





    ############################### Gráfico Curva S ##########################################################


    dfCurvaS = dfCurvaS.replace(to_replace='', value=np.nan).dropna(axis=0, how="all")


    fechaCurvS = dfCurvaS["Fecha"]
    programado = dfCurvaS["Programado"]
    ejecutado = dfCurvaS["Ejecutado"]

    fechaCurvS = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaCurvS))
    programado = list(map(lambda x: float(x) * 100, programado))
    ejecutado = list(map(lambda x: float(x) * 100, ejecutado))

    #style={'font-family': "Franklin Gothic"}
    # Crea la figura de curva S
    figcurvS = go.Figure()

    figcurvS.add_trace(go.Scatter(x=fechaCurvS, y=programado, name="Tiempo programado [%]"))
    figcurvS.add_trace(go.Scatter(x=fechaCurvS, y=ejecutado, name="Tiempo ejecutado [%]"))
    figcurvS.update_layout(title="Curva S", xaxis_title="Fecha",
                        yaxis_title="")
    figcurvS.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5,
    ))

    figcurvS.update_layout(
        font_family="Franklin Gothic",
        #font_color="blue",
        title_font_family="Franklin Gothic",
        #title_font_color="red",
        #legend_title_font_color="green"
    )
    figcurvS.update_xaxes(title_font_family="Franklin Gothic")



    ############################### Gráfico Retorta ##############################################
    numGT = value_numGT
    numGT = str(numGT)

    retortaGT = dfRetorta[dfRetorta["Geotube"] == numGT]

    fechaRet = retortaGT["Fecha"]
    aguaRet = retortaGT["Frac Agua"]
    HCRet = retortaGT["Frac HC"]
    solidosRet = retortaGT["Frac sólidos"]
    pHRet = retortaGT["pH"]

    fechaRet = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaRet))
    aguaRet = list(map(lambda x: float(x) * 100, aguaRet))
    HCRet = list(map(lambda x: float(x) * 100, HCRet))
    solidosRet = list(map(lambda x: float(x) * 100, solidosRet))
    pHRet = list(map(lambda x: float(x) * 100, pHRet))


    # Crea la figura de retorta
    figRetorta = go.Figure()

    figRetorta.add_trace(go.Scatter(x=fechaRet, y=aguaRet, name="Fracción de agua [%]"))
    figRetorta.add_trace(go.Scatter(x=fechaRet, y=HCRet, name="Fracción de hidrocarburo [%]"))
    figRetorta.add_trace(go.Scatter(x=fechaRet, y=solidosRet, name="Fracción de sólidos [%]"))
    figRetorta.update_layout(title="Análisis de Retorta", xaxis_title="Fecha",
                        yaxis_title="")
    figRetorta.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.7,
        xanchor="center",
        x=0.5
    ))

    figRetorta.update_layout(
        font_family="Franklin Gothic",
        #font_color="blue",
        title_font_family="Franklin Gothic",
        #title_font_color="red",
        #legend_title_font_color="green"
    )
    figRetorta.update_xaxes(title_font_family="Franklin Gothic")

    ############################### Gráfico Horómetro ##############################################

    dragadoGT = dfDragado[dfDragado["Geotube"] == numGT]

    cort = dragadoGT[dragadoGT["Horómetro"] == "Cortador"]
    horasCort = cort["Tiempo de operación [hr]"]
    fechaHorasCort = cort["Fecha"]

    motor = dragadoGT[dragadoGT["Horómetro"] == "Motor"]
    horasMotor = motor["Tiempo de operación [hr]"]
    fechaHorasMotor = motor["Fecha"]

    bomba = dragadoGT[dragadoGT["Horómetro"] == "Bomba"]
    horasBomba = bomba["Tiempo de operación [hr]"]
    fechaHorasBomba = bomba["Fecha"]

    fechaHorasCort = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaHorasCort))
    fechaHorasMotor = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaHorasMotor))
    fechaHorasBomba = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), fechaHorasBomba))
    horasCort = list(map(lambda x: float(x), horasCort))
    horasMotor = list(map(lambda x: float(x), horasMotor))
    horasBomba = list(map(lambda x: float(x), horasBomba))


    # Crea la figura de horómetro
    figHorometro = go.Figure()

    figHorometro.add_trace(go.Scatter(x=fechaHorasCort, y=horasCort, name="Cortador"))
    figHorometro.add_trace(go.Scatter(x=fechaHorasMotor, y=horasMotor, name="Motor"))
    figHorometro.add_trace(go.Scatter(x=fechaHorasBomba, y=horasBomba, name="Bomba"))
    figHorometro.update_layout(title="Horómetro", xaxis_title="Fecha",
                        yaxis_title="Tiempo [hr.]")
    figHorometro.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.7,
        xanchor="center",
        x=0.5
    ))

    figHorometro.update_layout(
        font_family="Franklin Gothic",
        #font_color="blue",
        title_font_family="Franklin Gothic",
        #title_font_color="red",
        #legend_title_font_color="green"
    )
    figHorometro.update_xaxes(title_font_family="Franklin Gothic")

    ####################### Gráfico Volumen agua lodosa ingresado al Geotube ############################
    labelGraphGT = 'gal'
    Qbomba = bomba["Caudal [GPM]"]
    Qbomba = list(map(lambda x: float(x), Qbomba))


    if value_unidades_GT == True:
        volLDS = np.array(Qbomba) * np.array(horasBomba) * 60  # [gal]
    else:
        labelGraphGT = 'm3'
        volLDS = np.array(Qbomba) * np.array(horasBomba) * 60 / 264.172 # [gal]





    # Crea la figura de agua lodosa
    figAguaLDS = go.Figure()

    figAguaLDS.add_trace(go.Scatter(x=fechaHorasBomba, y=volLDS, name=""))
    figAguaLDS.update_layout(title="Agua Lodosa Ingresada al Geotube", xaxis_title="Fecha",
                        yaxis_title="Volumen" + " [" + labelGraphGT + "]")
    figAguaLDS.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.7,
        xanchor="center",
        x=0.5
    ))

    figAguaLDS.update_layout(
        font_family="Franklin Gothic",
        #font_color="blue",
        title_font_family="Franklin Gothic",
        #title_font_color="red",
        #legend_title_font_color="green"
    )
    figAguaLDS.update_xaxes(title_font_family="Franklin Gothic")



    ############################### Gráfico Peso y Volumen Geotube ##############################################

    GT = dfGeotube[dfGeotube["Geotube"] == numGT]
    GT["Fecha Completa"] = GT["Fecha"] + " " + GT["Hora"]

    fechaGT = GT["Fecha Completa"]
    pesoGT = GT["Peso [ton]"]
    volGT = GT["Volumen [m3]"]

    fechaGT = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S"), fechaGT))
    pesoGT = list(map(lambda x: float(x), pesoGT))
    volGT = list(map(lambda x: float(x), volGT))

    # Crea la figura de peso y volumen
    figPesoVol = go.Figure()

    figPesoVol.add_trace(go.Scatter(x=fechaGT, y=pesoGT, name="Peso [ton]"))
    figPesoVol.add_trace(go.Scatter(x=fechaGT, y=volGT, name="Volumen [m3]"))
    figPesoVol.update_layout(title="Peso y Volumen Geotube", xaxis_title="Fecha",
                        yaxis_title="")
    figPesoVol.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    figPesoVol.update_layout(
        font_family="Franklin Gothic",
        #font_color="blue",
        title_font_family="Franklin Gothic",
        #title_font_color="red",
        #legend_title_font_color="green"
    )
    figPesoVol.update_xaxes(title_font_family="Franklin Gothic")

    prctDia4 = (prctDia / 100) * 10
    prctAcum4 = (prctAcum / 100) * 10
    aguaAcum4 = (round(aguaAcum0/len(numGT9)*100, 2) / 65) * 10
    pesoLDSextAcum4 = (pesoLDSextAcum9 / 3600) * 10



    prctUso4 = round((prctUso / 100) * 100, 2)
    prctUso5 = round((prctUso / 100) * 10, 2)



    return figcurvS, figRetorta, figHorometro, figPesoVol, figAguaLDS, progDia, ejecDia, varDia, \
           horoCortDia, horoMotorDia, horoBombaDia, aguaLDSdia, progAcum, ejecAcum, varAcum, \
           cortAcum, motorAcum, bombaAcum, aguaAcum, HCAcum, solAcum, diasOper, volBombGT, pesoLDSextAcum, \
           capGTRes, volGTRes, pesoGTRes, prctUso4, prctDia4, prctAcum4, aguaAcum4, pesoLDSextAcum4, \
           prctUso5, prctUso5


@app.callback(
    Output("download-component", "data"),
    Input("btn", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./assets/Instructivo_Piscina_Pulmón.pdf")

if __name__ == '__main__':
    app.run_server(debug=False)

