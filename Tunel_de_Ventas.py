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
from datetime import date
import plotly.express as px
import dash_auth



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
#app.css.append_css({'external_url': '/static/reset.css'})
#app.server.static_folder = 'static'
server = app.server

#auth = dash_auth.BasicAuth(
#    app,
#    {'MONICA': 'GERENTE',
#     'LUISA': 'COMERCIAL',
#     'NELSY': 'COMERCIAL',
#     'ADRIANA': 'GERENTE',
#     }
#)



data = [['3/11/2020', '9:32:00 a. m.', '9:34:00 a. m.', '0.8', '1']]
data = [['3/11/2020', '9:32:00 a. m.', '9:34:00 a. m.', '0.8', '1', '2', '0.8', '211.3376', '303.2', '80096.9504', '344', '124', '1'], ['3/11/2020', '9:47:00 a. m.', '9:48:00 a. m.', '1.1', '1.8', '1', '2.8', '739.6816', '307.2', '81153.6384', '347', '126', '1'], ['3/11/2020', '9:55:00 a. m.', '9:57:00 a. m.', '1.8', '2.2', '2', '1.6', '422.6752', '308.8', '81576.3136', '349', '127', '1']]
data = [['Borrar!', 'Borrar!', 'Borrar!', 'Borrar!', 'Borrar!', 'Borrar!']]
data = []


