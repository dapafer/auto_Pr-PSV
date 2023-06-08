import streamlit as st

import pymysql

import pandas as pd

from datetime import datetime, date, timedelta

import requests as req



# establecer conexión con base de datos MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='supermercado'
)

# función para ejecutar consultas SQL
def ejecutar_consulta(consulta, parametros=None):
    with connection.cursor() as cursor:
        cursor.execute(consulta, parametros)
        resultados = cursor.fetchall()
    return resultados

# obtener categorías de tabla "categorias"
consulta_categorias = 'SELECT DISTINCT categoria FROM categorias'
categorias = [row[0] for row in ejecutar_consulta(consulta_categorias)]

# configurar título principal
st.sidebar.markdown('# **Pr-PSV+**')

# mostrar selector de página en el menú lateral
pagina_seleccionada = st.sidebar.selectbox('Selecciona una opción', ['', 'Previsión', 'Pedido', 'Vendido'])


# mostrar mensaje de bienvenida en página principal
st.title('Bienvenida/o a Pr-PSV+')
st.subheader('Seleccione una opción en el menú lateral')

# mostrar enlace encima de imagen
url = 'https://facebook.github.io/prophet/'
st.markdown(f'Con tecnología de [Prophet]({url})')

# mostrar imagen
image = 'images/prophet_logo_2.png'
st.image(image, use_column_width=True)

st.divider()





# mostrar página "Previsión"
if pagina_seleccionada == 'Previsión':
    # mostrar título "Pr" en menú lateral
    st.sidebar.markdown('## **Pr**')

    # selector de categoría en menú lateral
    categoria_seleccionada = st.sidebar.selectbox('Selecciona una categoría', [''] + categorias, key='prevision_categoria')

    if categoria_seleccionada:
        # mostrar título "Previsión" en la página principal
        st.title('Previsión')
        # obtener id de la categoría seleccionada
        consulta_id_categoria = 'SELECT categoria_id FROM categorias WHERE categoria = %s'
        id_categoria = ejecutar_consulta(consulta_id_categoria, categoria_seleccionada)[0][0]

        # selector de rango de fechas en menú lateral
        fecha_actual = date.today()  # Fecha actual
        fecha_inicio = st.sidebar.date_input('Selecciona la fecha de inicio', min_value=fecha_actual, max_value=None, value=None, key='prevision_fecha_inicio')
        fecha_fin = st.sidebar.date_input('Selecciona la fecha de fin', min_value=fecha_actual, max_value=None, value=None, key='prevision_fecha_fin')

        if fecha_inicio and fecha_fin:
            # convertir fechas seleccionadas a formato de base de datos
            fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

            # consulta SQL para obtener datos de previsiones para la categoría y rango de fechas seleccionado
            consulta_previsiones = '''
            SELECT p.producto, p.formato, v.fecha, vp.prevision
            FROM productos p
            JOIN ventas_productos vp ON p.producto_id = vp.producto_id
            JOIN ventas v ON vp.venta_id = v.venta_id
            WHERE p.categoria_id = %s
            AND v.fecha BETWEEN %s AND %s
            ORDER BY p.producto_id ASC, v.fecha ASC
            '''
            previsiones = ejecutar_consulta(consulta_previsiones, (id_categoria, fecha_inicio_str, fecha_fin_str))

            # crear dataframe con resultados
            df_previsiones = pd.DataFrame(previsiones, columns=['producto', 'formato', 'fecha', 'prevision'])

            # transformar dataframe para tener una columna por cada fecha de previsión
            df_previsiones = df_previsiones.pivot(index=['producto', 'formato'], columns='fecha', values='prevision')

            # ordenar columnas por fecha
            df_previsiones = df_previsiones.reindex(sorted(df_previsiones.columns), axis=1)

            # mostrar tabla previsiones
            st.write(df_previsiones)

            # botón para guardar informe
            if st.button('Guardar informe'):
                # guardar dataframe en archivo CSV
                df_previsiones.to_csv('data/streamlit/informe_previsiones.csv', index=True)
                st.success('Informe guardado con éxito')

            st.divider()

            # convertir previsiones a números enteros
            df_previsiones = df_previsiones.astype(int)

            # calcular suma de previsiones por fecha
            suma_previsiones = df_previsiones.sum()

            # mostrar resultado de suma de previsiones por fecha
            st.write('### **Previsión por fecha**')
            st.write(suma_previsiones)

            st.divider()

            # crear gráfico de barras para suma de previsiones por fecha
            chart = st.bar_chart(suma_previsiones, use_container_width=True)



