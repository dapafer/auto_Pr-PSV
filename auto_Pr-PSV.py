import pymysql
from datetime import datetime, date
import streamlit as st
import pandas as pd

# Configurar el título principal
st.sidebar.markdown("# **auto_Pr-PSV**")

# Establecer conexión con la base de datos MySQL
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="password",
    database="supermercado"
)

# Función para ejecutar consultas SQL
def ejecutar_consulta(consulta, parametros=None):
    with connection.cursor() as cursor:
        cursor.execute(consulta, parametros)
        resultados = cursor.fetchall()
    return resultados

# Obtener categorías de la tabla categorias
consulta_categorias = "SELECT DISTINCT categoria FROM categorias"
categorias = [row[0] for row in ejecutar_consulta(consulta_categorias)]

# Mostrar selector de página en el menú lateral
pagina_seleccionada = st.sidebar.selectbox("Selecciona una página", ["", "Previsión", "Pedido", "Vendido"])


# Mostrar mensaje de bienvenida en la página principal
st.title("Bienvenida/o a Pr-PSV+")
st.subheader("Seleccione una opción en la barra lateral")

# Mostrar enlace debajo de la imagen
url = "https://facebook.github.io/prophet/"  # Reemplaza con el enlace deseado
st.markdown(f"Con tecnología de [Prophet]({url})")

# Mostrar imagen "Con tecnología de"
image = "images/PROPHET_logo_1.png"  # Reemplaza con la ruta correcta de la imagen
st.image(image, use_column_width=True)




if pagina_seleccionada == "Previsión":
    # Mostrar título "Previsión" en el menú lateral
    st.sidebar.markdown("## **Previsión**")

    # Selector de categoría en el menú lateral
    categoria_seleccionada = st.sidebar.selectbox("Selecciona una categoría", [""] + categorias, key="prevision_categoria")

    if categoria_seleccionada:
        # Mostrar título "Previsión" en la página principal
        st.title("Previsión")
        # Obtener el id de la categoría seleccionada
        consulta_id_categoria = "SELECT categoria_id FROM categorias WHERE categoria = %s"
        id_categoria = ejecutar_consulta(consulta_id_categoria, categoria_seleccionada)[0][0]

        # Selector de rango de fechas en el menú lateral
        fecha_actual = date.today()  # Fecha actual

        fecha_inicio = st.sidebar.date_input("Selecciona la fecha de inicio", min_value=fecha_actual, max_value=None, value=None, key="prevision_fecha_inicio")
        fecha_fin = st.sidebar.date_input("Selecciona la fecha de fin", min_value=fecha_actual, max_value=None, value=None, key="prevision_fecha_fin")

        if fecha_inicio and fecha_fin:
            # Convertir fechas seleccionadas a formato de base de datos
            fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

            # Consulta SQL para obtener los datos de previsiones para la categoría y rango de fechas seleccionado
            consulta_previsiones = """
            SELECT p.producto, p.formato, v.fecha, vp.prevision
            FROM productos p
            JOIN ventas_productos vp ON p.producto_id = vp.producto_id
            JOIN ventas v ON vp.venta_id = v.venta_id
            WHERE p.categoria_id = %s
            AND v.fecha BETWEEN %s AND %s
            ORDER BY p.producto_id ASC, v.fecha ASC  # Ordenar por el id de producto y fecha de forma ascendente
            """
            previsiones = ejecutar_consulta(consulta_previsiones, (id_categoria, fecha_inicio_str, fecha_fin_str))

            # Crear un DataFrame con los resultados
            df_previsiones = pd.DataFrame(previsiones, columns=['producto', 'formato', 'fecha', 'prevision'])

            # Transformar el DataFrame para tener una columna por cada fecha de previsión
            df_previsiones = df_previsiones.pivot(index=['producto', 'formato'], columns='fecha', values='prevision')

            # Ordenar las columnas del DataFrame por la fecha
            df_previsiones = df_previsiones.reindex(sorted(df_previsiones.columns), axis=1)

            # Mostrar la tabla de previsiones
            st.write(df_previsiones)

            # Calcular la suma de las previsiones por fecha
            suma_previsiones = df_previsiones.sum()

            # Mostrar el resultado de la suma de previsiones por fecha
            st.write("### **Suma de previsiones por fecha:**")
            st.write(suma_previsiones)

            st.markdown("---")

            # Crear gráfico de barras para la suma de previsiones por fecha
            st.bar_chart(suma_previsiones, use_container_width=True)





