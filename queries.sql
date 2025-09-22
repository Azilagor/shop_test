#Сумма товаров заказанных каждым клиентом
SELECT c.name AS client_name,
       SUM(oi.quantity * p.price) AS total_sum
FROM clients c
JOIN orders o ON o.client_id = c.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
GROUP BY c.name
ORDER BY total_sum DESC;


#Просмотр дочерних элементов для категорий
SELECT parent.id AS category_id,
       parent.name AS category_name,
       COUNT(child.id) AS children_count
FROM categories parent
LEFT JOIN categories child ON child.parent_id = parent.id
GROUP BY parent.id, parent.name
ORDER BY parent.id;


#Топ 5 самых покупаемых товаров за месяц
SELECT p.name AS product_name,
       (SELECT c1.name
        FROM categories c1
        WHERE c1.id = (
            SELECT c2.id
            FROM categories c2
            WHERE c2.id = p.category_id
            AND c2.parent_id IS NULL
            LIMIT 1
        )
       ) AS root_category,
       SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o ON o.id = oi.order_id
WHERE o.order_date >= NOW() - INTERVAL '1 month'
GROUP BY p.id, p.name, p.category_id
ORDER BY total_sold DESC
LIMIT 5;


#Оптимизация, создание индексов
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_products_category ON products(category_id);
