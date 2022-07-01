@app.callback(
    Output(component_id='datatable-interactivity-purgas', component_property='data'),

    Input('store-data-purgas', 'modified_timestamp'),
    State('store-data-purgas', 'data')


)

def pegar_tabla_purgas(ts, data):
    #if ts is None:
    #    raise PreventUpdate

    return data



    Output(component_id='store-data-purgas', component_property='data'),

    Input('registro-purgas', 'n_clicks'),
    State('fecha-purgas', 'date'),
    State('hora-inicial-purgas', 'value'),
    State('hora-final-purgas', 'value'),
    State('altura-inicial-purgas', 'value'),
    State('altura-final-purgas', 'value'),
    State('fase-purgas', 'value'),
    State('store-data-purgas', component_property="data"),
    #State(component_id='datatable-interactivity-purgas', component_property='data'),
    Input('borrar-purgas', 'n_clicks'),
    Input('guardar-cambios-purgas', 'n_clicks'),
    State(component_id='datatable-interactivity-purgas', component_property='data'),






style_header={
                                'font-family': "Franklin Gothic",
                                'textAlign': 'center',
                                'fontWeight': 'bold'
                            },



style={'font-family': "Franklin Gothic", 'textAlign': 'center',}
date=date.today(),

df['date'] = pd.to_datetime(df['date'])
df1 = df.groupby(df['date'].dt.to_period('M')).sum()
df1 = df1.resample('M').asfreq().fillna(0)

figTipodePotencialPotencial.update_xaxes(
    # dtick="M1",
    tickformat="%b %Y",
    # ticklabelmode="period"
)



@app.callback(Output("loading-output-1", "children"), Input("mi-mes-vol", "value"))
def input_triggers_spinner(value):
    time.sleep(1)
    return value


    names = ["Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]", "Altura Final [m]", "Tiempo [min]",
             "Volumen [m3]",
             "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]",
             "Total Purgas Captadas", "Fase", "", "", "", "Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]",
             "Altura Final [m]", "Tiempo [min]",
             "Volumen [m3]",
             "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]",
             "Total Purgas Bombeadas", "Fase", "", "", "", "Fecha", "Hora Inicio", "Hora Fin", "Lectura Inicial",
             "Lectura Final", "Turbidez [NTU]", "Color [Pt-Co]",
             "pH", "Tiempo [min]", "Volumen [m3]", "Volumen [gal]", "Tiempo Acumulado [min]", "Volumen Acumulado [m3]",
             "Volumen Acumulado [gal]", "Fase", "", "", "", "Fase", "Numero", "Largo", "Ancho", "Fecha", "Hora",
             "Altura Promedio", "Volumen Teórico [m3]", "% Uso", "Peso [Ton]", "Capacidad [m3]", "Referencia"]

    dfPURG50 = dfPURG50.astype({"Altura Inicial [m]": float, "Altura Final [m]": float,
                                "Tiempo [min]": 'int64', "Volumen [m3]": float, "Volumen [gal]": float,
                                "Volumen acumulado [m3]": float, "Volumen acumulado [gal]": float,
                                "Tiempo acumulado [min]": 'int64', "Total Purgas Captadas": 'int64',
                                "Fase": 'int64'
                                })

    ["Fecha", "Hora Inicio", "Hora Fin", "Altura Inicial [m]", "Altura Final [m]", "Tiempo [min]",
     "Volumen [m3]",
     "Volumen [gal]", "Volumen acumulado [m3]", "Volumen acumulado [gal]", "Tiempo acumulado [min]",
     "Total Purgas Captadas", "Fase"])


    dbc.Col([
        html.Div(id='dia-inicial-acum', style={'font-family': "Franklin Gothic"})
    ], xs=3, sm=3, md=3, lg=2, xl=2, align="center"), \
 \
    dbc.Col([
        html.Div(id='dia-final-acum', style={'font-family': "Franklin Gothic"})
    ], xs=2, sm=2, md=2, lg=2, xl=2, style={'textAlign': 'center'}, align='center'),



id='LED-dias-oper-GT'


fechaCLRdd = list(dict.fromkeys(fechaCLR))


dff = list(map(lambda fecha: datetime.strptime(fecha, "%d/%m/%Y"), dff))
dff = list(map(lambda fecha: str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year), dff))


dcc.Store(id='store-data-df_ventas', storage_type='memory'),  # 'local' or 'session'



    # Crea figuras de ventas potenciales y cantidad de potenciales por categoría por mes
    dfEstado = df[df['Estado'] == str(value_estado)]
    tipoDePotencial = list(dict.fromkeys(dfEstado['Tipo de Potencial']))
    #tipoDePotencial['Fecha'] = tipoDePotencial['Fecha contacto']
    dfEstado["Fecha contacto"] = pd.to_datetime(dfEstado["Fecha contacto"])


    figTipodePotencialPotencial = go.Figure()
    figTipodePotencialCantidad = go.Figure()

    for i in tipoDePotencial:
        tipoDePotenciali = dfEstado[dfEstado["Tipo de Potencial"] == i]
        tipoDePotencialiMES = tipoDePotenciali.groupby(tipoDePotenciali['Fecha contacto'].dt.to_period('M')).sum()
        tipoDePotencialiMESfrec = tipoDePotenciali.groupby(tipoDePotenciali['Fecha contacto'].dt.to_period('M')).count()
        tipoDePotencialiMESfrec = tipoDePotencialiMESfrec['Prospecto']
        xgraph = tipoDePotencialiMES.index.to_timestamp()
        ygraph = tipoDePotencialiMES['Prospecto'].values.tolist()
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



df_oferta_tabla = df_oferta[["Número oferta", "Estado oferta", "Fecha oferta", "Asunto", "Tipo oferta", "Cuenta", "Contacto", "Representante comercial", "Total", "Unidad de negocio", "Linea", "Sub linea", "Fuente", "Último seguimiento", "Situacion actual", "Entendimiento necesidad cliente", "Solucion propuesta", "Estado proceso comercial", "Razón perdida/cancelada"]]