app.layout = dbc.Container([
    dcc.Store(id='store-data-df_ventas', storage_type='memory'),  # 'local' or 'session'
    dcc.Store(id='store-data-df_oportunidades-tabla', storage_type='memory'),  # 'local' or 'session'
    dcc.Store(id='store-data-df_ofertas-tabla', storage_type='memory'),  # 'local' or 'session'
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
                   'text-align': 'center'},
        ),
        ]),
        dbc.Col(html.H5('"Cualquier tecnología lo suficientemente avanzada, es indistinguible de la magia." - Arthur C. Clarke '),style={'color':"green", 'font-family': "Franklin Gothic"})
    ]),
    dbc.Row([
        dbc.Tabs([
            dbc.Tab([
                dbc.Row([
                    dbc.Col(html.H1(
                        "Túnel de Ventas",
                        style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"}),
                        width=12, )
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Seleccionar Representante Comercial:",
                            id="selec-agente-target",
                            value='Ventas Geo',
                            color="info",
                            style={'font-family': "Franklin Gothic"},
                            # className="me-1",
                            n_clicks=0,
                        ),
                    ], xs=3, sm=3, md=3, lg=4, xl=4, align='center'),

                    dbc.Col([
                        dcc.Dropdown(id='Agente',
                                     options=[],
                                     #value='Todos',
                                     style={'font-family': "Franklin Gothic"}
                                     )
                    ], xs=3, sm=3, md=3, lg=4, xl=4, align='center'),
                ]),
                dbc.Row(dbc.Col(
                    dbc.Spinner(children=[dcc.Graph(id="embudo")], size="lg",
                                color="primary", type="border", fullscreen=True, ),
                    width={'size': 12, 'offset': 0}),
                ),
                dbc.Row(dbc.Col(
                    dbc.Spinner(children=[dcc.Graph(id="fig-pie-potencial")], size="lg",
                                color="primary", type="border", fullscreen=True, ),
                    width={'size': 12, 'offset': 0}),
                ),
                dbc.Row(dbc.Col(
                    dbc.Spinner(children=[dcc.Graph(id="fig-pie-cantidad")], size="lg",
                                color="primary", type="border", fullscreen=True, ),
                    width={'size': 12, 'offset': 0}),
                ),

            ], label="Túnel de Ventas", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row([
                    dbc.Col(html.H1(
                        "Resumen Prospecto",
                        style={'textAlign': 'center', 'color': '#082255', 'font-family': "Franklin Gothic"}),
                        width=12, )
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button(
                            "Seleccionar Prospecto:",
                            id="selec-uni-dia-target",
                            color="info",
                            style={'font-family': "Franklin Gothic"},
                            # className="me-1",
                            n_clicks=0,
                        ),
                    ], xs=3, sm=3, md=3, lg=3, xl=3, align='center'),

                    dbc.Col([
                        dcc.Dropdown(id='Estado',
                                     options=[],
                                     value='Leads',
                                     style={'font-family': "Franklin Gothic"}
                                     )
                    ], xs=3, sm=3, md=3, lg=2, xl=2, align='center'),
                ]),
                dbc.Row(dbc.Col(
                    dbc.Spinner(children=[dcc.Graph(id="fig-potencial")], size="lg",
                                color="primary", type="border", fullscreen=True, ),
                    width={'size': 12, 'offset': 0}),
                ),
                dbc.Row(dbc.Col(
                    dbc.Spinner(children=[dcc.Graph(id="fig-potencial-cantidad")], size="lg",
                                color="primary", type="border", fullscreen=True, ),
                    width={'size': 12, 'offset': 0}),
                ),

            ], label="Resumen Prospecto", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row(dbc.Col(
                    dbc.Spinner(children=[dcc.Graph(id="fig-potencial2")], size="lg",
                                color="primary", type="border", fullscreen=True, ),
                    width={'size': 12, 'offset': 0}),
                ),
                dbc.Row(dbc.Col(
                    dbc.Spinner(children=[dcc.Graph(id="fig-potencial-cantidad2")], size="lg",
                                color="primary", type="border", fullscreen=True, ),
                    width={'size': 12, 'offset': 0}),
                ),
            ], label="Resumen Potenciales", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),
            dbc.Tab([
                dbc.Row(
                    dash_table.DataTable(
                        id='datatable-df_oportunidades-tabla',
                        columns=[
                            {"name": "Asunto", "id": 1, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Numero OP", "id": 2, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Estado oportunidad", "id": 3, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Estado avance", "id": 4, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Porcentaje avance", "id": 5, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Visión vendedor", "id": 6, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "% visión vendedor", "id": 7, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Cuenta", "id": 8, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Asignada a", "id": 9, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Tipo oportunidad", "id": 10, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Categoría oportunidad", "id": 11, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Unidad de negocio", "id": 12, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Linea", "id": 13, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Sublinea", "id": 14, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Fuente", "id": 15, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Valor venta estimado", "id": 16, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Periodo de venta", "id": 17, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Fecha estimada cierre", "id": 18, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Trimestre estimado cierre", "id": 19, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Situacion actual", "id": 20, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Entendimiento necesidad cliente", "id": 21, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Solucion propuesta", "id": 22, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Estado proceso comercial", "id": 23, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Razón perdida/cancelada", "id": 24, "deletable": False, "selectable": False, "hideable": True},



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
                            'height': 'auto',
                            'font-family': "Franklin Gothic",
                            'textAlign': 'center',
                        },
                        style_header={
                            'font-family': "Franklin Gothic",
                            'textAlign': 'center',
                            'fontWeight': 'bold'
                        },

                    )
                ),

                dbc.Row(
                    dash_table.DataTable(
                        id='datatable-df_ofertas-tabla',
                        columns=[
                            {"name": "Número oferta", "id": 1, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Estado oferta", "id": 2, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Fecha oferta", "id": 3, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Asunto", "id": 4, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Tipo oferta", "id": 5, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Cuenta", "id": 6, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Contacto", "id": 7, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Representante comercial", "id": 8, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Total", "id": 9, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Unidad de negocio", "id": 10, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Linea", "id": 11, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Sub linea", "id": 12, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Fuente", "id": 13, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Último seguimiento", "id": 14, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Situacion actual", "id": 15, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Entendimiento necesidad cliente", "id": 16, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Solucion propuesta", "id": 17, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Estado proceso comercial", "id": 18, "deletable": False, "selectable": False, "hideable": True},
                            {"name": "Razón perdida/cancelada", "id": 19, "deletable": False, "selectable": False, "hideable": True},




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
                            'height': 'auto',
                            'font-family': "Franklin Gothic",
                            'textAlign': 'center',
                        },
                        style_header={
                            'font-family': "Franklin Gothic",
                            'textAlign': 'center',
                            'fontWeight': 'bold'
                        },

                    )
                ),

            ], label="Tablas", label_style={'color': '#082255', 'font-family': "Franklin Gothic"}),

        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div(id='output1', style={'font-family': "Franklin Gothic"})
                        ])
                    ]),
                ])
            ])
        ])
    ]),



])

