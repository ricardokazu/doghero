SELECT
  *
FROM (
  SELECT
    city,
    AVG(Venda) AS number
  FROM
    [festive-ellipse-220919:dataset_test.imovelweb]
  GROUP BY
    city
  ORDER BY
    number DESC
  LIMIT
    10);
  -- (SELECT city, COUNT(title) as number
    -- FROM [festive-ellipse-220919:dataset_test.imovelweb]
    -- GROUP BY city
    -- ORDER BY number DESC
    -- LIMIT 5),
  -- (SELECT *
    -- FROM [festive-ellipse-220919:dataset_test.imovelweb]
    -- WHERE Aluguel IS NOT NULL
    -- ORDER BY price_rent_total
    -- LIMIT 5),
  -- (SELECT *
    -- FROM [festive-ellipse-220919:dataset_test.imovelweb]
    -- WHERE Aluguel IS NOT NULL
    -- ORDER BY price_rent_total DESC
    -- LIMIT 1);