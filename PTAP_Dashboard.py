import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
#import dash_html_components as html
#import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go


# Importar hojas de trabajo de google drive     https://bit.ly/3uQfOvs
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID spreadsheet.
SAMPLE_SPREADSHEET_ID = '1uHo9KZbHzh1QXidL1-2c6uNjK4plKZHAM9GaPc8pcok'
SAMPLE_RANGE_PURGAS = "1. Purgas"

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result_PURGAS = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_PURGAS).execute()

# Obtiene y transforma hoja de purgas de google drive
dfPURG_GD = result_PURGAS.get('values', [])
names = ["Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]", "Altura Final [m]", "Tiempo [min]", "Volumen [m3]", "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]", "Total Purgas Captadas", "Fase"]
dfPURG_GD = pd.DataFrame(dfPURG_GD, columns =names)
dfPURG_GD.drop([0], inplace = True)

# Obtiene y transforma hoja de lodos de google drive
SAMPLE_RANGE_LODOS = "2. Lodos"

# Call the Sheets API
result_PURGAS = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_LODOS).execute()

dfLDS_GD = result_PURGAS.get('values', [])
names = ["Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]", "Altura Final [m]", "Tiempo [min]", "Volumen [m3]", "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]", "Total Purgas Bombeadas", "Fase"]
dfLDS_GD = pd.DataFrame(dfLDS_GD, columns =names)
dfLDS_GD.drop([0], inplace = True)
dfLDS_GD = dfLDS_GD.rename(index = lambda x: x -1)


# Obtiene y transforma hoja de clarificado de google drive
SAMPLE_RANGE_CLR = "3. Clarificado"

# Call the Sheets API
result_CLR = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_CLR).execute()

dfCLR_GD = result_CLR.get('values', [])
names = ["Fecha", "Hora Inicio", "Hora Fin", "Lectura Inicial", "Lectura Final", "Turbidez [NTU]", "Color [Pt-Co]", "pH", "Tiempo [min]", "Volumen [m3]", "Volumen [gal]", "Tiempo Acumulado [min]", "Volumen Acumulado [m3]", "Volumen Acumulado [gal]", "Fase"]
dfCLR_GD = pd.DataFrame(dfCLR_GD, columns =names)
dfCLR_GD.drop([0], inplace = True)
dfCLR_GD = dfCLR_GD.rename(index = lambda x: x -1)



# Obtiene y transforma hoja de Geotube de google drive
SAMPLE_RANGE_GT = "4. Geotube"

# Call the Sheets API
result_GT = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_GT).execute()

dfGT_GD = result_GT.get('values', [])
names = ["Numero", "Fecha", "Volumen Teórico [m3]", "% Uso", "Peso [Ton]", "Capacidad [m3]", "Fase"]
dfGT_GD = pd.DataFrame(dfGT_GD, columns =names)
dfGT_GD.drop([0], inplace = True)
dfGT_GD = dfGT_GD.rename(index = lambda x: x -1)

#print(dfGT_GD)

# Obtiene y transforma hoja de alimentación CL 800C de google drive
SAMPLE_RANGE_AlCLR = "5. Alimentación - CL800C"

# Call the Sheets API
result_AlCLR = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_AlCLR).execute()

