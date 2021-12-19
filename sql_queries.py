# sql_queries.py

hier_rev = """
    DROP TABLE IF EXISTS tempTable;
    DROP TABLE IF EXISTS resultTable;
    
    CREATE TEMPORARY TABLE IF NOT EXISTS tempTable AS
    SELECT date, sales.product_id, sales, revenue, hierarchy1_id
    FROM sales
    JOIN product_hierarchy
        on sales.product_id = product_hierarchy.product_id
    WHERE hierarchy1_id = '{}' AND sales IS NOT NULL AND sales != 0 AND date BETWEEN '{}' AND '{}';
    
    CREATE TABLE IF NOT EXISTS resultTable AS
    SELECT sum(sales) AS quantity, SUM(revenue) AS revenue
    FROM tempTable
    """

city_rev = """
    DROP TABLE IF EXISTS tempTable;
    DROP TABLE IF EXISTS resultTable;
    
    CREATE TEMPORARY TABLE IF NOT EXISTS tempTable AS
    SELECT date, sales.product_id, sales, revenue, store_id, city_id 
    FROM sales
    JOIN store_cities 
        on sales.store_id = store_cities.store_id
    WHERE city_id = '{}' AND sales IS NOT NULL AND sales != 0 AND date BETWEEN '{}' AND '{}';
    
    CREATE TABLE IF NOT EXISTS resultTable AS
    SELECT sum(sales) AS quantity, SUM(revenue) AS revenue
    FROM tempTable
"""