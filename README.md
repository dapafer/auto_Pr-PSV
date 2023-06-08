# **Pr-PSV+**

![portada](https://github.com/dapafer/auto_Pr-PSV/blob/main/images/sales_preds.png)

***

Pr-PSV+ es la mejora de la herramienta de gestión y control de pedidos de un supermercado, para las categorías de productos frescos, concretamente Fruta y verdura, Carne y Pescado. La mejora de la herramienta consiste en generar previsiones de venta futura en base a un modelo de predicción de series temporales, concretamente [Prophet](https://facebook.github.io/prophet/).

---
## 📌 **Índice.**

- [Contenido.](#contenido)
- [Problemas.](#problemas)
- [Soluciones.](#fact_tot)
- [Desarrollo.](#fact_tot_sub)
- [Demo.](#fact_tot_sub)
- [Próximos objetivos.](#prod_cat)

---
<a name="contenido"/>

### 📂 **Contenido**

El proyecto cuenta con la siguiente estructura principal:

- [`data`](https://github.com/dapafer/auto_Pr-PSV/tree/main/data): carpeta que contiene todos los archivos generados durante el desarrollo del proyecto, subdividida por cada proceso.
- [`demo`](https://github.com/dapafer/auto_Pr-PSV/tree/main/demo): carpeta principal para replicar la app web realizada, a través de los archivos que la contienen.
- [`src`](https://github.com/dapafer/auto_Pr-PSV/tree/main/src): carpeta principal con notebooks del proceso, y scripts de pruebas de `SQL`.
- [`Pr-PSV+.py`](https://github.com/dapafer/auto_Pr-PSV/blob/main/Pr-PSV%2B.py): script de ejecución de la app web, que simula la herramienta de gestión y control de pedidos.

---
<a name="problemas"/>

### ❗️ **Problemas**

El planteamiento de partida es analizar los problemas que tiene actualmente la herramienta. Principalmente son:

- Para realizar un pedido, las previsiones de una categoría se realizan basándose en un "ancla" (histórico de ventas de una fecha similar) de manera manual.
- Los pedidos se realizan y modifican en base a la "experiencia" que tiene la persona que lo realiza, la cual si no posee esa experiencia, el proceso de generar previsiones acordes es complicado.
- Solo se pueden realizar pedidos para el día siguiente al que se realizan, por tanto no es escalable a más fechas futuras.

---
<a name="soluciones"/>

### 💡 **Soluciones**

Por ello, se ha aplicado un modelo de generación de predicciones, que ha podido generar soluciones para mejorar la herramienta, las cuales son:

- Las previsiones se generan de manera automática en base a un histórico de ventas.
- No hace falta tener experiencia en la categoría para la cual se realiza el pedido, debido a esa generación automática de previsiones basadas en el modelo de aprendizaje automático.
- La herramienta puede generar pedidos para más fechas, debido a que genera predicciones para un número específico dado de fechas, no solo para el día siguiente al cual se realiza el pedido.

---
<a name="desarrollo"/>

### ▶️ **Desarrollo**

El desarrollo del proyecto ha tenido las siguientes etapas principales:

- **Web scraping & API**: 