dfAlCLR_GD = result_AlCLR.get('values', [])
names = ["Día", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
dfAlCLR_GD = pd.DataFrame(dfAlCLR_GD, columns =names)
dfAlCLR_GD.drop([0], inplace = True)
dfAlCLR_GD = dfAlCLR_GD.rename(index = lambda x: x -1)



dfPURG = dfPURG_GD
dfLDS = dfLDS_GD
dfCLR = dfCLR_GD
dfGT = dfGT_GD
dfAlCLR = dfAlCLR_GD

print(dfPURG)
#print(dfLDS)
#print(dfCLR)
#print(dfGT)
#print(dfAlCLR)


#convertir datos de string a tipo fecha
from datetime import datetime
fechaPURG = dfPURG.loc[:,"Fecha"]
fechaCLR = dfCLR.loc[:,"Fecha"]
fechaLDS = dfLDS.loc[:,"Fecha"]
fechaGT = dfGT.loc[:,"Fecha"]

ultAct = dfCLR["Fecha"].iloc[-1]
ultAct = str(ultAct)
meses = [9, 10, 11]
fechaPURGdd = list(dict.fromkeys(fechaPURG))
fechaCLRdd = list(dict.fromkeys(fechaCLR))

fechaGTdd = list(dict.fromkeys(fechaGT))

for i in range(0, len(fechaCLR)):
    fechaCLR[i] = datetime.strptime(fechaCLR[i], "%d/%m/%Y")

for i in range(0, len(fechaLDS)):
    fechaLDS[i] = datetime.strptime(fechaLDS[i], "%d/%m/%Y")

for i in range(0, len(fechaGT)):
    fechaGT[i] = datetime.strptime(fechaGT[i], "%d/%m/%Y")

# Obtiene la lista de los años que se han trabajado
anosfechaLDS = []
for x in fechaLDS:
    y = x.year
    anosfechaLDS.append(y)

anosfechaLDS = list(dict.fromkeys(anosfechaLDS))



#print(dfPURG)

#convertir datos de string a tipo numérico decimal
galCLRvec = dfCLR.loc[:,"Volumen [gal]"] # vector de los galones bombeados al clrificador
#print(galCLRvec)
for i in range(0, len(galCLRvec)):
    if galCLRvec[i] != "":
        galCLRvec[i] = float(galCLRvec[i])


pHCLRvec = dfCLR.loc[:,"pH"] # vector del pH de agua clarificada
#print(pHCLRvec)

#print(pHCLRvec)
for i in range(0, len(pHCLRvec)):
    if pHCLRvec[i] != "":
        pHCLRvec[i] = float(pHCLRvec[i])


turbCLRvec = dfCLR.loc[:,"Turbidez [NTU]"] # vector de la turbidez de agua clarificada
for i in range(0, len(turbCLRvec)):
    turbCLRvec[i] = float(turbCLRvec[i])

colorCLRvec = dfCLR.loc[:,"Color [Pt-Co]"] # vector del color de agua clarificada
for i in range(0, len(colorCLRvec)):
    if colorCLRvec[i] != "":
        colorCLRvec[i] = float(colorCLRvec[i])

galLDSvec = dfLDS.loc[:,"Volumen [gal]"] # vector de los galones captados del clarificador
for i in range(0, len(galLDSvec)):
    galLDSvec[i] = float(galLDSvec[i])

m3GTvec = dfGT.loc[:,"Volumen Teórico [m3]"] # vector de volumen teórico de Geotube
for i in range(0, len(m3GTvec)):
    m3GTvec[i] = float(m3GTvec[i])

usoGTvec = dfGT.loc[:,"% Uso"] # vector de volumen teórico de Geotube
for i in range(0, len(usoGTvec)):
    usoGTvec[i] = float(usoGTvec[i])

pesoGTvec = dfGT.loc[:,"Peso [Ton]"] # vector de volumen teórico de Geotube
for i in range(0, len(pesoGTvec)):
    pesoGTvec[i] = float(pesoGTvec[i])

numGTvec = dfGT.loc[:,"Numero"]
for i in range(0, len(numGTvec)):
    numGTvec[i] = float(numGTvec[i])


capGTvec = dfGT.loc[:,"Capacidad [m3]"]
for i in range(0, len(capGTvec)):
    capGTvec[i] = float(capGTvec[i])

alCLRvec = dfAlCLR.loc[31,:]
for i in range(1, len(alCLRvec)):
    alCLRvec[i] = float(alCLRvec[i])

numGTdd = list(dict.fromkeys(numGTvec))
fasedd = list(dict.fromkeys(dfPURG["Fase"]))


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

valuePurgCapt = dcc.Textarea(
        id='purg-capt-dia',
        value={},
        style={'width': '100%', 'height': 300},
    )

badgePurgCapt = dbc.Button(
    [
        "Purgas Captadas:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="secondary",
)

badgeSelecAno = dbc.Button(
    [
        "Seleccionar año:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="info",
)

badgeSelecMes = dbc.Button(
    [
        "Seleccionar mes:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="info",
)

badgeSelecDia = dbc.Button(
    [
        "Seleccionar día:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="info",
)

badgeSelecUnidades = dbc.Button(
    [
        "Seleccionar unidades:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="info",
)


badgeVolCapt = dbc.Button(
    [
        "Volumen Captado:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="secondary",
)

badgeBomb = dbc.Button(
    [
        "Bombeos retornados:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeVolRet = dbc.Button(
    [
        "Volumen Retornado:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgepHdia = dbc.Button(
    [
        "pH:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="success",
)

badgeturbdia = dbc.Button(
    [
        "Turbidez [NTU]:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="success",
)

badgecolordia = dbc.Button(
    [
        "Color:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="success",
)

badgenumGT = dbc.Button(
    [
        "Número:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="info",
)

badgecapGT = dbc.Button(
    [
        "Capacidad:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeusoGT = dbc.Button(
    [
        "Uso:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgevolGT = dbc.Button(
    [
        "Volumen:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgepesoGT = dbc.Button(
    [
        "Peso:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeDiasTra = dbc.Button(
    [
        "Días  Trabajados:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgePrctAguaTrat = dbc.Button(
    [
        "Agua tratada:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="primary",
)

badgeSelecFase = dbc.Button(
    [
        "Seleccionar Fase:",
        dbc.Badge("", color="light", text_color="primary", className="ms-1"),
    ],
    color="info",
)

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([dbc.CardImg(
            src="/assets/Logo.jpg",

            style={"width":"6rem",
                   'text-align': 'center'},
        ),
        ]),
    ]),
    dbc.Row([
                        dbc.Col(html.H1(
                            "Resumen del Sistema de Deshidratación de Lodos - Área de PTAP - Refinería de Barrancabermeja",
                            style={'textAlign': 'center'}), width=12)
                    ]),
    dbc.Row([
        dbc.Col([
            html.H5('Última actualización: ' + str(ultAct), style={'textAlign': 'right'})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Resumen Diario']))
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeSelecUnidades)
                        ]),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[
                                    {"label": "Galones", "value": True},
                                    {"label": "Metros cúbicos", "value": False},
                                ],
                                value=True,
                                id="unidades-input",
                            ),
                        ]),
                        dbc.Col([
                            dbc.Row(badgeSelecDia)
                        ], ),
                        dbc.Col([
                            dcc.Dropdown(id='Dia',
                                options=[{'label':x, 'value':x}
                                        for x in fechaCLRdd],
                                value='13/09/2021'
                         )
                        ], ),
                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgePurgCapt)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='purg-capt-dia')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgepHdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='pH-dia')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeBomb)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='bomb-dia')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgeturbdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='turb-dia')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolCapt),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-capt-dia')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgecolordia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='color-dia')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolRet),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-ret-dia')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgePrctAguaTrat),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='agua-trat-dia')
                        ], ),
                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([

                    ]),
                ])
                ]),

            ]),

        ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Resumen Mensual']))
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeSelecUnidades)
                        ]),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[
                                    {"label": "Galones", "value": True},
                                    {"label": "Metros cúbicos", "value": False},
                                ],
                                value=True,
                                id="unidades-mes-input",
                            ),
                        ]),
                        dbc.Col([
                            dbc.Row(badgeSelecAno)
                        ], ),
                        dbc.Col([
                            dcc.Dropdown(id='Ano',
                                         options=[{'label': x, 'value': x}
                                                  for x in anosfechaLDS],
                                         value=2021
                                         )
                        ], ),
                        dbc.Col([
                            dbc.Row(badgeSelecMes)
                        ], ),
                        dbc.Col([
                            dcc.Dropdown(id='meses',  # PONER DROPDOWN DINÁMICO DEPENDIENDO DE LAS FECHAS
                                         options=[],
                                         value=9
                                         )
                        ], ),
                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgePurgCapt)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='purg-capt-mes')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgepHdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='pH-mes')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeBomb)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='bomb-mes')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgeturbdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='turb-mes')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolCapt),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-capt-mes')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgecolordia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='color-mes')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolRet),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-ret-mes')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgePrctAguaTrat),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='agua-trat-mes')
                        ], ),
                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([

                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeDiasTra),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='dias-mes')
                        ], ),
                    ]),
                    dbc.Row(dcc.Graph(id='mi-mes-vol')),
                    dbc.Row(dcc.Graph(id='mi-mes-prop')),

                ])
            ]),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Resumen de Fase']))
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeSelecUnidades)
                        ]),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[
                                    {"label": "Galones", "value": True},
                                    {"label": "Metros cúbicos", "value": False},
                                ],
                                value=True,
                                id="unidades-fase-input",
                            ),
                        ]),
                        dbc.Col([
                            dbc.Row(badgeSelecFase)
                        ], ),
                        dbc.Col([
                            dcc.Dropdown(id='fase',
                                         options=[{'label': x, 'value': x}
                                                  for x in fasedd],
                                         value='2'
                                         )
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgePurgCapt)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='purg-capt-fase')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgepHdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='pH-fase')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeBomb)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='bomb-fase')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgeturbdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='turb-fase')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolCapt),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-capt-fase')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgecolordia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='color-fase')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolRet),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-ret-fase')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgePrctAguaTrat),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='agua-trat-fase')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeDiasTra),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='dias-fase')
                        ], ),
                    ]),
                    dbc.Row(dcc.Graph(id='mi-fase-vol')),
                    dbc.Row(dcc.Graph(id='mi-fase-prop')),

                ])
            ]),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Row(html.H2(['Resumen Acumulado']))
                    ]),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(badgeSelecUnidades)
                    ]),
                    dbc.Col(dbc.RadioItems(
                        options=[
                            {"label": "Galones", "value": True},
                            {"label": "Metros cúbicos", "value": False},
                        ],
                        value=True,
                        id="unidades-acum-input",
                    ), ),
                ]),
                dbc.Row([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgePurgCapt)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='purg-capt-acum')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgepHdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='pH-acum')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeBomb)
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='bomb-acum')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgeturbdia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='turb-acum')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolCapt),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-capt-acum')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgecolordia),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='color-acum')
                        ], ),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeVolRet),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='vol-ret-acum')
                        ], ),
                        dbc.Col([
                            dbc.Row(badgePrctAguaTrat),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='agua-trat-acum')
                        ], ),
                    ]),

                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeDiasTra),
                        ], ),
                        dbc.Col([
                            dcc.Graph(id='dias-acum')
                        ], ),
                    ]),
                    dbc.Row(dcc.Graph(id='mi-acum-vol')),
                    dbc.Row(dcc.Graph(id='mi-acum-prop')),

                ])

            ]),
            ])


        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                dbc.Row([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(html.H2(['Resumen Geotube']))
                        ]),

                ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Row(badgeSelecUnidades)
                        ]),
                        dbc.Col(dbc.RadioItems(
                            options=[
                                {"label": "Galones", "value": True},
                                {"label": "Metros cúbicos", "value": False},
                            ],
                            value=True,
                            id="unidades-GT-input",
                        ), ),
                        dbc.Col([
                            dbc.Row(badgenumGT)
                        ], ),
                        dbc.Col([
                            dcc.Dropdown(id='numGTDD',
                                         options=[{'label': x, 'value': x}
                                                  for x in numGTdd],
                                         value=6
                                         )
                        ], ),
                        dbc.Col([
                            dbc.Row(badgeSelecDia)
                        ], ),
                        dbc.Col([
                            dcc.Dropdown(id='fechaGTDD',
                                         options=[],
                                         # value='13/09/2021'
                                         )
                        ], ),

                    ]),
                    dbc.Row([
                        dbc.Col(dbc.Row(badgenumGT)),
                        dbc.Col(dcc.Graph(id='num-GT')),
                        dbc.Col(dbc.Row(badgeusoGT)),
                        dbc.Col(dcc.Graph(id='uso-GT')),
                    ]),
                    dbc.Row([
                        dbc.Col(dbc.Row(badgecapGT)),
                        dbc.Col(dcc.Graph(id='cap-GT')),
                        dbc.Col(dbc.Row(badgevolGT)),
                        dbc.Col(dcc.Graph(id='vol-GT')),
                    ]),
                    dbc.Row([
                        dbc.Col(dbc.Row(badgepesoGT)),
                        dbc.Col(dcc.Graph(id='peso-GT')),
                    ]),
                    dbc.Row(dcc.Graph(id='fig-GT')),
                    dbc.Row(dcc.Graph(id='fig-uso-GT')),
            ])
        ])
            ])

    ])
])
])




@app.callback(
    Output(component_id='purg-capt-dia', component_property="figure"),
    Output(component_id='vol-capt-dia', component_property="figure"),
    Output(component_id='bomb-dia', component_property="figure"),
    Output(component_id='vol-ret-dia', component_property="figure"),
    Output(component_id='pH-dia', component_property="figure"),
    Output(component_id='turb-dia', component_property="figure"),
    Output(component_id='color-dia', component_property="figure"),
    Output(component_id='agua-trat-dia', component_property="figure"),
    Input(component_id='Dia', component_property='value'),
    Input(component_id='unidades-input', component_property='value'),

)