@app.callback(
    Output(component_id='Agente', component_property='options'),
    Output(component_id='store-data-df_ventas', component_property='data'),
    Output(component_id='Estado', component_property='options'),
    # Output(component_id='store-data-df_oportunidades-tabla', component_property='data'),
    # Output(component_id='store-data-df_ofertas-tabla', component_property='data'),

    Input('my_interval', 'n_intervals'),
)

def dropdown_estado(value_intervals):

    SERVICE_ACCOUNT_FILE = 'keys_tunel_de_ventas.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1ZzhDFL9ELFj3j_Q1F5HWTS-hoPnv_-3tF-ubxldkKhg'

    SAMPLE_RANGE_COMBINADO = "Prueba Nabuco 2017"
    # SAMPLE_RANGE_COMBINADO = "2017"

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_COMBINADO = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                          range=SAMPLE_RANGE_COMBINADO).execute()

    dfCOMBINADO = result_COMBINADO.get('values', [])

    del dfCOMBINADO[0]

    names = ['Asunto', 'Numero OP', 'Estado oportunidad', 'Estado avance', 'Porcentaje avance', 'Visión vendedor', '% visión vendedor', 'Cuenta', 'Punto entrega', 'Contacto', 'Asignada a', 'Equipo', 'Recurso preventa', 'Complejidad', 'Último seguimiento', 'Fecha apertura', 'Trimestre apertura', 'Tipo oportunidad', 'Clase oportunidad', 'Categoría oportunidad', 'Sede', 'Descripción', 'Unidad de negocio', 'Linea', 'Sublinea', 'Fuente', 'Proveedor', 'Contacto proveedor', 'Codigo oportunidad proveedor', 'Vigencia proveedor', 'Oportunidad padre', 'Acuerdo comercial', 'Lista de precios', 'Tasa lista precio (multiplicar por)', 'Tasa lista precio (dividir por)', 'Valor venta estimado', 'Valor venta ponderado', 'Moneda', '% Margen esperado', 'Costo estimado', 'Utilidad estimada', 'Periodo de venta', 'Fecha estimada cierre', 'Trimestre estimado cierre', 'Fecha estimada facturacion', 'Trimestre estimado facturacion', 'Situacion actual', 'Entendimiento necesidad cliente', 'Solucion propuesta', 'Competidores', 'No. solicitud proceso comercial', 'Estado proceso comercial', 'Dias abierta', 'Campaña', 'Cerrada en', 'Razón perdida/cancelada', 'Codigo cotizacion externa', 'Horas esfuerzo estimado', 'Horas esfuerzo real', '% desviación esfuerzo', 'Costo esfuerzo real', '', '', '', 'Número oferta', 'Estado oferta', 'Fecha oferta', 'Asunto', 'Tipo oferta', 'Cuenta', 'Contacto', 'Representante comercial', 'Subtotal', 'Impuesto', 'Total', 'Moneda', 'Sede', 'Unidad de negocio', 'Linea', 'Sub linea', 'Fuente', 'Maquila', 'Costo total', '% otros gastos', 'Vlr. otros gastos', 'Vlr.utilidad', '% Margen', 'Último seguimiento', 'Acuerdo comercial', 'Lista de precios', 'Tasa lista precio (multiplicar por)', 'Tasa lista precio (dividir por)', 'Validez oferta', 'Termino pago', 'Observaciones moneda', 'Forma de envio', 'Condiciones flete', 'Incoterms', 'Garantia', 'Entregar en', 'Punto de entrega', 'Direccion entrega', 'País entrega', 'Departamento/Estado', 'Ciudad/Municipio', 'Otra ciudad', 'Nombre contacto entrega', 'Teléfono fijo contacto', 'Teléfono móvil contacto', 'Correo contacto', 'Tiempo de entrega', 'Fecha maxima entrega', 'Notas de recomendación al cliente', 'Mensaje interno', 'Situacion actual', 'Entendimiento necesidad cliente', 'Solucion propuesta', 'Oferta incluye', 'Oferta no incluye', 'Competidores', 'Recurso elabora', 'No. solicitud proceso comercial', 'Estado proceso comercial', 'Razón perdida/cancelada', 'Observaciones', 'Numero oportunidad']

    dfCOMBINADO = pd.DataFrame(dfCOMBINADO, columns=names)
    dfCOMBINADO.drop([0], inplace=True)
    dfCOMBINADO = dfCOMBINADO.rename(index=lambda x: x - 1)

    # Obtiene el dataframe de oportunidad con las columnas más relevantes
    df_oportunidad = dfCOMBINADO.iloc[:, 0:61]
    df_oportunidad_tabla = df_oportunidad[["Asunto", "Numero OP", "Estado oportunidad", "Estado avance", "Porcentaje avance", "Visión vendedor", "% visión vendedor", "Cuenta", "Asignada a", "Tipo oportunidad", "Categoría oportunidad", "Unidad de negocio", "Linea", "Sublinea", "Fuente", "Valor venta estimado", "Periodo de venta", "Fecha estimada cierre", "Trimestre estimado cierre", "Situacion actual", "Entendimiento necesidad cliente", "Solucion propuesta", "Estado proceso comercial", "Razón perdida/cancelada"]]
    df_oportunidad = df_oportunidad[["Estado oportunidad", "Asignada a", "Último seguimiento", "Fecha apertura", "Clase oportunidad", "Categoría oportunidad", "Fuente", "Valor venta estimado"]]
    df_oportunidad = df_oportunidad.replace(to_replace='', value=np.nan).dropna(axis=0, how="all")

    print(df_oportunidad)

    # Obtiene el dataframe de ofertas con las columnas más relevantes
    df_oferta = dfCOMBINADO.iloc[:, 64:126]
    df_oferta_tabla = df_oferta[["Número oferta", "Estado oferta", "Fecha oferta", "Asunto", "Tipo oferta", "Cuenta", "Contacto", "Representante comercial", "Total", "Unidad de negocio", "Linea", "Sub linea", "Fuente", "Último seguimiento", "Situacion actual", "Entendimiento necesidad cliente", "Solucion propuesta", "Estado proceso comercial", "Razón perdida/cancelada"]]
    df_oferta = df_oferta[["Estado oferta", "Fecha oferta", "Tipo oferta", "Representante comercial", "Total", "Moneda", "Linea", "Sub linea", "Último seguimiento", "Fuente"]]
    print(df_oferta)
    print(df_oportunidad_tabla)
    print(df_oferta_tabla)


    # Genera dataframe con columnas en común de dfs oportunidades y ofertas
    df_ventas = pd.DataFrame()
    df_ventas["Representante Comercial"] = pd.concat([df_oportunidad["Asignada a"], df_oferta["Representante comercial"]], axis=0)
    df_ventas["Último Seguimiento"] = pd.concat([df_oportunidad["Último seguimiento"], df_oferta["Último seguimiento"]], axis=0)
    df_ventas["Fecha Apertura"] = pd.concat([df_oportunidad["Fecha apertura"], df_oferta["Fecha oferta"]], axis=0)
    df_ventas["Valor Venta Estimado"] = pd.concat([df_oportunidad["Valor venta estimado"], df_oferta["Total"]], axis=0)
    df_ventas["Clase"] = pd.concat([df_oportunidad["Clase oportunidad"], df_oferta["Estado oferta"]], axis=0)
    df_ventas["Fuente"] = pd.concat([df_oportunidad["Fuente"], df_oferta["Fuente"]], axis=0)
    df_ventas["Categoría oportunidad"] = pd.concat([df_oportunidad["Categoría oportunidad"], df_oferta["Moneda"]], axis=0)


    # print(df_ventas)
    df_ventas["Clase"] = df_ventas["Clase"].apply(lambda x: 'Propuesta' if x == 'Emitida' else x)
    # df_ventas["Clase"] = list(map(lambda x: if(x = "Emitida"), df_ventas["Clase"]))
    #print(df_ventas)


    # df = dfCOMBINADO

    # estadosDD = list(dict.fromkeys(df['Estado']))
    agenteDD = list(dict.fromkeys(df_ventas["Representante Comercial"]))
    clase = list(dict.fromkeys(df_ventas["Clase"]))

    return agenteDD, df_ventas.to_dict('records'), clase

