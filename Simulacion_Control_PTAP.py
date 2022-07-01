import math

import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import random
from datetime import datetime
import dash_daq as daq
# Importar hojas de trabajo de google drive     https://bit.ly/3uQfOvs
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
import time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.css.append_css({'external_url': '/static/reset.css'})
app.server.static_folder = 'static'
server = app.server

app.layout = dbc.Container([

    dcc.Interval(
        id='my_interval',
        disabled=False,
        interval=100000*1000,
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
            "Simulación del Sistema de Control - CL-800C - Refinería de Barrancabermeja",
            style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"}), width=12, )
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Accordion([
                dbc.AccordionItem([
                    html.H5([
                                'La siguiente simulación presenta la forma en el que el proceso de deshidratación de lodos del clarificador CL-800C será automatizado.'])

                ], title="Introducción"),
            ], start_collapsed=True, style={'textAlign': 'left', 'color': '#082255', 'font-family': "Franklin Gothic"}),

        ], style={'color': '#082255', 'font-family': "Franklin Gothic"}),
    ]),

    dbc.Row([
        dbc.Tabs([
            dbc.Tab([
                # dbc.Row([
                #     dbc.Col([
                #         html.Div([
                #             dcc.Input(
                #                 id='acelerador-tiempo',
                #                 type='number',
                #                 placeholder="1, 2, 3, etc",
                #                 # A hint to the user of what can be entered in the control
                #                 debounce=True,
                #                 # Changes to input are sent to Dash server only on enter or losing focus
                #                 min=1, max=1000, step=1,  # Ranges of numeric value. Step refers to increments
                #                 # minLength=0, maxLength=5,  # Ranges for character length inside input box
                #                 autoComplete='off',
                #                 disabled=False,  # Disable input box
                #                 readOnly=False,  # Make input box read only
                #                 required=True,  # Require user to insert something into input box
                #                 size="6",  # Number of characters that will be visible inside box
                #                 style={'font-family': "Franklin Gothic", 'textAlign': 'center', }
                #
                #             )
                #         ], className="d-grid gap-2"),
                #     ], className="d-grid gap-2"),
                # ]),
                dbc.Row([
                    dbc.Col([
                        html.Div(id='tiempo-real', style={'font-size':36}),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Seleccionar periodo [seg/purga]:",
                            id="periodo-target",
                            color="info",
                            className="me-1",
                            n_clicks=0,
                            style={'font-family': "Franklin Gothic"},
                        ),
                        dbc.Popover(
                            "Es el periodo en el cual cada purga es enviada del clarificador CL-800C a la caja de lodos.",
                            target="periodo-target",
                            body=True,
                            trigger="hover",
                            style={'font-family': "Franklin Gothic"}
                        ),

                    ], width=2, align='center', className="d-grid gap-2"),
                    dbc.Col([
                        html.Div([
                            dcc.Input(
                                id='periodo',
                                value=600,
                                type='number',
                                placeholder="seg/purg",
                                # A hint to the user of what can be entered in the control
                                debounce=True,
                                # Changes to input are sent to Dash server only on enter or losing focus
                                min=1, max=5000, step=1,  # Ranges of numeric value. Step refers to increments
                                minLength=0, maxLength=5,  # Ranges for character length inside input box
                                autoComplete='off',
                                disabled=False,  # Disable input box
                                readOnly=False,  # Make input box read only
                                required=True,  # Require user to insert something into input box
                                size="6",  # Number of characters that will be visible inside box
                                style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                            )
                        ], className="d-grid gap-2"),
                    ], className="d-grid gap-2"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Seleccionar duración [seg]:",
                            id="duracion-target",
                            color="info",
                            className="me-1",
                            n_clicks=0,
                            style={'font-family': "Franklin Gothic"},
                        ),
                        dbc.Popover(
                            "Es la duración de cada purga que es enviada del clarificador CL-800C a la caja de lodos.",
                            target="duracion-target",
                            body=True,
                            trigger="hover",
                            style={'font-family': "Franklin Gothic"}
                        ),

                    ], width=2, align='center', className="d-grid gap-2"),
                    dbc.Col([
                        html.Div([
                            dcc.Input(
                                id='duracion',
                                value=60,
                                type='number',
                                placeholder="seg",
                                # A hint to the user of what can be entered in the control
                                debounce=True,
                                # Changes to input are sent to Dash server only on enter or losing focus
                                min=1, max=1000, step=1,  # Ranges of numeric value. Step refers to increments
                                minLength=0, maxLength=5,  # Ranges for character length inside input box
                                autoComplete='off',
                                disabled=False,  # Disable input box
                                readOnly=False,  # Make input box read only
                                required=True,  # Require user to insert something into input box
                                size="6",  # Number of characters that will be visible inside box
                                style={'font-family': "Franklin Gothic", 'textAlign': 'center', }

                            )
                        ], className="d-grid gap-2"),
                    ], className="d-grid gap-2"),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Seleccionar mes:",
                            id="mes-target",
                            color="info",
                            className="me-1",
                            n_clicks=0,
                            style={'font-family': "Franklin Gothic"},
                        ),
                        dbc.Popover(
                            "Es el mes en el cual se está operando el clarificador CL-800C.",
                            target="mes-target",
                            body=True,
                            trigger="hover",
                            style={'font-family': "Franklin Gothic"}
                        ),

                    ], width=2, align='center', className="d-grid gap-2"),
                    dbc.Col([
                        dcc.Dropdown(id='mes',
                                     value=1,
                                     style={'font-family': "Franklin Gothic"},
                                     options=[
                                         {'label': 'Enero', 'value': 1},
                                         {'label': 'Febrero', 'value': 2},
                                         {'label': 'Marzo', 'value': 3},
                                         {'label': 'Abril', 'value': 4},
                                         {'label': 'Mayo', 'value': 5},
                                         {'label': 'Junio', 'value': 6},
                                         {'label': 'Julio', 'value': 7},
                                         {'label': 'Agosto', 'value': 8},
                                         {'label': 'Septiembre', 'value': 9},
                                         {'label': 'Octubre', 'value': 10},
                                         {'label': 'Noviembre', 'value': 11},
                                         {'label': 'Diciembre', 'value': 12},
                                     ],
                                     # options=[
                                     #     {'label': 'New York City', 'value': 'NYC'},
                                     #     {'label': 'Montreal', 'value': 'MTL'},
                                     #     {'label': 'San Francisco', 'value': 'SF'},
                                     # ],
                                     )
                    ]),

                ]),

                dbc.Row(dcc.Graph(id='fig-vol-caja-lodos')),
                dbc.Row(dcc.Graph(id='fig-alt-caja-lodos')),
            ], label="Resumen Diario", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([], label="Resumen Mensual", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([], label="Resumen Fase", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([], label="Resumen Total", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([], label="Resumen Geotube", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
        ]),
    ]),

])


