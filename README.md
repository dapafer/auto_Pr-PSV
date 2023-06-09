# **Pr-PSV+**

![portada](https://github.com/dapafer/auto_Pr-PSV/blob/main/images/sales_preds.png)

---

Pr-PSV+ es la mejora de la herramienta de gestión y control de pedidos de un supermercado, para las categorías de productos frescos, concretamente Fruta y verdura, Carne y Pescado. La mejora de la herramienta consiste en generar previsiones de venta futura en base a un modelo de predicción de series temporales, concretamente [Prophet](https://facebook.github.io/prophet/).

---
## 📌 **Índice.**

- [Contenido.](#contenido)
- [Problemas.](#problemas)
- [Soluciones.](#soluciones)
- [Desarrollo.](#desarrollo)
- [Demo.](#demo)
- [Próximos objetivos.](#proximos_objetivos)

---
<a name='contenido'/>

### 📂 **Contenido**

El proyecto cuenta con la siguiente estructura principal:

- [`data`](https://github.com/dapafer/auto_Pr-PSV/tree/main/data): carpeta que contiene todos los archivos generados durante el desarrollo del proyecto, subdividida por cada proceso.
- [`demo`](https://github.com/dapafer/auto_Pr-PSV/tree/main/demo): carpeta principal con demostraciones de funcionamiento de la webapp, y archivos para replicarla.
- [`src`](https://github.com/dapafer/auto_Pr-PSV/tree/main/src): carpeta principal con notebooks del proceso y scripts de pruebas de `SQL`, subdividida por cada proceso.
- [`Pr-PSV+.py`](https://github.com/dapafer/auto_Pr-PSV/blob/main/Pr-PSV%2B.py): script de ejecución de la webapp, que simula la herramienta de gestión y control de pedidos.

---
<a name='problemas'/>

### ❗️ **Problemas**

El planteamiento de partida es analizar los problemas que tiene actualmente la herramienta. Principalmente son:

- Para realizar un pedido, las previsiones de una categoría se realizan basándose en un "ancla" (histórico de ventas de una fecha similar) de manera manual.
- Los pedidos se realizan y modifican en base a la "experiencia" que tiene la persona que lo realiza, la cual si no posee esa experiencia, el proceso de generar previsiones acordes es complicado.
- Solo se pueden realizar pedidos para el día siguiente al que se realizan, por tanto no es escalable a más fechas futuras.

---
<a name='soluciones'/>

### 💡 **Soluciones**

Por ello, se ha aplicado un modelo de generación de predicciones, que ha podido generar soluciones para mejorar la herramienta, las cuales son:

- Las previsiones se generan de manera automática en base a un histórico de ventas.
- No hace falta tener experiencia en la categoría para la cual se realiza el pedido, debido a esa generación automática de previsiones basadas en el modelo de aprendizaje automático.
- La herramienta puede generar pedidos para más fechas, debido a que genera predicciones para un número específico dado de fechas, no solo para el día siguiente al cual se realiza el pedido.

---
<a name='desarrollo'/>

### 📝 **Desarrollo**

El desarrollo del proyecto ha tenido las siguientes etapas principales:

- [**Web scraping & API**](https://github.com/dapafer/auto_Pr-PSV/tree/main/src/scraping): el primer objetivo fue generar y obtener datos de la categoría de Fruta y Verdura de un supermercado, en este caso Mercadona. Se han extraído datos a través de `Selenium`. También se han extraído datos de climatología de las fechas en las que se tienen datos de venta, lo cual se ha realizado a través de la `API` de AEMET (Agencia Estatal de Metereología). Por supuesto, se ha realizado una limpieza y transfrmación de los datos obtenidos.
- [**Generación de predicciones de venta**](https://github.com/dapafer/auto_Pr-PSV/tree/main/src/preds): En base a los [datos generados de venta](https://github.com/dapafer/auto_Pr-PSV/blob/main/src/database/random_data_values_fyv.ipynb), se ha procedido a utilizar un modelo generación de predicciones, específico para series temporales, llamado [Prophet](https://github.com/dapafer/auto_Pr-PSV/blob/main/src/preds/preds_fyv_prevision.ipynb).
- [**Transformación y carga a base de datos**](https://github.com/dapafer/auto_Pr-PSV/tree/main/src/database): teniendo toda la estructura creada y transformada de tablas y datos, hemos realizado la [exportación y carga](https://github.com/dapafer/auto_Pr-PSV/blob/main/src/database/supermercado_database_to_mysql.ipynb) a una base de datos en `MySQL`. Posteriormente, hemos realizado unas [consultas](https://github.com/dapafer/auto_Pr-PSV/blob/main/data/sql/filters.sql), para comprobar que la estructura y los datos estuvieran correctamente estructurados, así como para generar datos para la realización de predicciones.

<a name='demo'/>

### ▶️ **Demo**

La carpeta [demo](https://github.com/dapafer/auto_Pr-PSV/tree/main/demo) contiene varios vídeos de demostración del funcionamiento de la webapp. Además, se han realizado visualizaciones en [`Tableau`]((https://public.tableau.com/views/supermercado_16862877278830/supermercado?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link) para constrastar los datos generados y las predicciones.

Debido a que los datos son extraídos y manejados a través de la base de datos en local, la estructura del proyecto se puede replicar en cuanto a manejo de la webapp, realizando el siguiente proceso:

- Clonar el repositorio en local.
- Generar una base de datos similar en `MySQL` ejecutando la consulta del archivo [`supermercado_structure.sql`](https://github.com/dapafer/auto_Pr-PSV/blob/main/demo/supermercado_structure.sql).
- Cargar y exportar los datos a la base de datos creada ejecutando el archivo [`supermercado_database.py`](https://github.com/dapafer/auto_Pr-PSV/blob/main/demo/supermercado_database.py).

**NOTA**: deberás cambiar las credenciales de conexión a la base de datos tuya propia (host, user, password...).

- Ejecutar el archivo [`Pr-PSV+.py`](https://github.com/dapafer/auto_Pr-PSV/blob/main/Pr-PSV%2B.py) en la Terminal, ubicándote en la carpeta principal de este repositorio, con el siguiente comando:

```
$ streamlit run Pr-PSV+.py
```
**NOTA**: deberás cambiar las credenciales de conexión a la base de datos tuya propia (host, user, password...).

<a name='proximos_objetivos'/>

### ✔️ **Próximos objetivos**

Los siguientes pasos para realizar son:
- Obtener más datos de  venta históricos, para poder entrenar mejor al modelo de predicciones.
- Escalar la herramienta a más categorías, concretamente a Carne y Pescado.
- Automatizar más el proceso y enriquecer más la herramienta.