@app.callback(
    Output(component_id='output1', component_property='children'),
    Output('embudo', component_property='figure'),

    Output('fig-pie-potencial', component_property='figure'),
    Output('fig-pie-cantidad', component_property='figure'),
    Output('fig-potencial', component_property='figure'),
    Output('fig-potencial-cantidad', component_property='figure'),
    Output('fig-potencial2', component_property='figure'),
    Output('fig-potencial-cantidad2', component_property='figure'),


    Input('my_interval', 'n_intervals'),

    Input(component_id='Agente', component_property='value'),
    Input(component_id='store-data-df_ventas', component_property='data'),
    Input(component_id='Estado', component_property='value'),
)

def tunel_de_ventas(value_interval, value_representante, df, value_estado):
    df = pd.DataFrame(df)
    #print(df)
    # print(value_estado)
    print(value_representante)


    # Asignar tipos a cada variable
    df['Valor Venta Estimado'] = list(map(lambda x: x.replace(".", ""), df['Valor Venta Estimado']))
    #df['Valor Venta Estimado'] = list(map(lambda x: x[:-2], df['Valor Venta Estimado']))
    df['Valor Venta Estimado'] = df['Valor Venta Estimado'].apply(lambda x: x[:-2] if len(x)>1 else x)
    df['Valor Venta Estimado'] = list(map(lambda x: float(x), df['Valor Venta Estimado']))
    #df = df.astype({"Valor Venta Estimado": float, "Clase": str})
    df["Fecha Apertura"] = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), df["Fecha Apertura"]))
    df["Último Seguimiento"] = df["Último Seguimiento"].apply(lambda x: 'No existe' if (x == '' or x == None) else x)
    #df["Último Seguimiento"] = df["Último Seguimiento"].apply(lambda x: 'No existe' if x == None else x)
    df["Fuente"] = df["Fuente"].apply(lambda x: 'No reportada' if x == '' else x)
    df["Fuente"] = df["Fuente"].apply(lambda x: 'No reportada' if x == None else x)
    df["Categoría oportunidad"] = df["Categoría oportunidad"].apply(lambda x: None if x == 'COP' else x)
    df["Categoría oportunidad"] = df["Categoría oportunidad"].apply(lambda x: None if x == 'USD' else x)

    a = df["Categoría oportunidad"]
    print("a")
    print(a)

    print(df["Fecha Apertura"])
    print(df["Último Seguimiento"])

    a = df["Último Seguimiento"]
    b = df["Fecha Apertura"]
    for i in range(0, len(b)):
        if a[i] == 'No existe':
            a[i] = b[i]

    print(df.dtypes)
    retorno = ''

    # Filtra el dataframe por el representante comercial seleccionado
    df = df[df['Representante Comercial'] == value_representante]
    #print(df)

    # Número de clientes y venta potencial TOTALES
    clientesTotal = len(df['Valor Venta Estimado'])
    ventaProsTotal = np.array(df['Valor Venta Estimado'])
    ventaProsTotal = sum(ventaProsTotal)

    #print(clientesTotal)
    #print(ventaProsTotal)

    # Número de clientes y venta potencial de POTENCIAL
    dfPotencial = df[df['Clase'] == 'Potenciales']
    clientesPotenciales = len(dfPotencial['Clase'])
    ventaProsPot = np.array(dfPotencial['Valor Venta Estimado'])
    ventaProsPot = sum(ventaProsPot)

    #print(clientesPotenciales)
    #print(ventaProsPot)

    # Número de clientes y venta potencial de LEADS
    dfLeads = df[df['Clase'] == 'Leads']
    clientesLeads = len(dfLeads['Clase'])
    ventaProsLead = np.array(dfLeads['Valor Venta Estimado'])
    ventaProsLead = sum(ventaProsLead)

    #print(clientesLeads)
    #print(ventaProsLead)

    # Número de clientes y venta potencial de DESARROLLO
    dfDesarrollo = df[df['Clase'] == 'Desarrollo']
    clientesDesa = len(dfDesarrollo['Clase'])
    ventaProsDesa = np.array(dfDesarrollo['Valor Venta Estimado'])
    ventaProsDesa = sum(ventaProsDesa)

    #print(clientesDesa)
    #print(ventaProsDesa)

    # Número de clientes y venta potencial EN PROPUESTA
    dfPropuesta = df[df['Clase'] == 'Propuesta']
    clientesProp = len(dfPropuesta['Clase'])
    ventaProsProp = np.array(dfPropuesta['Valor Venta Estimado'])
    ventaProsProp = sum(ventaProsProp)

    #print(clientesProp)
    #print(ventaProsProp)

    # Número de clientes y venta potencial GANADA
    dfGanada = df[df['Clase'] == 'Ganada']
    clientesGanada = len(dfGanada['Clase'])
    ventaProsGanada = np.array(dfGanada['Valor Venta Estimado'])
    ventaProsGanada = sum(ventaProsGanada)

    #print(clientesGanada)
    #print(ventaProsGanada)

    # Número de clientes y venta potencial PERDIDA
    dfPerdida = df[df['Clase'] == 'Perdida']
    clientesPerdida = len(dfPerdida['Clase'])
    ventaProsPerdida = np.array(dfPerdida['Valor Venta Estimado'])
    ventaProsPerdida = sum(ventaProsPerdida)

    #print(clientesPerdida)
    #print(ventaProsPerdida)



    ############################ Crea Figura de pie chart ############################
    estados = df['Clase']
    estados = list(dict.fromkeys(estados))
    dfEstadoSumCant = pd.DataFrame(index=estados, columns=['Suma Prospecto', 'Cantidad', 'Estado'])


    for i in estados:
        dfestado = df[df["Clase"] == i]
        estadoProspSuma = dfestado['Valor Venta Estimado'].values.sum()
        estadoProspCant = len(dfestado['Valor Venta Estimado'])
        dfEstadoSumCant['Suma Prospecto'][i] = estadoProspSuma
        dfEstadoSumCant['Cantidad'][i] = estadoProspCant
        dfEstadoSumCant['Estado'][i] = i

    print(dfEstadoSumCant)

    pie_chart_prospeccto = px.pie(
        data_frame=dfEstadoSumCant,
        values='Suma Prospecto',
        names='Estado',
        color='Estado',  # differentiate markers (discrete) by color
        #color_discrete_sequence=["green", "Black", "blue", "yellow", "red", "purple"],  # set marker colors
        color_discrete_map={"Potencial":"light green", "Leads":"blue", "Desarrollo":"red", "En Propuesta":"green",
                            "Ganada": "yellow", "Perdida":"black"},
        #hover_name='negative',  # values appear in bold in the hover tooltip
        # hover_data=['positive'],            #values appear as extra data in the hover tooltip
        # custom_data=['total'],              #values are extra data to be used in Dash callbacks
        #labels={"state": "the State"},  # map the labels
        title='Sumatoria de Ventas Prospecto',  # figure title
        #template='presentation',  # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        # 'plotly_white', 'plotly_dark', 'presentation',
        # 'xgridoff', 'ygridoff', 'gridon', 'none'
        #width=800,  # figure width in pixels
        #height=600,  # figure height in pixels
        hole=0.5,  # represents the hole in middle of pie
    )

    pie_chart_prospeccto.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )

    pie_chart_cantidad = px.pie(
        data_frame=dfEstadoSumCant,
        values='Cantidad',
        names='Estado',
        color='Estado',  # differentiate markers (discrete) by color
        #color_discrete_sequence=["green", "Black", "blue", "yellow", "red", "purple"],  # set marker colors
        color_discrete_map={"Potencial":"light green", "Leads":"blue", "Desarrollo":"red", "En Propuesta":"green",
                            "Ganada": "yellow", "Perdida":"black"},
        #hover_name='negative',  # values appear in bold in the hover tooltip
        # hover_data=['positive'],            #values appear as extra data in the hover tooltip
        # custom_data=['total'],              #values are extra data to be used in Dash callbacks
        #labels={"state": "the State"},  # map the labels
        title='Cantidad de Ventas Prospecto',  # figure title
        #template='presentation',  # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        # 'plotly_white', 'plotly_dark', 'presentation',
        # 'xgridoff', 'ygridoff', 'gridon', 'none'
        #width=800,  # figure width in pixels
        #height=600,  # figure height in pixels
        hole=0.5,  # represents the hole in middle of pie
    )

    pie_chart_cantidad.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )


    ############################ Cajas del túnel de ventas ###################################

    # Create figure
    fig = go.Figure()

    # Constants
    img_width = 1600
    img_height = 900
    scale_factor = 0.5

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0
        )
    )

    # Configure axes
    fig.update_xaxes(
        visible=False,
        range=[0, img_width * scale_factor]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="stretch",
            source="/assets/Embudo_de_Ventas.png")
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    ### Potenciales
    fig.add_annotation(
        x=105,
        y=365,
        text='Potenciales',
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=397,
        y=365,
        text=clientesPotenciales,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    ventaProsPot = round(ventaProsPot / 1000000, 2)
    ventaProsPot = str(ventaProsPot) + ' MM'
    fig.add_annotation(
        x=690,
        y=365,
        text=ventaProsPot,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=150,
        y=278,
        text='Leads',
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=397,
        y=278,
        text=clientesLeads,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    ventaProsLead = round(ventaProsLead / 1000000, 2)
    ventaProsLead = str(ventaProsLead) + ' MM'
    fig.add_annotation(
        x=653,
        y=278,
        text=ventaProsLead,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=189,
        y=191,
        text='Desarrollo',
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=397,
        y=191,
        text=clientesDesa,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    ventaProsDesa = round(ventaProsDesa / 1000000, 2)
    ventaProsDesa = str(ventaProsDesa) + ' MM'
    fig.add_annotation(
        x=620,
        y=191,
        text=ventaProsDesa,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=226,
        y=106,
        text='Propuesta',
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=397,
        y=106,
        text=clientesProp,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    ventaProsProp = round(ventaProsProp / 1000000, 2)
    ventaProsProp = str(ventaProsProp) + ' MM'
    fig.add_annotation(
        x=573,
        y=106,
        text=ventaProsProp,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=260,
        y=30,
        text='Ganadas',
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=397,
        y=30,
        text=clientesGanada,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    ventaProsGanada = round(ventaProsGanada / 1000000, 2)
    ventaProsGanada = str(ventaProsGanada) + ' MM'
    fig.add_annotation(
        x=540,
        y=30,
        text=ventaProsGanada,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=753,
        y=191,
        text='Perdidas',
        yanchor='bottom',
        showarrow=False,
        font=dict(size=24, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    fig.add_annotation(
        x=753,
        y=106,
        text=clientesPerdida,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    ventaProsPerdida = round(ventaProsPerdida / 1000000, 2)
    ventaProsPerdida = str(ventaProsPerdida) + ' MM'
    fig.add_annotation(
        x=730,
        y=30,
        text=ventaProsPerdida,
        yanchor='bottom',
        showarrow=False,
        font=dict(size=30, color="black", family="Franklin Gothic"),
        align="left",
        bordercolor='black',
        borderwidth=2,
        bgcolor="#CFECEC",
        opacity=0.8,
                        )

    # Crea figuras de ventas potenciales y cantidad de potenciales por categoría por mes

    dfEstado = df[df['Clase'] == str(value_estado)] # Clase
    tipoDePotencial = list(dict.fromkeys(dfEstado['Fuente'])) # Fuente
    dfEstado["Último Seguimiento"] = pd.to_datetime(dfEstado["Último Seguimiento"]) # Último Seguimiento

    figTipodePotencialPotencial = go.Figure()
    figTipodePotencialCantidad = go.Figure()

    for i in tipoDePotencial:
        tipoDePotenciali = dfEstado[dfEstado["Fuente"] == i] # Fuente
        tipoDePotencialiMES = tipoDePotenciali.groupby(tipoDePotenciali['Último Seguimiento'].dt.to_period('M')).sum()
        tipoDePotencialiMESfrec = tipoDePotenciali.groupby(tipoDePotenciali['Último Seguimiento'].dt.to_period('M')).count()
        tipoDePotencialiMESfrec = tipoDePotencialiMESfrec['Valor Venta Estimado'] # Valor Venta Estimado
        xgraph = tipoDePotencialiMES.index.to_timestamp()
        ygraph = tipoDePotencialiMES['Valor Venta Estimado'].values.tolist() # Valor Venta Estimado
        figTipodePotencialPotencial.add_trace(go.Bar(x=xgraph,
                                                         y=ygraph,
                                                         name=i, ))
        ygraph = tipoDePotencialiMESfrec.values.tolist()
        figTipodePotencialCantidad.add_trace(go.Bar(x=xgraph, y=ygraph, name=i, ))

    figTipodePotencialPotencial.update_xaxes(tickformat="%b %Y")
    figTipodePotencialPotencial.update_layout(title="Ventas Potenciales Por Valor", xaxis_title="Fecha", yaxis_title="Valor [COP]")
    figTipodePotencialPotencial.update_layout(legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=-0.5,
                                         xanchor="center",
                                         x=0.5
                                         ))

    figTipodePotencialPotencial.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figTipodePotencialPotencial.update_xaxes(title_font_family="Franklin Gothic")

    figTipodePotencialCantidad.update_xaxes(tickformat="%b %Y")
    figTipodePotencialCantidad.update_layout(title="Ventas Potenciales Por Cantidad", xaxis_title="Fecha", yaxis_title="Cantidad")
    figTipodePotencialCantidad.update_layout(legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=-0.5,
                                         xanchor="center",
                                         x=0.5
                                         ))

    figTipodePotencialCantidad.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figTipodePotencialCantidad.update_xaxes(title_font_family="Franklin Gothic")


    # Crea figuras de ventas potenciales y cantidad de potenciales por categoría por mes DE LAS POTENCIALES

    dfEstado2 = df[df['Clase'] == 'Potenciales'] # Clase
    print(dfEstado2)
    tipoDePotencial2 = list(dict.fromkeys(dfEstado2['Categoría oportunidad'])) # Fuente
    print(tipoDePotencial2)
    dfEstado2["Último Seguimiento"] = pd.to_datetime(dfEstado2["Último Seguimiento"]) # Último Seguimiento

    figTipodePotencialPotencial2 = go.Figure()
    figTipodePotencialCantidad2 = go.Figure()

    for i in tipoDePotencial2:
        tipoDePotenciali2 = dfEstado2[dfEstado2["Categoría oportunidad"] == i] # Fuente
        tipoDePotencialiMES2 = tipoDePotenciali2.groupby(tipoDePotenciali2['Último Seguimiento'].dt.to_period('M')).sum()
        tipoDePotencialiMESfrec2 = tipoDePotenciali2.groupby(tipoDePotenciali2['Último Seguimiento'].dt.to_period('M')).count()
        tipoDePotencialiMESfrec2 = tipoDePotencialiMESfrec2['Valor Venta Estimado'] # Valor Venta Estimado
        xgraph2 = tipoDePotencialiMES2.index.to_timestamp()
        ygraph2 = tipoDePotencialiMES2['Valor Venta Estimado'].values.tolist() # Valor Venta Estimado
        figTipodePotencialPotencial2.add_trace(go.Bar(x=xgraph2,
                                                         y=ygraph2,
                                                         name=i, ))
        ygraph2 = tipoDePotencialiMESfrec2.values.tolist()
        figTipodePotencialCantidad2.add_trace(go.Bar(x=xgraph2, y=ygraph2, name=i, ))

    figTipodePotencialPotencial2.update_xaxes(tickformat="%b %Y")
    figTipodePotencialPotencial2.update_layout(title="Ventas Potenciales Por Valor", xaxis_title="Fecha", yaxis_title="Valor [COP]")
    figTipodePotencialPotencial2.update_layout(legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=-0.5,
                                         xanchor="center",
                                         x=0.5
                                         ))

    figTipodePotencialPotencial2.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figTipodePotencialPotencial2.update_xaxes(title_font_family="Franklin Gothic")

    figTipodePotencialCantidad2.update_xaxes(tickformat="%b %Y")
    figTipodePotencialCantidad2.update_layout(title="Ventas Potenciales Por Cantidad", xaxis_title="Fecha", yaxis_title="Cantidad")
    figTipodePotencialCantidad2.update_layout(legend=dict(orientation="h",
                                         yanchor="bottom",
                                         y=-0.5,
                                         xanchor="center",
                                         x=0.5
                                         ))

    figTipodePotencialCantidad2.update_layout(
        font_family="Franklin Gothic",
        title_font_family="Franklin Gothic",
    )
    figTipodePotencialCantidad2.update_xaxes(title_font_family="Franklin Gothic")



    return retorno, fig, pie_chart_prospeccto, pie_chart_cantidad, figTipodePotencialPotencial, \
           figTipodePotencialCantidad, figTipodePotencialPotencial2, figTipodePotencialCantidad2


if __name__ == '__main__':
    app.run_server()
    #app.run_server(debug=False, port=8077, threaded=True)

