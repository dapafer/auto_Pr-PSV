-- VENTA

-- Venta total por CATEGORÍA:
-- obtener venta por "categoria", "fecha" y "dia"
SELECT v.fecha, v.dia_semana, c.categoria, SUM(vp.venta) AS venta
FROM ventas v
JOIN ventas_productos vp ON v.venta_id = vp.venta_id
JOIN productos p ON vp.producto_id = p.producto_id
JOIN categorias c ON p.categoria_id = c.categoria_id
WHERE c.categoria_id = 1
GROUP BY v.fecha, v.dia_semana, c.categoria;

-- obtener venta por "categoria", "fecha" y "dia" específico
SELECT v.fecha, v.dia_semana, c.categoria, SUM(vp.venta) AS venta
FROM ventas v
JOIN ventas_productos vp ON v.venta_id = vp.venta_id
JOIN productos p ON vp.producto_id = p.producto_id
JOIN categorias c ON p.categoria_id = c.categoria_id
WHERE c.categoria_id = 1 AND v.dia_semana = 'lunes'
GROUP BY v.fecha, v.dia_semana, c.categoria;



-- Venta total por SUBCATEGORÍA:
-- obtener venta total por "subcategoria", "fecha" y "dia"
SELECT v.fecha, v.dia_semana, s.subcategoria, SUM(vp.venta) AS venta
FROM ventas v
JOIN ventas_productos vp ON v.venta_id = vp.venta_id
JOIN productos p ON vp.producto_id = p.producto_id
JOIN subcategorias s ON p.subcategoria_id = s.subcategoria_id
WHERE s.subcategoria_id = 1
GROUP BY v.fecha, v.dia_semana, s.subcategoria;

-- obtener venta por "subcategoria", "fecha" y "dia" específico
SELECT v.fecha, v.dia_semana, s.subcategoria, SUM(vp.venta) AS venta
FROM ventas v
JOIN ventas_productos vp ON v.venta_id = vp.venta_id
JOIN productos p ON vp.producto_id = p.producto_id
JOIN subcategorias s ON p.subcategoria_id = s.subcategoria_id
WHERE s.subcategoria_id = 1 AND v.dia_semana = 'lunes'
GROUP BY v.fecha, v.dia_semana, s.subcategoria;



-- Venta total por PRODUCTO:
-- obtener venta por "formato", "producto", "categoria", "fecha" y "dia"
SELECT v.fecha, v.dia_semana, c.categoria, p.producto, p.formato, vp.venta
FROM ventas v
JOIN ventas_productos vp ON v.venta_id = vp.venta_id
JOIN productos p ON vp.producto_id = p.producto_id
JOIN categorias c ON p.categoria_id = c.categoria_id
WHERE c.categoria_id = 1
GROUP BY v.fecha, v.dia_semana, c.categoria, p.producto, p.formato, vp.venta, p.producto_id
ORDER BY v.fecha ASC, p.producto_id ASC;

-- obtener venta por "producto", "categoria", "fecha" y "dia" específico
SELECT v.fecha, v.dia_semana, c.categoria, p.producto, vp.venta
FROM ventas v
JOIN ventas_productos vp ON v.venta_id = vp.venta_id
JOIN productos p ON vp.producto_id = p.producto_id
JOIN categorias c ON p.categoria_id = c.categoria_id
WHERE c.categoria_id = 1 AND v.dia_semana = 'lunes'
GROUP BY v.fecha, v.dia_semana, c.categoria, p.producto, vp.venta, p.producto_id
ORDER BY v.fecha ASC, p.producto_id ASC;