def dia_interactivo(value_dia,value_unidades):
    #fechaDIA = 12
    #mes = 10
    #print(value_mes)
    #print(value_dia)
    #print(value_unidades)
    #value_mes = float(value_mes)

    # --------------------------------- Módulo 1 ------------------------------------------

    # Calcula las purgas captadas para un día determinado & volumen [gal] total para un día determinado
    fechaDIA = value_dia
    fechaDIA = datetime.strptime(fechaDIA, "%d/%m/%Y")
    fechaDIA = fechaDIA.day


    purgsdiaLDS = 0
    galdiaLDS = 0
    galdiaLDSacum = 0
    for i in range(0, len(fechaLDS)):
        if fechaDIA == fechaLDS[i].day:
            purgsdiaLDS = purgsdiaLDS + 1
            galdiaLDS = galLDSvec[i]
            galdiaLDSacum = galdiaLDSacum + galdiaLDS



    # Calcula los bombeos de clarificado para un día determinado & volumen [gal] total de bombeo de clarificado para un día determinado & turbidez, color y pH de agua clarificada para un día determinado
    purgsdiaCLR = 0
    galdiaCLR = 0
    galdiaCLRacum = 0
    pHdiaCLR = 0
    pHdiaCLRacum = 0
    turbdiaCLR = 0
    turbdiaCLRacum = 0
    colordiaCLR = 0
    colordiaCLRacum = 0

    for i in range(0, len(fechaCLR)):
        if fechaDIA == fechaCLR[i].day:
            purgsdiaCLR = purgsdiaCLR + 1
            galdiaCLR = galCLRvec[i]
            galdiaCLRacum = galdiaCLRacum + galdiaCLR

            pHdiaCLR = pHCLRvec[i]
            pHdiaCLRacum = pHdiaCLRacum + pHdiaCLR

            turbdiaCLR = turbCLRvec[i]
            turbdiaCLRacum = turbdiaCLRacum + turbdiaCLR

            colordiaCLR = colorCLRvec[i]
            colordiaCLRacum = colordiaCLRacum + colordiaCLR

    # Calcula el promedio del dia de pH, turbidez y color
    pHdiaCLRprom = pHdiaCLRacum / purgsdiaCLR
    turbdiaCLRprom = turbdiaCLRacum / purgsdiaCLR
    colordiaCLRprom = colordiaCLRacum / purgsdiaCLR

    # Obtiene el flujo de entrada promedio del al clarificador
    fechaDIA = value_dia
    fechaDIA = datetime.strptime(fechaDIA, "%d/%m/%Y")
    for i in range(1, len(alCLRvec)):
        if fechaDIA.month == i:
            galInCLR = galCLRvec[i]

   # Calcula el porcentaje de agua tratada proveniente de las purgas en un día
    prctOutDiavec = [0.67, 0.71, 0.98, 0.6, 0.86, 0.57, 0.67, 0.64, 0.8, 0.78, 0.83, 0.99, 0.66, 0.57, 0.66, 0.92, 0.81, 0.54, 0.84, 0.87, 0.83, 0.51, 0.99, 0.57, 0.66, 0.96, 0.5, 0.58, 0.88, 0.77, 0.6]
    for i in range(0, len(prctOutDiavec)):
        if fechaDIA.day == i:
            prctOutDia = prctOutDiavec[i]
            galOutCLRdia = galInCLR * 60 * 24 * prctOutDia
            prctaguatratdia = galdiaCLRacum/galOutCLRdia


    #Cambia unidades a m3 por radioitem
    suffix_galdiaacum = " gal"
    if value_unidades == False:
        galdiaLDSacum = galdiaLDSacum / 264.72
        galdiaCLRacum = galdiaCLRacum / 264.72
        #prctaguatratdia = prctaguatratdia * 264.72
        suffix_galdiaacum = " m3"

    # Crea indicador de las purgas captadas en un día
    figpurgsdiaLDS = go.Figure()
    figpurgsdiaLDS.add_trace(go.Indicator(
        value=purgsdiaLDS,))

    figpurgsdiaLDS.update_traces(number={"font":{"size":18}})
    figpurgsdiaLDS.update_layout(height=30, width=150)


    # Crea indicador del volumen captado en un día
    figgaldiaLDSacum = go.Figure()
    figgaldiaLDSacum.add_trace(go.Indicator(
        value=galdiaLDSacum,
        number = {'suffix': suffix_galdiaacum},
    ))

    figgaldiaLDSacum.update_traces(number={"font": {"size": 18}})
    figgaldiaLDSacum.update_layout(height=30, width=150)

    # Crea indicador de los bombeos de clarificado en un día
    figpurgsdiaCLR = go.Figure()
    figpurgsdiaCLR.add_trace(go.Indicator(
        value=purgsdiaCLR, ))

    figpurgsdiaCLR.update_traces(number={"font": {"size": 18}})
    figpurgsdiaCLR.update_layout(height=30, width=150)

    # Crea indicador del volumen de clarificado retornado en un día
    figgaldiaCLRacum = go.Figure()
    figgaldiaCLRacum.add_trace(go.Indicator(
        value=galdiaCLRacum,
        number={'suffix': suffix_galdiaacum},
    ))

    figgaldiaCLRacum.update_traces(number={"font": {"size": 18}})
    figgaldiaCLRacum.update_layout(height=30, width=150)

    # Crea indicador del ph de agua clarificada retornada en un día
    figpHdiaCLRprom = go.Figure()
    figpHdiaCLRprom.add_trace(go.Indicator(
        value=pHdiaCLRprom, ))

    figpHdiaCLRprom.update_traces(number={"font": {"size": 18}})
    figpHdiaCLRprom.update_layout(height=30, width=150)

    # Crea indicador de la turbidez de agua clarificada retornada en un día
    figturbdiaCLRprom = go.Figure()
    figturbdiaCLRprom.add_trace(go.Indicator(
        value=turbdiaCLRprom, ))

    figturbdiaCLRprom.update_traces(number={"font": {"size": 18}})
    figturbdiaCLRprom.update_layout(height=30, width=150)

    # Crea indicador del color de agua clarificada retornada en un día
    figcolordiaCLRprom = go.Figure()
    figcolordiaCLRprom.add_trace(go.Indicator(
        value=colordiaCLRprom, ))

    figcolordiaCLRprom.update_traces(number={"font": {"size": 18}})
    figcolordiaCLRprom.update_layout(height=30, width=150)

    # Crea indicador del porcentaje de agua tratada de purgas en un día
    figprctaguatratdia = go.Figure()
    figprctaguatratdia.add_trace(go.Indicator(
        value=prctaguatratdia*100,
        number={'suffix': "%"},
        delta={'reference': 1}, ))

    figprctaguatratdia.update_traces(number={"font": {"size": 18}})
    figprctaguatratdia.update_layout(height=30, width=150)

    return figpurgsdiaLDS, figgaldiaLDSacum, figpurgsdiaCLR, figgaldiaCLRacum, figpHdiaCLRprom, figturbdiaCLRprom, figcolordiaCLRprom, \
           figprctaguatratdia



@app.callback(
    Output('meses', 'options'),
    Input(component_id='Ano', component_property='value'),
)

def Selec_mes_interactivo(value_ano):
    meses_selec = []
    for x in fechaLDS:
    #for x in fechaPURGdd:
        if x.year == value_ano:
            y = x.month
            meses_selec.append(y)

    meses_selec = list(dict.fromkeys(meses_selec))
    return [{'label':c, 'value':c} for c in meses_selec]

@app.callback(
    Output('meses', 'value'),
    Input('meses', 'options'),
)

def set_Geotube_fecha_value(mes_selec):
    x = mes_selec[0]
    x = x["value"]
    return x

@app.callback(
    Output(component_id='purg-capt-mes', component_property="figure"),
    Output(component_id='vol-capt-mes', component_property="figure"),
    Output(component_id='bomb-mes', component_property="figure"),
    Output(component_id='vol-ret-mes', component_property="figure"),
    Output(component_id='pH-mes', component_property="figure"),
    Output(component_id='turb-mes', component_property="figure"),
    Output(component_id='color-mes', component_property="figure"),
    Output(component_id='agua-trat-mes', component_property="figure"),
    Output(component_id='dias-mes', component_property="figure"),
    Output(component_id='mi-mes-vol', component_property="figure"),
    Output(component_id='mi-mes-prop', component_property="figure"),
    Input(component_id='meses', component_property='value'),
    Input(component_id='unidades-mes-input', component_property='value'),
    Input(component_id='Ano', component_property='value'),


)