# mostrar página "Pedido"
elif pagina_seleccionada == 'Pedido':
    # mostrar título "P" en menú lateral
    st.sidebar.markdown('## **P**')

    # selector de categoría en menú lateral
    categoria_seleccionada = st.sidebar.selectbox('Selecciona una categoría', [''] + categorias, key='categoria')

    if categoria_seleccionada:
        # mostrar título "Pedido" en la página principal
        st.title('Pedido')
        # obtener id de categoría seleccionada
        consulta_id_categoria = 'SELECT categoria_id FROM categorias WHERE categoria = %s'
        id_categoria = ejecutar_consulta(consulta_id_categoria, categoria_seleccionada)[0][0]

        # consulta SQL para obtener productos de categoría seleccionada
        consulta_productos = '''
        SELECT producto, formato, precio
        FROM productos
        WHERE categoria_id = %s
        '''
        productos = ejecutar_consulta(consulta_productos, id_categoria)

        # selector de fecha en menú lateral
        fecha_actual = datetime.now().date()
        fecha_seleccionada = st.sidebar.date_input('Selecciona una fecha', min_value=fecha_actual, max_value=None, value=None, key='fecha')

        if fecha_seleccionada:
            # introducir clave API
            querystring = {'api_key': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcGFyaWNpb2Zlcm5hbmRlei5kQGdtYWlsLmNvbSIsImp0aSI6IjEwNDY5YzVkLTMwMDUtNDhhMi1hYTU3LTBiM2M2NjE3MmFiOSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNjgzNTAzNTQ3LCJ1c2VySWQiOiIxMDQ2OWM1ZC0zMDA1LTQ4YTItYWE1Ny0wYjNjNjYxNzJhYjkiLCJyb2xlIjoiIn0._fxyjpdUYGVn4fEMEYg64Mvcc5ODJp2J8jLlbUNDtYw'}

            # introducir código de "provincia"
            provincia = '28'

            # fuente de datos para sacar datos climatológicos diarios de una estación concreta
            url = f'https://opendata.aemet.es/opendata//api/prediccion/provincia/manana/{provincia}'

            headers = {
            'cache-control': "no-cache"
            }

            # consultar API
            res = req.request('GET', url, headers=headers, params=querystring)

            # obtener la URL de descarga de los datos
            data_url = res.json()['datos']

            # descargar los datos
            data_res = req.get(data_url)

            # mostrar los resultados de la consulta climatológica al principio de la página
            st.subheader('Informe Climatológico')
            st.code(data_res.text)

            st.divider()

            # convertir fecha seleccionada a formato de base de datos
            fecha_seleccionada_str = fecha_seleccionada.strftime('%Y-%m-%d')

            # consulta SQL para obtener datos de ventas para categoría y fecha seleccionadas
            consulta_ventas = '''
            SELECT p.producto, p.formato, p.precio, vp.prevision
            FROM productos p
            JOIN ventas_productos vp ON p.producto_id = vp.producto_id
            JOIN ventas v ON vp.venta_id = v.venta_id
            WHERE p.categoria_id = %s
            AND v.fecha = %s
            '''
            ventas = ejecutar_consulta(consulta_ventas, (id_categoria, fecha_seleccionada_str))

            # crear dataframe con resultados
            df_ventas = pd.DataFrame(ventas, columns=['producto', 'formato', 'precio', 'prevision'])

            # mostrar resultados
            pedido_total = 0
            pr_total = 0

            for index, row in df_ventas.iterrows():
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

                with col1:
                    st.write('##### **Producto**')
                    st.write(row['producto'])

                with col2:
                    st.write('##### **Formato**')
                    st.write(row['formato'])

                with col3:
                    st.write('##### **Precio**')
                    st.write(row['precio'])

                with col4:
                    st.write('##### **Cantidad**')
                    prevision = st.number_input("", value=row['prevision'], key=index, format="%d", min_value=0, max_value=999)
                    pedido_total += prevision

                with col5:
                    st.write('## **Pr**')
                    default_value = str(row['prevision'])
                    st.write(default_value)
                    pr_total += int(default_value)


            st.divider()

            # pedido total
            col4_total, col5_total = st.columns([4, 1])
            with col4_total:
                st.write('## **Pedido TOTAL**')
                st.markdown('<h3>{}</h3>'.format(pedido_total), unsafe_allow_html=True)

            # Pr total
            with col5_total:
                st.write('## **Pr TOTAL**')
                st.markdown('<h3>{}</h3>'.format(pr_total), unsafe_allow_html=True)
            
            # botón para guardar pedido
            if st.button('Guardar Pedido'):
                st.success('Pedido guardado correctamente')

 

# mostrar página "Vendido"
elif pagina_seleccionada == 'Vendido':
    # mostrar título "V" en menú lateral
    st.sidebar.markdown('## **V**')

    # selector de categoría en menú lateral
    categoria_seleccionada = st.sidebar.selectbox('Selecciona una categoría', [''] + categorias, key='vendido_categoria')

    if categoria_seleccionada:
        # mostrar título "Vendido" en la página principal
        st.title('Vendido')
        # obtener id de categoría seleccionada
        consulta_id_categoria = 'SELECT categoria_id FROM categorias WHERE categoria = %s'
        id_categoria = ejecutar_consulta(consulta_id_categoria, categoria_seleccionada)[0][0]

        # selector de fecha en menú lateral
        fecha_actual = date.today()
        fecha_seleccionada = st.sidebar.date_input('Selecciona una fecha', min_value=None, max_value=fecha_actual, value=None, key='vendido_fecha')

        if fecha_seleccionada:
            # convertir fecha seleccionada a formato de base de datos
            fecha_seleccionada_str = fecha_seleccionada.strftime('%Y-%m-%d')

            # consulta SQL para obtener datos de ventas para categoría y fecha seleccionadas
            consulta_ventas = '''
            SELECT p.producto, p.formato, vp.venta, vp.prevision, v.lluvia, v.temperatura_minima, v.temperatura_maxima
            FROM productos p
            JOIN ventas_productos vp ON p.producto_id = vp.producto_id
            JOIN ventas v ON vp.venta_id = v.venta_id
            WHERE p.categoria_id = %s
            AND v.fecha = %s
            '''
            ventas = ejecutar_consulta(consulta_ventas, (id_categoria, fecha_seleccionada_str))

            # crear dataframe con resultados
            df_ventas = pd.DataFrame(ventas, columns=['producto', 'formato', 'venta', 'prevision', 'lluvia', 'temperatura_minima', 'temperatura_maxima'])

            # mostrar tabla de ventas
            st.write(df_ventas)

            st.divider()

            # calcular suma de columnas 'venta' y 'prevision'
            suma_venta = df_ventas['venta'].sum()
            suma_prevision = df_ventas['prevision'].sum()
            diferencia = suma_venta - suma_prevision

            col1, col2, col3 = st.columns(3)
            col1.metric(label='##### **Venta TOTAL**', value=suma_venta)
            col2.metric(label='##### **Previsión TOTAL**', value=suma_prevision)
            col3.metric(label='##### **Diferencia**', value=diferencia)

            # botón para guardar informe
            if st.button('Guardar informe'):
                # guardar dataframe en archivo CSV
                df_ventas.to_csv('data/streamlit/informe_ventas.csv', index=False)
                st.success('Informe guardado con éxito')

            st.divider()

            # crear gráfico de barras horizontales
            data = {'Venta': suma_venta, 'Previsión': suma_prevision}
            st.bar_chart(data, use_container_width=True)