@app.callback(
    Output(component_id='tiempo-real', component_property='children'),
    Output(component_id='fig-vol-caja-lodos', component_property='figure'),
    Output(component_id='fig-alt-caja-lodos', component_property='figure'),

    Input('my_interval', 'n_intervals'),
    Input('periodo', 'value'),
    Input('duracion', 'value'),
    Input('mes', 'value'),
    # Input(component_id='mes', component_property='value'),

    # Input('acelerador-tiempo', 'value'),

)
def tiempo(value_intervals, value_periodo, value_duracion, value_mes):
    periodo = value_periodo   # [seg]
    dura = value_duracion   # [seg]
    mes = value_mes   # []

    # Obtiene la concentración de SST en el mes & cantidad de GRAN purgas
    sstVec = [{1: 3500,
             2: 5000,
             3: 6000,
             4: 7500,
             5: 5000,
             6: 5200,
             7: 4000,
             8: 3000,
             9: 3600,
             10: 7500,
             11: 7000,
             12: 5000,
             }]
    sst = sstVec[0][mes]

    cantCranPurgsVec = [{1: 1,
             2: 2,
             3: 2,
             4: 3,
             5: 2,
             6: 2,
             7: 2,
             8: 1,
             9: 1,
             10: 3,
             11: 3,
             12: 2,
             }]
    cantGranPurgs = cantCranPurgsVec[0][mes]

    # Genera el tiempo que se tienen las GRANDES purgas
    L = 2  # [m] Longitud caja de lodos
    W = 2  # [m] Ancho caja de lodos
    H = 3  # [m] Altura caja de lodos
    t = 1
    tfinal = int(86400/2)   # [seg]
    tspan = list(range(0, tfinal))   # [seg]
    delVolGP = 6/60  # [m3/seg] cambio de volumen de la caja de lodos al llegar una gran purga
    duraGP = 120  # [seg] duración de la gran purga
    granPurgs = np.ones(len(tspan))
    granPurgs = np.array(granPurgs) * 0
    if cantGranPurgs == 1:
        seed = random.randint(0, len(granPurgs)-duraGP)
        for i in range(seed, seed+duraGP):
            granPurgs[i] = 1

    if cantGranPurgs == 2:
        seed1 = random.randint(0, len(granPurgs)/2 -duraGP)
        seed2 = random.randint(len(granPurgs)/2 -duraGP, len(granPurgs) -duraGP)
        for i in range(seed1, seed1+duraGP):
            granPurgs[i] = 1
        for i in range(seed2, seed2+duraGP):
            granPurgs[i] = 1

    if cantGranPurgs == 3:
        seed1 = random.randint(0, len(granPurgs)/3 -duraGP)
        seed2 = random.randint(len(granPurgs)/3 -duraGP, len(granPurgs)*2/3 -duraGP)
        seed3 = random.randint(len(granPurgs)*2/3 -duraGP, len(granPurgs) -duraGP)
        for i in range(seed1, seed1+duraGP):
            granPurgs[i] = 1
        for i in range(seed2, seed2+duraGP):
            granPurgs[i] = 1
        for i in range(seed3, seed3+duraGP):
            granPurgs[i] = 1

    # Calcula el volumen ingrasado a la caja de lodos de las GRANDES purgas
    volInGP = granPurgs * delVolGP  # [m] volumen ingresada a la caja de lodos

    # print(seed)
    print(granPurgs[:1000])

    # Generar periodo de tiempo y frecuencia de purgas
    purgs = np.ones(len(tspan))
    purgs = np.array(purgs) * 0

    for i in range(0, len(purgs), periodo):
        for j in range(0, dura):
            purgs[i+j] = 1

    Alods = 0.7/60   # [m/seg]

    # Volumen ingresado a la caja de lodos por pequeñas purgas
    purgs = np.array(purgs)
    ACL = purgs * Alods  # [m] Altura ingresada a la caja de lodos
    VolinCL2 = purgs * (Alods * L * W)  # [m] volumen ingresada a la caja de lodos
    # print(VolinCL2[:1000])

    # Volumen ingresado a la caja de lodos por pequeñas & GRANDES purgas
    volInTot = VolinCL2 + volInGP

    # Volumen bombeado de la caja de lodos al Geotube
    Hmax = 2.5  # [m] Altura de inicio de bombeo
    Hmin = 0.3  # [m] Altura parada de bombeo
    Vmax = Hmax * W * L  # [m] Volumen de inicio de bombeo
    Vmin = Hmin * W * L  # [m] Volumen parada de bombeo
    Qbomb = 1.71/60  # [m3/s] Caudal de bombeo a 15bar
    # Qbomb = 0  # [m3/s] Caudal de bombeo a 15bar

    tbombOn = np.ones(len(tspan))
    tbombOn = np.array(tbombOn) * 0


    # Cálculo junto de todas las variables
    volCLVec = np.ones(len(tspan))
    voloutCL = np.ones(len(tspan))
    volBomb = np.ones(len(tspan))

    volCLVec = np.array(volCLVec) * 0
    voloutCL = np.array(voloutCL) * 0
    volBomb = np.array(volBomb) * 0

    bombBTN = 0

    for i in range(0, len(tspan)-1):

        if volCLVec[i] >= Vmax or bombBTN == 1:
            bombBTN = 1
            tbombOn[i] = 1
            volBomb[i] = tbombOn[i] * Qbomb * bombBTN
            volCLVec[i+1] = volCLVec[i] - volBomb[i] + VolinCL2[i]
            if volCLVec[i] >= (L * W * H):
                volCLVec[i] = (L * W * H)
                voloutCL[i] = VolinCL2[i]
            if volCLVec[i] < Vmin:
                bombBTN = 0
        else:
            volCLVec[i + 1] = volCLVec[i] + VolinCL2[i]


    # Crea la figura de volumenes de la caja de lodos
    figVolCL = go.Figure()
    figVolCL.add_trace(go.Scatter(x=tspan, y=volCLVec, name="Volumen caja de lodos [m3]"))
    figVolCL.add_trace(go.Scatter(x=tspan, y=VolinCL2, name="Volumen ingresado de las pequeñas purgas a la caja de lodos [m3]"))
    figVolCL.add_trace(go.Scatter(x=tspan, y=voloutCL, name="Volumen egresado de la caja de lodos [m3]"))
    figVolCL.add_trace(go.Scatter(x=tspan, y=volInGP, name="Volumen ingresado de las grandes purgas a la caja de lodos [m3]"))
    figVolCL.add_trace(go.Scatter(x=tspan, y=volInTot, name="Volumen ingresado total a la caja de lodos [m3]"))
    figVolCL.update_layout(title="Volumen Caja de lodos", xaxis_title="Tiempo [seg]",
                        yaxis_title="Volumen [m3]")
    figVolCL.update_layout(legend=dict(
        yanchor="bottom",
        y=-1,
        xanchor="center",
        x=0.5
    ))
    figVolCL.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figVolCL.update_xaxes(title_font_family="Franklin Gothic")

    # Crea la figura de altura de la caja de lodos
    figAltCL = go.Figure()
    figAltCL.add_trace(go.Scatter(x=tspan, y=volCLVec/(L*W), name="Altura caja de lodos [m]"))
    figAltCL.add_trace(go.Scatter(x=tspan, y=VolinCL2/(L*W), name="Altura ingresada a la caja de lodos [m]"))
    figAltCL.add_trace(go.Scatter(x=tspan, y=voloutCL/(L*W), name="Altura egresada de la caja de lodos [ma]"))
    figAltCL.update_layout(title="Altura Caja de lodos", xaxis_title="Tiempo [seg]",
                        yaxis_title="Volumen [m3]")
    figAltCL.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))
    figAltCL.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figAltCL.update_xaxes(title_font_family="Franklin Gothic")




    return t, figVolCL, figAltCL


    # value_acel = float(value_acel)
    #
    # # Se genera el reloj
    # # tseg = round((value_intervals / (1/100)) % 60)
    # tseg = round((value_intervals * (1/(value_acel*10))) % 60)
    #
    # tmin = math.floor(value_intervals * (1/6000)) % 60
    # thora = math.floor(value_intervals * (1/360000)) % 24
    #
    # if tseg < 10:
    #     tseg = str('0') + str(tseg)
    #
    # if tmin < 10:
    #     tmin = str('0') + str(tmin)
    #
    # if thora < 10:
    #     thora = str('0') + str(thora)
    #
    # t = str(thora) + str(':') + str(tmin) + str(':') + str(tseg)


# @app.callback(
#     Output(component_id='my_interval', component_property='interval'),
#
#     Input('acelerador-tiempo', 'value'),
#
# )
# def tiempo(value_acel):
#
#     # acel = round(float(value_acel) * 1000)
#     acel =value_acel
#     print('El inervalo es de:')
#     print(acel)
#
#     return acel



if __name__ == '__main__':
    app.run_server()