def mes_interactivo(value_mes, value_unidades, value_año):

    # --------------------------------- Módulo 2 ------------------------------------------
    #print(value_mes)
    #print(value_unidades)
    # Calcula las purgas captadas para un mes determinado & volumen [gal] total para un mes determinado
    mes = value_mes
    #año = float(value_año)
    año = value_año
    #print(año)
    print(type(año))
    purgsmesLDS = 0
    galmesLDS = 0
    galmesLDSacum = 0
    for i in range(0, len(fechaLDS)):
        if mes == fechaLDS[i].month and año == fechaLDS[i].year:
            purgsmesLDS = purgsmesLDS + 1
            galmesLDS = galLDSvec[i]
            galmesLDSacum = galmesLDSacum + galmesLDS

    # Calcula los bombeos de clarificado para un mes determinado & volumen [gal] total de bombeo de clarificado para un mes determinado & turbidez, color y pH de agua clarificada para un día determinado
    purgsmesCLR = 0
    galmesCLR = 0
    galmesCLRacum = 0
    pHmesCLR = 0
    pHmesCLRacum = 0
    turbmesCLR = 0
    turbmesCLRacum = 0
    colormesCLR = 0
    colormesCLRacum = 0
    #print(fechaCLR)

    for i in range(0, len(fechaCLR)):

        if mes == fechaCLR[i].month and año == fechaCLR[i].year:

            purgsmesCLR = purgsmesCLR + 1
            galmesCLR = galCLRvec[i]
            galmesCLRacum = galmesCLRacum + galmesCLR

            pHmesCLR = pHCLRvec[i]
            pHmesCLRacum = pHmesCLRacum + pHmesCLR

            turbmesCLR = turbCLRvec[i]
            turbmesCLRacum = turbmesCLRacum + turbmesCLR

            colormesCLR = colorCLRvec[i]
            colormesCLRacum = colormesCLRacum + colormesCLR

    # Calcula el promedio del mes de pH, turbidez y color


    pHmesCLRprom = pHmesCLRacum / purgsmesCLR
    turbmesCLRprom = turbmesCLRacum / purgsmesCLR
    colormesCLRprom = colormesCLRacum / purgsmesCLR


    # Toma los días de un mes de galones de clarificado y turbidez, color y pH
    fechamesCLR = 0
    fechamesCLRxlbl = [None]

    for i in range(0, len(fechaCLR)):
        if mes == fechaCLR[i].month and año == fechaCLR[i].year:
            fechamesCLR = fechaCLR[i]
            a = np.array(fechamesCLRxlbl)
            fechamesCLRxlbl = np.resize(a, i + 1)
            fechamesCLRxlbl[i] = fechamesCLR

    # Elimina los espacios vacíos de los vectores
    fechamesCLRxlblF = [None]
    galmesCLRvec = [None]
    cont = 1
    for i in range(0, len(fechamesCLRxlbl)):
        if fechamesCLRxlbl[i] != None:
            a = np.array(fechamesCLRxlblF)
            fechamesCLRxlblF = np.resize(a, cont)

            b = np.array(galmesCLRvec)
            galmesCLRvec = np.resize(b, cont)

            fechamesCLRxlblF[cont - 1] = fechamesCLRxlbl[i]
            galmesCLRvec[cont - 1] = galCLRvec[i]
            cont = cont + 1

    # Toma los días de un mes de volumen de purgas captadas
    fechamesLDS = 0
    fechamesLDSxlbl = [None]

    for i in range(0, len(fechaLDS)):
        if mes == fechaLDS[i].month and año == fechaLDS[i].year:
            fechamesLDS = fechaLDS[i]
            a = np.array(fechamesLDSxlbl)
            fechamesLDSxlbl = np.resize(a, i + 1)
            fechamesLDSxlbl[i] = fechamesLDS

   # Elimina los espacios vacíos de los vectores
    fechamesLDSxlblF = [None]
    cont = 1
    for i in range(0, len(fechamesLDSxlbl)):
        if fechamesLDSxlbl[i] != None:
            a = np.array(fechamesLDSxlblF)
            fechamesLDSxlblF = np.resize(a, cont)

            fechamesLDSxlblF[cont - 1] = fechamesLDSxlbl[i]
            cont = cont + 1

    # Calcula los galones de agua clarificada totales enviados por día en un mes
    cont = 0
    galmesCLR2 = 0
    galmesCLRacum2 = 0
    galmesCLRylbl = [None]

    for j in range(1, 31):
        for i in range(0, len(fechamesCLRxlblF)):
            if j == fechamesCLRxlblF[i].day:
                galmesCLR2 = galmesCLRvec[i]  # PROBLEMA GALclrVEC
                galmesCLRacum2 = galmesCLRacum2 + galmesCLR2
                # print(j)
                a = np.array(galmesCLRylbl)
                galmesCLRylbl = np.resize(a, j + 5)
                # print(len(galmesCLRylbl))
                # print(galmesCLRylbl)
                galmesCLRylbl[j] = galmesCLRacum2

        galmesCLRacum2 = 0  # dentro del j fuera del i
        cont = cont + 1

    # Calcula los galones de purgas totales captadas por día en un mes
    galmesLDS2 = 0
    galmesLDSacum2 = 0
    galmesLDSylbl = [None]

    for j in range(0, 31):
        for i in range(0, len(fechamesLDSxlblF)):
            if j == fechamesLDSxlblF[i].day:
                galmesLDS2 = galLDSvec[i]
                galmesLDSacum2 = galmesLDSacum2 + galmesLDS2
                a = np.array(galmesLDSylbl)
                galmesLDSylbl = np.resize(a, j + 5)
                galmesLDSylbl[j] = galmesLDSacum2

        galmesLDSacum2 = 0  # dentro del j fuera del i

    # Calcula la turbidez, color y pH promedios de agua clarificada enviados por día en un mes
    colorCLRacum = 0
    turbCLRacum = 0
    pHCLRacum = 0
    cont = 0
    pHmesCLRylbl = [None]
    turbmesCLRylbl = [None]
    colormesCLRylbl = [None]
    conta = [None]

    for j in range(1, 31):
        for i in range(0, len(fechamesCLRxlblF)):
            if j == fechamesCLRxlblF[i].day :
                pHCLR = pHCLRvec[i]
                turbCLR = turbCLRvec[i]
                colorCLR = colorCLRvec[i]

                pHCLRacum = pHCLRacum + pHCLR
                turbCLRacum = turbCLRacum + turbCLR
                colorCLRacum = colorCLRacum + colorCLR
                cont = cont + 1

                a = np.array(pHmesCLRylbl)
                pHmesCLRylbl = np.resize(a, j + 5)

                b = np.array(turbmesCLRylbl)
                turbmesCLRylbl = np.resize(b, j + 5)

                c = np.array(colormesCLRylbl)
                colormesCLRylbl = np.resize(c, j + 5)

                d = np.array(conta)
                conta = np.resize(d, j + 5)

                pHmesCLRylbl[j] = pHCLRacum
                turbmesCLRylbl[j] = turbCLRacum
                colormesCLRylbl[j] = colorCLRacum
                conta[j] = cont

        colorCLRacum = 0
        turbCLRacum = 0
        pHCLRacum = 0
        cont = 0

    # Divide por el promedio
    for j in range(0, len(pHmesCLRylbl)):
        if conta[j] != None:
            pHmesCLRylbl[j] = pHmesCLRylbl[j] / conta[j]
            turbmesCLRylbl[j] = turbmesCLRylbl[j] / conta[j]
            colormesCLRylbl[j] = colormesCLRylbl[j] / conta[j]

    # Elimina los espacios vacíos de los vectores
    pHmesCLRylblF = [None]
    cont = 1
    for i in range(0, len(pHmesCLRylbl)):
        if pHmesCLRylbl[i] != None:
            a = np.array(pHmesCLRylblF)
            pHmesCLRylblF = np.resize(a, cont)

            pHmesCLRylblF[cont - 1] = pHmesCLRylbl[i]
            cont = cont + 1

    turbmesCLRylblF = [None]
    cont = 1
    for i in range(0, len(turbmesCLRylbl)):
        if turbmesCLRylbl[i] != None:
            a = np.array(turbmesCLRylblF)
            turbmesCLRylblF = np.resize(a, cont)

            turbmesCLRylblF[cont - 1] = turbmesCLRylbl[i]
            cont = cont + 1

    colormesCLRylblF = [None]
    cont = 1
    for i in range(0, len(colormesCLRylbl)):
        if colormesCLRylbl[i] != None:
            a = np.array(colormesCLRylblF)
            colormesCLRylblF = np.resize(a, cont)
            colormesCLRylblF[cont - 1] = colormesCLRylbl[i]
            cont = cont + 1

    galmesCLRylblF = [None]
    cont = 1
    for i in range(0, len(galmesCLRylbl)):
        if galmesCLRylbl[i] != None:
            a = np.array(galmesCLRylblF)
            galmesCLRylblF = np.resize(a, cont)

            galmesCLRylblF[cont - 1] = galmesCLRylbl[i]
            cont = cont + 1

    galmesLDSylblF = [None]
    cont = 1
    for i in range(0, len(galmesLDSylbl)):
        if galmesLDSylbl[i] != None:
            a = np.array(galmesLDSylblF)
            galmesLDSylblF = np.resize(a, cont)

            galmesLDSylblF[cont - 1] = galmesLDSylbl[i]
            cont = cont + 1

    # Elimina elementos repetidos
    fechamesCLRxlblF = list(dict.fromkeys(fechamesCLRxlblF))
    fechamesLDSxlblF = list(dict.fromkeys(fechamesLDSxlblF))

    # Cuenta los días trabajados en un mes
    diasMes = len(fechamesCLRxlblF)

    # Obtiene el flujo de entrada promedio del al clarificador
    fechaMes = value_mes
    fechaMes = float(fechaMes)
    for i in range(1, len(alCLRvec)):
        if fechaMes == i:
            galInCLR = alCLRvec[i]


    # Calcula el porcentaje de agua tratada proveniente de las purgas en el mes
    prctOutmes = 0.73
    galOutCLRmes = galInCLR * 60 * 24 * prctOutmes * 30.5
    prctaguatratmes = galmesCLRacum/ galOutCLRmes

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum = " gal"
    yaxis_label = "Volumen [gal]"
    if value_unidades == False:
        galmesLDSacum = galmesLDSacum / 264.72
        galmesCLRacum = galmesCLRacum / 264.72
        galmesLDSylblF = galmesLDSylblF / 264.72
        galmesCLRylblF = galmesCLRylblF / 264.72
        suffix_galdiaacum = " m3"
        yaxis_label = "Volumen [m3]"

    # Crea indicador de las purgas en un mes
    figpurgsmesLDS = go.Figure()
    figpurgsmesLDS.add_trace(go.Indicator(
        value=purgsmesLDS, ))

    figpurgsmesLDS.update_traces(number={"font": {"size": 18}})
    figpurgsmesLDS.update_layout(height=30, width=150)

    #print(purgsmesLDS)
    # Crea indicador del volumen captado en un mes
    figgalmesLDSacum = go.Figure()
    figgalmesLDSacum.add_trace(go.Indicator(
       value=galmesLDSacum,
        number={'suffix': suffix_galdiaacum},
    ))

    figgalmesLDSacum.update_traces(number={"font": {"size": 18}})
    figgalmesLDSacum.update_layout(height=30, width=150)

    # Crea indicador de los bombeos de clarificado en un mes
    figpurgsmesCLR = go.Figure()
    figpurgsmesCLR.add_trace(go.Indicator(
        value=purgsmesCLR, ))

    figpurgsmesCLR.update_traces(number={"font": {"size": 18}})
    figpurgsmesCLR.update_layout(height=30, width=150)

    # Crea indicador del volumen de clarificado retornado en un mes
    figgalmesCLRacum = go.Figure()
    figgalmesCLRacum.add_trace(go.Indicator(
        value=galmesCLRacum,
        number={'suffix': suffix_galdiaacum},
    ))

    figgalmesCLRacum.update_traces(number={"font": {"size": 18}})
    figgalmesCLRacum.update_layout(height=30, width=150)

    # Crea indicador del ph de agua clarificada retornada en un mes
    figpHmesCLRprom = go.Figure()
    figpHmesCLRprom.add_trace(go.Indicator(
        value=pHmesCLRprom, ))

    figpHmesCLRprom.update_traces(number={"font": {"size": 18}})
    figpHmesCLRprom.update_layout(height=30, width=150)

    # Crea indicador de la turbidez de agua clarificada retornada en un mes
    figturbmesCLRprom = go.Figure()
    figturbmesCLRprom.add_trace(go.Indicator(
        value=turbmesCLRprom, ))

    figturbmesCLRprom.update_traces(number={"font": {"size": 18}})
    figturbmesCLRprom.update_layout(height=30, width=150)

    # Crea indicador del color de agua clarificada retornada en un mes
    figcolormesCLRprom = go.Figure()
    figcolormesCLRprom.add_trace(go.Indicator(
        value=colormesCLRprom, ))

    figcolormesCLRprom.update_traces(number={"font": {"size": 18}})
    figcolormesCLRprom.update_layout(height=30, width=150)

    # Crea indicador de los días trabajados en un mes
    figdiasMes = go.Figure()
    figdiasMes.add_trace(go.Indicator(
        value=diasMes, ))

    figdiasMes.update_traces(number={"font": {"size": 18}})
    figdiasMes.update_layout(height=30, width=150)

    # Crea indicador del porcentaje de agua tratada de purgas en un mes
    figprctaguatratmes = go.Figure()
    figprctaguatratmes.add_trace(go.Indicator(
        value=prctaguatratmes*100,
        number={'suffix': "%"},
    ))

    figprctaguatratmes.update_traces(number={"font": {"size": 18}})
    figprctaguatratmes.update_layout(height=30, width=150)

    #print(fechamesCLRxlblF)
    #print(fechamesLDSxlblF)
    #print(galmesCLRylblF)
    #print(galmesLDSylblF)
    #Crea la figura de el volumen captado y retornado
    figmesvol = go.Figure()

    figmesvol.add_trace(go.Scatter(x=fechamesCLRxlblF, y=galmesCLRylblF, name="Volumen retornado de agua clarificada [gal]"))
    figmesvol.add_trace(go.Scatter(x=fechamesLDSxlblF, y=galmesLDSylblF, name="Volumen captado de agua lodosa [gal]"))
    figmesvol.update_layout(title="Agua Captada/Retornada", xaxis_title="Fecha", yaxis_title=yaxis_label)
    figmesvol.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    #Crea la figura de las propiedades de agua retornada
    figmesprop = go.Figure()
    figmesprop.add_trace(go.Scatter(x=fechamesCLRxlblF, y=pHmesCLRylblF, name="pH"))
    figmesprop.add_trace(go.Scatter(x=fechamesCLRxlblF, y=colormesCLRylblF, name="Color [Pt-Co]"))
    figmesprop.add_trace(go.Scatter(x=fechamesCLRxlblF, y=turbmesCLRylblF, name="Turbidez [NTU]"))
    figmesprop.update_layout(title="Propiedades de Agua Clarificada", xaxis_title="Fecha")
    figmesprop.update_layout(legend=dict(orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    #return figmesvol, figmesprop, \
    #       figpurgsmesLDS, figgalmesLDSacum, figpurgsmesCLR, figgalmesCLRacum, figpHmesCLRprom, figturbmesCLRprom, figcolormesCLRprom, \
    #       figdiasMes, figprctaguatratmes
    return figpurgsmesLDS, figgalmesLDSacum, figpurgsmesCLR, figgalmesCLRacum, figpHmesCLRprom, figturbmesCLRprom, figcolormesCLRprom, \
           figprctaguatratmes, figdiasMes, figmesvol, figmesprop



@app.callback(
    Output(component_id='purg-capt-acum', component_property="figure"),
    Output(component_id='vol-capt-acum', component_property="figure"),
    Output(component_id='bomb-acum', component_property="figure"),
    Output(component_id='vol-ret-acum', component_property="figure"),
    Output(component_id='pH-acum', component_property="figure"),
    Output(component_id='turb-acum', component_property="figure"),
    Output(component_id='color-acum', component_property="figure"),
    Output(component_id='dias-acum', component_property="figure"),
    Output(component_id='agua-trat-acum', component_property="figure"),
    Output(component_id='mi-acum-vol', component_property="figure"),
    Output(component_id='mi-acum-prop', component_property="figure"),
    Input(component_id='unidades-acum-input', component_property='value'),
)

def acum_interactivo(value_unidades): # Revisar porcentaje de agua tratada!!!
    # --------------------------------- Módulo 3 ------------------------------------------
    #print(value_unidades)
    # Calcula las purgas totales captadas
    purgtotLDS = len(galLDSvec)

    # Calcula los galones totales de agua lodosa captados
    galtotLDS = sum(galLDSvec)

    # Calcula los bombeos de clarificado totales
    bombtotCLR = len(galCLRvec)

    # Calcula los galones totales de clarificado retornados
    galtotCLR = sum(galCLRvec)

    # Calcula el pH de clarificado total acumulado promedio
    pHtotCLR = sum(pHCLRvec)/len(pHCLRvec)

    # Calcula la turbidez de clarificado total acumulado promedio
    turbtotCLR = sum(turbCLRvec) / len(turbCLRvec)

    # Calcula el color de clarificado total acumulado promedio
    colortotCLR = sum(colorCLRvec) / len(colorCLRvec)

    # Calcula los galones totales acumulados enviados por día

    cont = 0
    galCLRacum = 0
    galCLRylbl = [None]

    for k in range(1, 12):
        for j in range(1, 31):
            for i in range(0, len(fechaCLR)):
                if j == fechaCLR[i].day and k == fechaCLR[i].month:
                    galCLR = galCLRvec[i]
                    galCLRacum = galCLRacum + galCLR
                    a = np.array(galCLRylbl)
                    galCLRylbl = np.resize(a, cont)

                    galCLRylbl[cont - 1] = galCLRacum
                    # print(galCLRylbl)
            galCLRacum = 0
            cont = cont + 1

    # Calcula la turbidez, color y pH promedios de agua clarificada enviados por día acumulado
    colorCLRacum = 0
    turbCLRacum = 0
    pHCLRacum = 0
    contador = 0
    cont = 0
    pHCLRylbl = [None]
    turbCLRylbl = [None]
    colorCLRylbl = [None]
    conta = [None]

    for k in range(1, 12):
        for j in range(1, 31):
            for i in range(0, len(fechaCLR)):
                if j == fechaCLR[i].day and k == fechaCLR[i].month:
                    pHCLR = pHCLRvec[i]
                    turbCLR = turbCLRvec[i]
                    colorCLR = colorCLRvec[i]

                    pHCLRacum = pHCLRacum + pHCLR
                    turbCLRacum = turbCLRacum + turbCLR
                    colorCLRacum = colorCLRacum + colorCLR
                    contador = contador + 1

                    a = np.array(pHCLRylbl)
                    pHCLRylbl = np.resize(a, cont)

                    b = np.array(turbCLRylbl)
                    turbCLRylbl = np.resize(b, cont)

                    c = np.array(colorCLRylbl)
                    colorCLRylbl = np.resize(c, cont)

                    d = np.array(conta)
                    conta = np.resize(d, cont)

                    pHCLRylbl[cont - 1] = pHCLRacum
                    turbCLRylbl[cont - 1] = turbCLRacum
                    colorCLRylbl[cont - 1] = colorCLRacum
                    conta[cont - 1] = contador

            colorCLRacum = 0
            turbCLRacum = 0
            pHCLRacum = 0
            contador = 0
            cont = cont + 1

    # Calcula la turbidez, color y pH promedios de agua clarificada enviados por día acumulado
    colorCLRacum = 0
    turbCLRacum = 0
    pHCLRacum = 0
    contador = 0
    cont = 0
    pHCLRylbl = [None]
    turbCLRylbl = [None]
    colorCLRylbl = [None]
    conta = [None]

    for k in range(1, 12):
        for j in range(1, 31):
            for i in range(0, len(fechaCLR)):
                if j == fechaCLR[i].day and k == fechaCLR[i].month:
                    pHCLR = pHCLRvec[i]
                    turbCLR = turbCLRvec[i]
                    colorCLR = colorCLRvec[i]

                    pHCLRacum = pHCLRacum + pHCLR
                    turbCLRacum = turbCLRacum + turbCLR
                    colorCLRacum = colorCLRacum + colorCLR
                    contador = contador + 1

                    a = np.array(pHCLRylbl)
                    pHCLRylbl = np.resize(a, cont)

                    b = np.array(turbCLRylbl)
                    turbCLRylbl = np.resize(b, cont)

                    c = np.array(colorCLRylbl)
                    colorCLRylbl = np.resize(c, cont)

                    d = np.array(conta)
                    conta = np.resize(d, cont)

                    pHCLRylbl[cont - 1] = pHCLRacum
                    turbCLRylbl[cont - 1] = turbCLRacum
                    colorCLRylbl[cont - 1] = colorCLRacum
                    conta[cont - 1] = contador

            colorCLRacum = 0
            turbCLRacum = 0
            pHCLRacum = 0
            contador = 0
            cont = cont + 1

    # Divide por el promedio
    for j in range(0, len(pHCLRylbl)):
        if conta[j] != None:
            pHCLRylbl[j] = pHCLRylbl[j] / conta[j]
            turbCLRylbl[j] = turbCLRylbl[j] / conta[j]
            colorCLRylbl[j] = colorCLRylbl[j] / conta[j]

    # Calcula los galones totales captados por día acumulado

    # print(galLDSvec)
    cont = 0
    galLDSacum = 0
    galLDSylbl = [None]
    for k in range(1, 12):
        for j in range(1, 31):
            for i in range(0, len(fechaLDS)):
                if j == fechaLDS[i].day and k == fechaLDS[i].month:
                    galLDS = galLDSvec[i]
                    galLDSacum = galLDSacum + galLDS
                    a = np.array(galLDSylbl)
                    galLDSylbl = np.resize(a, cont)

                    galLDSylbl[cont - 1] = galLDSacum
                    # print(galCLRylbl)
            galLDSacum = 0
            cont = cont + 1

    # Elimina los espacios vacíos de los vectores
    galCLRylblF = [None]
    cont = 1
    for i in range(0, len(galCLRylbl)):
        if galCLRylbl[i] != None:
            a = np.array(galCLRylblF)
            galCLRylblF = np.resize(a, cont)

            galCLRylblF[cont - 1] = galCLRylbl[i]
            cont = cont + 1

    pHCLRylblF = [None]
    cont = 1
    for i in range(0, len(pHCLRylbl)):
        if pHCLRylbl[i] != None:
            a = np.array(pHCLRylblF)
            pHCLRylblF = np.resize(a, cont)

            pHCLRylblF[cont - 1] = pHCLRylbl[i]
            cont = cont + 1

    turbCLRylblF = [None]
    cont = 1
    for i in range(0, len(turbCLRylbl)):
        if turbCLRylbl[i] != None:
            a = np.array(turbCLRylblF)
            turbCLRylblF = np.resize(a, cont)

            turbCLRylblF[cont - 1] = turbCLRylbl[i]
            cont = cont + 1

    colorCLRylblF = [None]
    cont = 1
    for i in range(0, len(colorCLRylbl)):
        if colorCLRylbl[i] != None:
            a = np.array(colorCLRylblF)
            colorCLRylblF = np.resize(a, cont)

            colorCLRylblF[cont - 1] = colorCLRylbl[i]
            cont = cont + 1

    galLDSylblF = [None]
    cont = 1
    for i in range(0, len(galLDSylbl)):
        if galLDSylbl[i] != None:
            a = np.array(galLDSylblF)
            galLDSylblF = np.resize(a, cont)

            galLDSylblF[cont - 1] = galLDSylbl[i]
            cont = cont + 1

    # Elimina elementos repetidos
    fechaCLR2 = list(dict.fromkeys(fechaCLR))
    fechaLDS2 = list(dict.fromkeys(fechaLDS))

    # Obtiene el flujo de entrada promedio del al clarificador
    galInCLRacum = 2527  # [GPM]

    #Calcula la diferencia entre el último y el primer día trabajado
    datediff = fechaCLR2[-1] - fechaCLR2[0]
    datediff = datediff.days

    # Calcula el porcentaje de agua tratada de las purgas acumulado
    prctOutacum = 0.73
    galOutCLRacum = galInCLRacum * 60 * 24 * prctOutacum * datediff
    prctaguatratacum = galtotCLR / galOutCLRacum

    # Cuenta los días trabajados acumulados
    diasacum = len(fechaCLR2)

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum = " gal"
    yaxis_label = "Volumen [gal]"
    if value_unidades == False:
        galtotLDS = galtotLDS / 264.72
        galtotCLR = galtotCLR / 264.72
        galCLRylblF = galCLRylblF / 264.72
        galLDSylblF = galLDSylblF / 264.72
        suffix_galdiaacum = " m3"
        yaxis_label = "Volumen [m3]"

    # Crea la figura de el volumen captado y retornado
    figacumvol = go.Figure()

    figacumvol.add_trace(go.Scatter(x=fechaCLR2, y=galCLRylblF, name="Volumen retornado de agua clarificada [gal]"))
    figacumvol.add_trace(go.Scatter(x=fechaLDS2, y=galLDSylblF, name="Volumen captado de agua lodosa [gal]"))
    figacumvol.update_layout(title="Agua Captada/Retornada Acumulado", xaxis_title="Fecha",
                             yaxis_title=yaxis_label)
    figacumvol.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    # Crea la figura de las propiedades de agua retornada
    figacumprop = go.Figure()
    figacumprop.add_trace(go.Scatter(x=fechaCLR2, y=pHCLRylblF, name="pH"))
    figacumprop.add_trace(go.Scatter(x=fechaCLR2, y=colorCLRylblF, name="Color [Pt-Co]"))
    figacumprop.add_trace(go.Scatter(x=fechaCLR2, y=turbCLRylblF, name="Turbidez [NTU]"))
    figacumprop.update_layout(title="Propiedades de Agua Clarificada", xaxis_title="Fecha")
    figacumprop.update_layout(legend=dict(orientation="h",
                                            yanchor="bottom",
                                            y=-0.5,
                                            xanchor="center",
                                            x=0.5
                                            ))


    # Crea indicador de las purgas en un acumulado
    figpurgtotLDS = go.Figure()
    figpurgtotLDS.add_trace(go.Indicator(
        value=purgtotLDS, ))

    figpurgtotLDS.update_traces(number={"font": {"size": 18}})
    figpurgtotLDS.update_layout(height=30, width=150)

    # Crea indicador del volumen captado en un acumulado
    figgaltotLDS = go.Figure()
    figgaltotLDS.add_trace(go.Indicator(
        value=galtotLDS,
        number={'suffix': suffix_galdiaacum},
    ))

    figgaltotLDS.update_traces(number={"font": {"size": 18}})
    figgaltotLDS.update_layout(height=30, width=150)

    # Crea indicador de los bombeos de clarificado en un acumulado
    figbombtotCLR = go.Figure()
    figbombtotCLR.add_trace(go.Indicator(
        value=bombtotCLR, ))

    figbombtotCLR.update_traces(number={"font": {"size": 18}})
    figbombtotCLR.update_layout(height=30, width=150)

    # Crea indicador del volumen de clarificado retornado en un acumulado
    figgaltotCLR = go.Figure()
    figgaltotCLR.add_trace(go.Indicator(
        value=galtotCLR,
        number={'suffix': suffix_galdiaacum},
    ))

    figgaltotCLR.update_traces(number={"font": {"size": 18}})
    figgaltotCLR.update_layout(height=30, width=150)

    # Crea indicador del ph de agua clarificada retornada en un acumulado
    figpHtotCLR = go.Figure()
    figpHtotCLR.add_trace(go.Indicator(
        value=pHtotCLR, ))

    figpHtotCLR.update_traces(number={"font": {"size": 18}})
    figpHtotCLR.update_layout(height=30, width=150)

    # Crea indicador de la turbidez de agua clarificada retornada en un acumulado
    figturbtotCLR = go.Figure()
    figturbtotCLR.add_trace(go.Indicator(
        value=turbtotCLR, ))

    figturbtotCLR.update_traces(number={"font": {"size": 18}})
    figturbtotCLR.update_layout(height=30, width=150)

    # Crea indicador del color de agua clarificada retornada en un acumulado
    figcolortotCLR = go.Figure()
    figcolortotCLR.add_trace(go.Indicator(
        value=colortotCLR, ))

    figcolortotCLR.update_traces(number={"font": {"size": 18}})
    figcolortotCLR.update_layout(height=30, width=150)

    # Crea indicador de los días trabajados acumulados
    figdiasacum = go.Figure()
    figdiasacum.add_trace(go.Indicator(
        value=diasacum, ))

    figdiasacum.update_traces(number={"font": {"size": 18}})
    figdiasacum.update_layout(height=30, width=150)


    # Crea indicador del porcentaje de agua tratada de purgas acumulado
    figprctaguatratacum = go.Figure()
    figprctaguatratacum.add_trace(go.Indicator(
        value=prctaguatratacum*100,
        number={'suffix': "%"},
    ))

    figprctaguatratacum.update_traces(number={"font": {"size": 18}})
    figprctaguatratacum.update_layout(height=30, width=150)

    #return figacumvol, figacumprop,\
    #       figpurgtotLDS, figgaltotLDS, figbombtotCLR, figgaltotCLR, figpHtotCLR, figturbtotCLR, figcolortotCLR, \
    #       figdiasacum, figprctaguatratacum

    return figpurgtotLDS, figgaltotLDS, figbombtotCLR, figgaltotCLR, figpHtotCLR, figturbtotCLR, figcolortotCLR, \
           figdiasacum, figprctaguatratacum, figacumvol, figacumprop # porcentaje de agua tratada



@app.callback(
    Output(component_id='purg-capt-fase', component_property="figure"),
    Output(component_id='vol-capt-fase', component_property="figure"),
    Output(component_id='bomb-fase', component_property="figure"),
    Output(component_id='vol-ret-fase', component_property="figure"),
    Output(component_id='pH-fase', component_property="figure"),
    Output(component_id='turb-fase', component_property="figure"),
    Output(component_id='color-fase', component_property="figure"),
    Output(component_id='dias-fase', component_property="figure"),
    Output(component_id='agua-trat-fase', component_property="figure"),
    Output(component_id='mi-fase-vol', component_property="figure"),
    Output(component_id='mi-fase-prop', component_property="figure"),

    Input(component_id='unidades-fase-input', component_property='value'),
    Input(component_id='fase', component_property='value'),
)

def fase_interactivo(value_unidades, value_fase):
    #print(value_unidades)
    print(value_fase)
    fase = value_fase

    faseVecLDS = dfLDS["Fase"]
    galtotLDS = []
    # Calcula las purgas captadas para una fase determinada & volumen [gal] total para una fase determinada
    for i in range(0, len(faseVecLDS)):
        if fase == faseVecLDS[i]:
            y = galLDSvec[i]
            galtotLDS.append(y)

    purgfaseLDS = len(galtotLDS)
    galtotLDS = sum(galtotLDS)

    #print(purgfaseLDS) # Correcto
    #print(galfaseLDSacum) # Correcto

    # Calcula los bombeos de clarificado para una fase determinada & volumen [gal] total de bombeo de clarificado para una fase determinada & turbidez, color y pH de agua clarificada para un día determinado
    faseVecCLR = dfCLR["Fase"]
    galtotCLR = []
    pHfaseCLR = []
    turbfaseCLR = []
    colorfaseCLR = []

    for i in range(0, len(faseVecCLR)):
        if fase == faseVecCLR[i]:
            y = galCLRvec[i]
            galtotCLR.append(y)

            p = pHCLRvec[i]
            pHfaseCLR.append(p)

            t = turbCLRvec[i]
            turbfaseCLR.append(t)

            c = colorCLRvec[i]
            colorfaseCLR.append(c)

    bombfaseCLR = len(galtotCLR)
    galtotCLR = sum(galtotCLR)

    pHfaseCLRprom = sum(pHfaseCLR)/len(pHfaseCLR)
    turbfaseCLRprom = sum(turbfaseCLR)/len(turbfaseCLR)
    colorfaseCLRprom = sum(colorfaseCLR)/len(colorfaseCLR)

    #print(bombfaseCLR) # correcto
    #print(galtotCLR) # correcto
    #print(pHfaseCLRprom) # correcto
    #print(turbfaseCLRprom) # correcto
    #print(colorfaseCLRprom) # correcto

    # Toma los días de un mes de galones de clarificado y turbidez, color y pH
    dffaseCLRxlbl = dfCLR[dfCLR.Fase == fase]
    indx = dffaseCLRxlbl.index
    indx = indx[0]
    dffaseCLRxlbl = dffaseCLRxlbl.rename(index=lambda x: x-indx)
    fechafaseCLRxlbl = dffaseCLRxlbl["Fecha"]
    #print(fechafaseCLRxlbl) # correcto


    # Toma los días de un mes de volumen de purgas captadas
    dffaseLDSxlbl = dfLDS[dfLDS.Fase == fase]
    indx = dffaseLDSxlbl.index
    indx = indx[0]
    dffaseLDSxlbl = dffaseLDSxlbl.rename(index=lambda x: x-indx)
    fechafaseLDSxlbl = dffaseLDSxlbl["Fecha"]
    #print(fechafaseLDSxlbl) # correcto

    # Calcula los galones totales de fase enviados por día INCORRECTO

    cont = 0
    galCLRacum = 0
    galCLRylbl = [None]
    galfaseCLRvec = dffaseCLRxlbl["Volumen [gal]"]
    #print(fechafaseCLRxlbl)
    #print(galfaseCLRvec)
    #print(fechafaseCLRxlbl[1])
    #print(type(fechafaseCLRxlbl[1]))

    for k in range(1, 12):
        for j in range(1, 31):
            for i in range(0, len(fechafaseCLRxlbl)):
                if j == fechafaseCLRxlbl[i].day and k == fechafaseCLRxlbl[i].month:
                    galCLR = galfaseCLRvec[i] # Aquí está el problema. No es galCLRvec
                    galCLRacum = galCLRacum + galCLR

                    a = np.array(galCLRylbl)
                    galCLRylbl = np.resize(a, cont)

                    galCLRylbl[cont - 1] = galCLRacum
            galCLRacum = 0
            cont = cont + 1

    #print(galCLRylbl) # correcto

    # Calcula la turbidez, color y pH promedios de agua clarificada enviados por día acumulado
    colorCLRacum = 0
    turbCLRacum = 0
    pHCLRacum = 0
    contador = 0
    cont = 0
    pHCLRylbl = [None]
    turbCLRylbl = [None]
    colorCLRylbl = [None]
    conta = [None]

    pHfaseCLRvec = dffaseCLRxlbl["pH"]
    turbfaseCLRvec = dffaseCLRxlbl["Turbidez [NTU]"]
    colorfaseCLRvec = dffaseCLRxlbl["Color [Pt-Co]"]

    for k in range(1, 12):
        for j in range(1, 31):
            for i in range(0, len(fechafaseCLRxlbl)):
                if j == fechafaseCLRxlbl[i].day and k == fechafaseCLRxlbl[i].month:
                    pHCLR = pHfaseCLRvec[i]
                    turbCLR = turbfaseCLRvec[i]
                    colorCLR = colorfaseCLRvec[i]

                    pHCLRacum = pHCLRacum + pHCLR
                    turbCLRacum = turbCLRacum + turbCLR
                    colorCLRacum = colorCLRacum + colorCLR
                    contador = contador + 1

                    a = np.array(pHCLRylbl)
                    pHCLRylbl = np.resize(a, cont)

                    b = np.array(turbCLRylbl)
                    turbCLRylbl = np.resize(b, cont)

                    c = np.array(colorCLRylbl)
                    colorCLRylbl = np.resize(c, cont)

                    d = np.array(conta)
                    conta = np.resize(d, cont)

                    pHCLRylbl[cont - 1] = pHCLRacum
                    turbCLRylbl[cont - 1] = turbCLRacum
                    colorCLRylbl[cont - 1] = colorCLRacum
                    conta[cont - 1] = contador

            colorCLRacum = 0
            turbCLRacum = 0
            pHCLRacum = 0
            contador = 0
            cont = cont + 1

    # Divide por el promedio
    for j in range(0, len(pHCLRylbl)):
        if conta[j] != None:
            pHCLRylbl[j] = pHCLRylbl[j] / conta[j]
            turbCLRylbl[j] = turbCLRylbl[j] / conta[j]
            colorCLRylbl[j] = colorCLRylbl[j] / conta[j]

    #print(pHCLRylbl) # correcto
    #print(turbCLRylbl) # correcto
    #print(colorCLRylbl) # correcto

    # Calcula los galones totales captados por día acumulado INCORRECTO

    # print(galLDSvec)
    cont = 0
    galLDSacum = 0
    galLDSylbl = [None]
    galfaseLDSvec = dffaseLDSxlbl["Volumen [gal]"]
    for k in range(1, 12):
        for j in range(1, 31):
            for i in range(0, len(fechafaseLDSxlbl)):
                if j == fechafaseLDSxlbl[i].day and k == fechafaseLDSxlbl[i].month:
                    galLDS = galfaseLDSvec[i]
                    galLDSacum = galLDSacum + galLDS
                    a = np.array(galLDSylbl)
                    galLDSylbl = np.resize(a, cont)

                    galLDSylbl[cont - 1] = galLDSacum
                    # print(galCLRylbl)
            galLDSacum = 0
            cont = cont + 1

    #print(galLDSylbl) # correcto

    # Elimina espacios vacíos de los vectores
    galLDSylblF = []
    for i in range(0, len(galLDSylbl)):
        if galLDSylbl[i] != None:
            x = galLDSylbl[i]
            galLDSylblF.append(x)

    galCLRylblF = []
    for i in range(0, len(galCLRylbl)):
        if galCLRylbl[i] != None:
            x = galCLRylbl[i]
            galCLRylblF.append(x)

    pHCLRylblF = []
    for i in range(0, len(pHCLRylbl)):
        if pHCLRylbl[i] != None:
            x = pHCLRylbl[i]
            pHCLRylblF.append(x)

    turbCLRylblF = []
    for i in range(0, len(turbCLRylbl)):
        if turbCLRylbl[i] != None:
            x = turbCLRylbl[i]
            turbCLRylblF.append(x)

    colorCLRylblF = []
    for i in range(0, len(colorCLRylbl)):
        if colorCLRylbl[i] != None:
            x = colorCLRylbl[i]
            colorCLRylblF.append(x)

    # Elimina elementos repetidos
    fechafaseCLRxlblF = list(dict.fromkeys(fechafaseCLRxlbl))
    fechafaseLDSxlblF = list(dict.fromkeys(fechafaseLDSxlbl))

    #print(fechafaseLDSxlblF)
    #print(fechafaseCLRxlblF)
    #print(galLDSylblF)  # correcto
    #print(galCLRylblF)
    #print(pHCLRylblF)
    #print(turbCLRylblF)
    #print(colorCLRylblF)

    # Cuenta los días trabajados en una fase
    diasfase = len(fechafaseCLRxlblF)

    # Obtiene el flujo de entrada promedio del al clarificador
    galInCLRacum = 2527  # [GPM]

    #Calcula la diferencia entre el último y el primer día trabajado
    datediff = fechafaseCLRxlblF[-1] - fechafaseCLRxlblF[0]
    datediff = datediff.days
    #print(datediff) # correcto

    # Calcula el porcentaje de agua tratada de las purgas en una fase
    prctOutacum = 0.73
    galOutCLRacum = galInCLRacum * 60 * 24 * prctOutacum * datediff
    prctaguatratacum = galtotCLR / galOutCLRacum

    #print(prctaguatratacum) # correcto

    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum = " gal"
    yaxis_label = "Volumen [gal]"
    if value_unidades == False:
        galtotLDS = galtotLDS / 264.72
        galtotCLR = galtotCLR / 264.72
        galCLRylblF = galCLRylblF / 264.72
        galLDSylblF = galLDSylblF / 264.72
        suffix_galdiaacum = " m3"
        yaxis_label = "Volumen [m3]"


    # Crea la figura de el volumen captado y retornado
    figacumvol = go.Figure()

    figacumvol.add_trace(go.Scatter(x=fechafaseCLRxlblF, y=galCLRylblF, name="Volumen retornado de agua clarificada [gal]"))
    figacumvol.add_trace(go.Scatter(x=fechafaseLDSxlblF, y=galLDSylblF, name="Volumen captado de agua lodosa [gal]"))
    figacumvol.update_layout(title="Agua Captada/Retornada Acumulado", xaxis_title="Fecha",
                             yaxis_title=yaxis_label)
    figacumvol.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))


    # Crea la figura de las propiedades de agua retornada
    figacumprop = go.Figure()
    figacumprop.add_trace(go.Scatter(x=fechafaseCLRxlblF, y=pHCLRylblF, name="pH"))
    figacumprop.add_trace(go.Scatter(x=fechafaseCLRxlblF, y=colorCLRylblF, name="Color [Pt-Co]"))
    figacumprop.add_trace(go.Scatter(x=fechafaseCLRxlblF, y=turbCLRylblF, name="Turbidez [NTU]"))
    figacumprop.update_layout(title="Propiedades de Agua Clarificada", xaxis_title="Fecha")
    figacumprop.update_layout(legend=dict(orientation="h",
                                            yanchor="bottom",
                                            y=-0.5,
                                            xanchor="center",
                                            x=0.5
                                            ))


    # Crea indicador de las purgas en una fase
    figpurgtotLDS = go.Figure()
    figpurgtotLDS.add_trace(go.Indicator(
        value=purgfaseLDS, ))

    figpurgtotLDS.update_traces(number={"font": {"size": 18}})
    figpurgtotLDS.update_layout(height=30, width=150)

    # Crea indicador del volumen captado en una fase
    figgaltotLDS = go.Figure()
    figgaltotLDS.add_trace(go.Indicator(
        value=galtotLDS,
        number={'suffix': suffix_galdiaacum},
    ))

    figgaltotLDS.update_traces(number={"font": {"size": 18}})
    figgaltotLDS.update_layout(height=30, width=150)

    # Crea indicador de los bombeos de clarificado en una fase
    figbombtotCLR = go.Figure()
    figbombtotCLR.add_trace(go.Indicator(
        value=bombfaseCLR, ))

    figbombtotCLR.update_traces(number={"font": {"size": 18}})
    figbombtotCLR.update_layout(height=30, width=150)

    # Crea indicador del volumen de clarificado retornado en una fase
    figgaltotCLR = go.Figure()
    figgaltotCLR.add_trace(go.Indicator(
        value=galtotCLR,
        number={'suffix': suffix_galdiaacum},
    ))

    figgaltotCLR.update_traces(number={"font": {"size": 18}})
    figgaltotCLR.update_layout(height=30, width=150)


    # Crea indicador del ph de agua clarificada retornada en un acumulado
    figpHtotCLR = go.Figure()
    figpHtotCLR.add_trace(go.Indicator(
        value=pHfaseCLRprom, ))

    figpHtotCLR.update_traces(number={"font": {"size": 18}})
    figpHtotCLR.update_layout(height=30, width=150)

    # Crea indicador de la turbidez de agua clarificada retornada en un acumulado
    figturbtotCLR = go.Figure()
    figturbtotCLR.add_trace(go.Indicator(
        value=turbfaseCLRprom, ))

    figturbtotCLR.update_traces(number={"font": {"size": 18}})
    figturbtotCLR.update_layout(height=30, width=150)


    # Crea indicador del color de agua clarificada retornada en un acumulado
    figcolortotCLR = go.Figure()
    figcolortotCLR.add_trace(go.Indicator(
        value=colorfaseCLRprom, ))

    figcolortotCLR.update_traces(number={"font": {"size": 18}})
    figcolortotCLR.update_layout(height=30, width=150)

    # Crea indicador de los días trabajados acumulados
    figdiasacum = go.Figure()
    figdiasacum.add_trace(go.Indicator(
        value=diasfase, ))

    figdiasacum.update_traces(number={"font": {"size": 18}})
    figdiasacum.update_layout(height=30, width=150)


    # Crea indicador del porcentaje de agua tratada de purgas acumulado
    figprctaguatratacum = go.Figure()
    figprctaguatratacum.add_trace(go.Indicator(
        value=prctaguatratacum*100,
        number={'suffix': "%"},
    ))

    figprctaguatratacum.update_traces(number={"font": {"size": 18}})
    figprctaguatratacum.update_layout(height=30, width=150)

    return figpurgtotLDS, figgaltotLDS, figbombtotCLR, figgaltotCLR, figpHtotCLR, figturbtotCLR, figcolortotCLR, \
           figdiasacum, figprctaguatratacum, figacumvol, figacumprop,


