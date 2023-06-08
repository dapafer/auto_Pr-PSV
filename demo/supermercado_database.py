#!/usr/bin/env python
# coding: utf-8

# # **SUPERMERCADO DATABASE to MySQL Workbench**

# ## **Importar librerías**

# In[1]:


import warnings
warnings.filterwarnings('ignore')

import pandas as pd


# In[2]:


# generar estructura de tablas y datos para exportar
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database, drop_database


# ## **Cargar datos**

# In[3]:


# dataframes para exportar a base de datos "supermercado"
categorias = pd.read_csv('../data/categorias.csv')

subcategorias = pd.read_csv('../data/subcategorias.csv')

productos = pd.read_csv('../data/productos.csv')

ventas = pd.read_csv('../data/ventas.csv')

ventas_productos = pd.read_csv('../data/ventas_productos.csv')


# ## **Crear base de datos**

# In[4]:


# crear conexión con base de datos en MySQL Workbench
str_conn = 'mysql+pymysql://root:password@localhost:3306/supermercado'
cursor = create_engine(str_conn)


# In[5]:


# crear base de datos y sesión
Base = declarative_base()
Session = sessionmaker(bind=cursor)
session = Session()


# ## **Crear tablas**

# ### **Categorías**

# In[6]:


# crear clase para la tabla "categorias"
class Categoria(Base):
    __tablename__ = 'categorias'
    categoria_id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(String(50), nullable=False)

    # relación con tabla "subcategorias"
    subcategorias = relationship('Subcategoria', back_populates='categorias')

    # relación con tabla "productos"
    productos = relationship('Producto', back_populates='categorias')

    # relación con tabla "ventas"
    ventas = relationship('Venta', back_populates='categorias')


# ### **Subcategorías**

# In[7]:


class Subcategoria(Base):
    __tablename__ = 'subcategorias'
    subcategoria_id = Column(Integer, primary_key=True, autoincrement=True)
    subcategoria = Column(String(50), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'), nullable=False)

    # relación con tabla "productos"
    productos = relationship('Producto', back_populates='subcategorias')

    # relación con tabla "categorias"
    categorias = relationship('Categoria', back_populates='subcategorias')


# ### **Productos**

# In[8]:


class Producto(Base):
    __tablename__ = 'productos'
    producto_id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String(50), nullable=False)
    formato = Column(String(50), nullable=False)
    precio = Column(String(50), nullable=False)
    subcategoria_id = Column(Integer, ForeignKey('subcategorias.subcategoria_id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'), nullable=False)
    
    # relación con tabla "ventas_productos"
    ventas_productos = relationship('VentaProducto', back_populates='productos')

    # relación con tabla "subcategorias"
    subcategorias = relationship('Subcategoria', back_populates='productos')

    # relación con tabla "categorias"
    categorias = relationship('Categoria', back_populates='productos')


# ### **Ventas**

# In[9]:


class Venta(Base):
    __tablename__ = 'ventas'
    venta_id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    dia_semana = Column(String(20), nullable=False)
    numero_semana = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.categoria_id'), nullable=False)
    lluvia = Column(String(20), nullable=False)
    temperatura_minima = Column(Float, nullable=False)
    temperatura_maxima = Column(Float, nullable=False)
    
    # relación con tabla "ventas_productos"
    ventas_productos = relationship('VentaProducto', back_populates='ventas')

    # relación con tabla "categorias"
    categorias = relationship('Categoria', back_populates='ventas')


# ### **Ventas-Productos**

# In[10]:


class VentaProducto(Base):
    __tablename__ = 'ventas_productos'
    venta_id = Column(Integer, ForeignKey('ventas.venta_id'), primary_key=True)
    producto_id = Column(Integer, ForeignKey('productos.producto_id'), primary_key=True)
    venta = Column(Integer, nullable=False)
    prevision = Column(Integer, nullable=False)
    
    # relación con tabla "ventas"
    ventas = relationship('Venta', back_populates='ventas_productos')

    # relación con tabla "productos"
    productos = relationship('Producto', back_populates='ventas_productos')


# ## **Verificar tablas existentes**

# In[11]:


# nombre tablas que deseas verificar y eliminar
table_names = ['ventas_productos', 'ventas', 'productos', 'subcategorias', 'categorias']

# crear un objeto MetaData
metadata = MetaData(bind=cursor)

# verificar y eliminar tablas existentes
for table_name in table_names:
    if cursor.has_table(table_name):
        table = Table(table_name, metadata, autoload=True)
        table.drop(cursor)


# ## **Exportar datos**

# In[12]:


# crear tablas en base de datos "supermercado"
Base.metadata.create_all(cursor)


# In[13]:


# convertir tablas en listas de diccionarios para exportacion
cat_data = categorias.to_dict(orient='records')

sub_data = subcategorias.to_dict(orient='records')

prod_data = productos.to_dict(orient='records')

vent_data = ventas.to_dict(orient='records')

vent_prod_data = ventas_productos.to_dict(orient='records')


# In[14]:


# insertar datos en base de datos "supermercado"
for row in cat_data:
    categoria = Categoria(categoria=row['categoria'])
    session.add(categoria)

for row in sub_data:
    subcategoria = Subcategoria(subcategoria=row['subcategoria'], categoria_id=row['categoria_id'])
    session.add(subcategoria)

for row in prod_data:
    producto = Producto(producto=row['producto'], formato=row['formato'], precio=row['precio'], subcategoria_id=row['subcategoria_id'], categoria_id=row['categoria_id'])
    session.add(producto)

for row in vent_data:
    venta = Venta(fecha=row['fecha'], dia_semana=row['dia_semana'], numero_semana=row['numero_semana'], categoria_id=row['categoria_id'], lluvia=row['lluvia'], temperatura_minima=row['temperatura_minima'], temperatura_maxima=row['temperatura_maxima'])
    session.add(venta)

for row in vent_prod_data:
    venta_producto = VentaProducto(venta_id=row['venta_id'], producto_id=row['producto_id'], venta=row['venta'], prevision=row['prevision'])
    session.add(venta_producto)

session.commit()