# Mostrar página seleccionada
elif pagina_seleccionada == "Pedido":
    # Mostrar título "Pedido" en el menú lateral
    st.sidebar.markdown("## **Pedido**")

    # Selector de categoría en el menú lateral
    categoria_seleccionada = st.sidebar.selectbox("Selecciona una categoría", [""] + categorias, key="categoria")

    if categoria_seleccionada:
        # Mostrar título "Pedido" en la página principal
        st.title("Pedido")
        # Obtener el id de la categoría seleccionada
        consulta_id_categoria = "SELECT categoria_id FROM categorias WHERE categoria = %s"
        id_categoria = ejecutar_consulta(consulta_id_categoria, categoria_seleccionada)[0][0]

        # Consulta SQL para obtener los productos de la categoría seleccionada
        consulta_productos = """
        SELECT producto, formato, precio
        FROM productos
        WHERE categoria_id = %s
        """
        productos = ejecutar_consulta(consulta_productos, id_categoria)

        # Selector de fecha en el menú lateral
        fecha_actual = datetime.now().date()  # Fecha actual
        fecha_seleccionada = st.sidebar.date_input("Selecciona una fecha", min_value=fecha_actual, max_value=None, value=None, key="fecha")

        if fecha_seleccionada:
            # Convertir fecha seleccionada a formato de base de datos
            fecha_seleccionada_str = fecha_seleccionada.strftime('%Y-%m-%d')

            # Consulta SQL para obtener los datos de ventas para la categoría y fecha seleccionadas
            consulta_ventas = """
            SELECT p.producto, p.formato, p.precio, vp.prevision
            FROM productos p
            JOIN ventas_productos vp ON p.producto_id = vp.producto_id
            JOIN ventas v ON vp.venta_id = v.venta_id
            WHERE p.categoria_id = %s
            AND v.fecha = %s
            """
            ventas = ejecutar_consulta(consulta_ventas, (id_categoria, fecha_seleccionada_str))

            # Crear un DataFrame con los resultados
            df_ventas = pd.DataFrame(ventas, columns=['producto', 'formato', 'precio', 'prevision'])

            # Mostrar los resultados en Streamlit
            pedido_total = 0
            pr_total = 0

            for index, row in df_ventas.iterrows():
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])  # Ancho relativo de las columnas

                with col1:
                    st.write("##### **Producto**")
                    st.write(row['producto'])

                with col2:
                    st.write("##### **Formato**")
                    st.write(row['formato'])

                with col3:
                    st.write("##### **Precio**")
                    st.write(row['precio'])

                with col4:
                    st.write("##### **Cantidad**")
                    prevision = st.number_input("", value=row['prevision'], key=index, format="%d", min_value=0, max_value=999)
                    pedido_total += prevision

                with col5:
                    st.write("## **Pr**")
                    default_value = str(row['prevision'])
                    st.write(default_value)
                    pr_total += int(default_value)

            # Pedido total
            st.markdown("---")
            col4_total, col5_total = st.columns([4, 1])
            with col4_total:
                st.write("## **Pedido TOTAL**")
                st.markdown("<h3>{}</h3>".format(pedido_total), unsafe_allow_html=True)

            # Pr total
            with col5_total:
                st.write("## **Pr TOTAL**")
                st.markdown("<h3>{}</h3>".format(pr_total), unsafe_allow_html=True)
            
            # Botón para guardar el pedido
            if st.button("Guardar Pedido"):
                st.success("Pedido guardado con éxito")
 



elif pagina_seleccionada == "Vendido":
    # Mostrar título "Vendido" en el menú lateral
    st.sidebar.markdown("## **Vendido**")

    # Selector de categoría en el menú lateral
    categoria_seleccionada = st.sidebar.selectbox("Selecciona una categoría", [""] + categorias, key="vendido_categoria")

    if categoria_seleccionada:
        # Mostrar título "Vendido" en la página principal
        st.title("Vendido")
        # Obtener el id de la categoría seleccionada
        consulta_id_categoria = "SELECT categoria_id FROM categorias WHERE categoria = %s"
        id_categoria = ejecutar_consulta(consulta_id_categoria, categoria_seleccionada)[0][0]

        # Selector de fecha en el menú lateral
        fecha_actual = date.today()  # Fecha actual

        fecha_seleccionada = st.sidebar.date_input("Selecciona una fecha", min_value=None, max_value=fecha_actual, value=None, key="vendido_fecha")

        if fecha_seleccionada:
            # Convertir fecha seleccionada a formato de base de datos
            fecha_seleccionada_str = fecha_seleccionada.strftime('%Y-%m-%d')

            # Consulta SQL para obtener los datos de ventas para la categoría y fecha seleccionadas
            consulta_ventas = """
            SELECT p.producto, p.formato, vp.venta, vp.prevision
            FROM productos p
            JOIN ventas_productos vp ON p.producto_id = vp.producto_id
            JOIN ventas v ON vp.venta_id = v.venta_id
            WHERE p.categoria_id = %s
            AND v.fecha = %s
            """
            ventas = ejecutar_consulta(consulta_ventas, (id_categoria, fecha_seleccionada_str))

            # Crear un DataFrame con los resultados
            df_ventas = pd.DataFrame(ventas, columns=['producto', 'formato', 'venta', 'prevision'])

            # Mostrar la tabla de ventas
            st.write(df_ventas)

            # Calcular la suma de las columnas 'venta' y 'prevision'
            suma_venta = df_ventas['venta'].sum()
            suma_prevision = df_ventas['prevision'].sum()
            diferencia = suma_venta - suma_prevision

            # Mostrar el resultado de las sumas
            st.write("### **Venta TOTAL:**", suma_venta)
            st.write("### **Previsión TOTAL:**", suma_prevision)
            st.write("##### **Diferencia:**", diferencia)

            st.markdown("---")

            # Crear gráfico de barras horizontales
            data = {"Venta": suma_venta, "Previsión": suma_prevision}
            st.bar_chart(data, use_container_width=True)