@app.callback(
    Output('fechaGTDD', 'options'),
    Input(component_id='numGTDD', component_property='value'),
)

def Num_Geotube_interactivo(value_numGT):
    dff = dfGT_GD[dfGT_GD.Numero==value_numGT]
    dff = dff["Fecha"]
    fecha_selec_str = []
    for x in dff:
        d = str(x.day)
        m = str(x.month)
        y = str(x.year)
        s = d + "/" + m + "/" + y
        fecha_selec_str.append(s)

    return [{'label':c, 'value':c} for c in fecha_selec_str]

@app.callback(
    Output('fechaGTDD', 'value'),
    Input('fechaGTDD', 'options'),
)

def set_Geotube_fecha_value(fecha_selec):
    x = fecha_selec[0]
    x = x["value"]
    y = datetime.strptime(x, "%d/%m/%Y")
    return x
    #return [{'label':c, 'value':c} for c in x]

@app.callback(
    Output(component_id='num-GT', component_property="figure"),
    Output(component_id='uso-GT', component_property="figure"),
    Output(component_id='cap-GT', component_property="figure"),

    Output(component_id='vol-GT', component_property="figure"),
    Output(component_id='peso-GT', component_property="figure"),
    Output(component_id='fig-GT', component_property="figure"),
    Output(component_id='fig-uso-GT', component_property="figure"),

    Input('fechaGTDD', 'value'),
    Input('numGTDD', 'value'),
    Input('unidades-GT-input', 'value'),


)

