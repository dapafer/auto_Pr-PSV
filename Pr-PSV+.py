import streamlit as st
import webbrowser

# Obtén el nombre de la página seleccionada en el menú lateral
pagina_seleccionada = st.sidebar.selectbox("Selecciona una página", ["Nombre Página 1", "Nombre Página 2", ...])

# Mapea los nombres de las páginas con sus URL correspondientes
urls = {
    "Nombre Página 1": "http://localhost:8501/pagina_principal",
    "Nombre Página 2": "http://localhost:8501/page2",
    # Agrega más páginas y sus URL aquí 
}

# Abre la página correspondiente en el navegador
if pagina_seleccionada in urls:
    url = urls[pagina_seleccionada]
    webbrowser.open_new_tab(url)