def Geotube_interactivo(value_fechaGT, value_numGT, value_unidades):
    # --------------------------------- Módulo 4 ------------------------------------------



    numGT = value_numGT
    diaGT = value_fechaGT

    # Determina la capacidad del Geotube
    for i in range(0, len(numGTvec)):
        if numGT == numGTvec[i]:
            capGT = capGTvec[i]

    #print(numGT)
    #print(diaGT)

    # Convierte a tipo numérico
    numGT = float(numGT)

    # Convierte a tipo fecha
    diaGT = datetime.strptime(diaGT, "%d/%m/%Y")



    # Determina % uso, volumen y pes del Geotube en un día seleccionado
    for i in range(0, len(numGTvec)):
        if numGT == numGTvec[i] and diaGT == fechaGT[i]:
            prctUso = usoGTvec[i]
            volGT = m3GTvec[i]
            pesoGT = pesoGTvec[i]
    #print(prctUso)
    #print(volGT)
    #print(pesoGT)
    # Crea vector para graficar volumen, peso y uso de un determinado Geotube
    volGTvecF = [None]
    pesoGTvecF = [None]
    usoGTvecF = [None]
    fechaGTvecF = [None]

    for i in range(0, len(numGTvec)):
        if numGT == numGTvec[i]:
            a = np.array(volGTvecF)
            volGTvecF = np.resize(a, i + 1)

            b = np.array(pesoGTvecF)
            pesoGTvecF = np.resize(b, i + 1)

            c = np.array(usoGTvecF)
            usoGTvecF = np.resize(c, i + 1)

            d = np.array(fechaGTvecF)
            fechaGTvecF = np.resize(d, i + 1)

            volGTvecF[i] = m3GTvec[i]
            pesoGTvecF[i] = pesoGTvec[i]
            usoGTvecF[i] = usoGTvec[i]
            fechaGTvecF[i] = fechaGT[i]

    #usoGTvecF = usoGTvecF*100
    # Cambia unidades a m3 por radioitem
    suffix_galdiaacum = " gal"
    yaxis_label = "Volumen del Geotube [gal]"
    if value_unidades == False:
        capGT = capGT / 264.72
        volGT = volGT / 264.72
        volGTvecF = volGTvecF / 264.72
        #galLDSylblF = galLDSylblF / 264.72
        suffix_galdiaacum = " m3"
        yaxis_label = "Volumen del Geotube [m3]"


    # Crea la figura de peso y volumen del Geotube
    figGT = go.Figure()

    figGT.add_trace(go.Scatter(x=fechaGTvecF, y=volGTvecF, name="Volumen del Geotube [m3]"))
    figGT.add_trace(go.Scatter(x=fechaGTvecF, y=pesoGTvecF, name="Peso del Geotube [Ton]"))
    figGT.update_layout(title="Peso y Volumen del Geotube", xaxis_title="Fecha",
                             yaxis_title="")
    figGT.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))



    # Crea la figura de porcentaje de uso del Geotube
    #print(usoGTvecF)
    #print(type(usoGTvecF[0]))
    #print(type(usoGTvecF[1]))

    for i in range(0, len(usoGTvecF)):
        if usoGTvecF[i] != None:
            usoGTvecF[i] = usoGTvecF[i] * 100
            usoGTvecF[i] = float(usoGTvecF[i])
    #usoGTvecF = usoGTvecF*100
    figusoGT = go.Figure()

    figusoGT.add_trace(go.Scatter(x=fechaGTvecF, y=usoGTvecF))
    figusoGT.update_layout(title="Uso del Geotube", xaxis_title="Fecha",
                        yaxis_title="Uso [%]")
    figusoGT.update_layout(legend=dict(
        yanchor="bottom",
        y=-0.5,
        xanchor="center",
        x=0.5
    ))

    # Crea indicador del número del Geotube
    fignumGT = go.Figure()
    fignumGT.add_trace(go.Indicator(
        value=numGT, ))

    fignumGT.update_traces(number={"font": {"size": 18}})
    fignumGT.update_layout(height=30, width=70)

    # Crea indicador de la capacidad del Geotube
    figcapGT = go.Figure()
    figcapGT.add_trace(go.Indicator(
        value=capGT, ))

    figcapGT.update_traces(number={"font": {"size": 18}})
    figcapGT.update_layout(height=30, width=70)

    # Crea indicador del porcentaje de uso de un Geotubo para un día seleccionado
    figprctUso = go.Figure()
    figprctUso.add_trace(go.Indicator(
        value=prctUso*100,
        number={'suffix': "%"},))

    figprctUso.update_traces(number={"font": {"size": 18}})
    figprctUso.update_layout(height=30, width=70)

    # Crea indicador del volumen de un Geotubo para un día seleccionado en m3
    figvolGT = go.Figure()
    figvolGT.add_trace(go.Indicator(
        value=volGT, ))

    figvolGT.update_traces(number={"font": {"size": 18}})
    figvolGT.update_layout(height=30, width=70)

    # Crea indicador del peso de un Geotubo para un día seleccionado en ton
    figpesoGT = go.Figure()
    figpesoGT.add_trace(go.Indicator(
        value=pesoGT, ))

    figpesoGT.update_traces(number={"font": {"size": 18}})
    figpesoGT.update_layout(height=30, width=70)

    #return fignumGT, figcapGT, figprctUso, figvolGT, figpesoGT, figGT, figusoGT
    return fignumGT, figprctUso, figcapGT, figvolGT, figpesoGT, figGT, figusoGT



if __name__ == '__main__':
    app.run_server()

