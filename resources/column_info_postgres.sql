SELECT
    t.column_name
  , UPPER(data_type)             AS data_type
  , is_nullable
  , COALESCE(column_default, '') AS column_default
  , COALESCE(column_constr, '')  AS column_constr
  , COALESCE(description, '')    AS description
FROM
    (SELECT
         column_name
       , data_type
       , CASE WHEN is_nullable = 'YES' THEN 'Нет' ELSE 'Да' END                                AS is_nullable
       , CASE WHEN column_default LIKE 'nextval%' THEN 'Автоинкримент' ELSE column_default END AS column_default
       , pgd.description
    FROM
        pg_catalog.pg_statio_all_tables st
            JOIN information_schema.columns c ON c.table_schema = st.schemaname AND
                                                 c.table_name = st.relname
            LEFT JOIN pg_catalog.pg_description pgd ON pgd.objoid = st.relid
            AND pgd.objsubid = c.ordinal_position
    WHERE
        c.table_name = '{table_name}') t
        LEFT JOIN (SELECT
                       column_name
                     , STRING_AGG(column_constr, ', ') AS column_constr
    FROM
        (SELECT
             CASE
                 WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'PK'
                 ELSE
                     CASE
                         WHEN tc.constraint_type = 'FOREIGN KEY' THEN 'FK [' || ccu.table_name || '.' || ccu.column_name
                                                                          || '](/home/СУБД/Структура-баз-данных-ЕГАИС/'
                                                                          || tc.table_catalog || '/' || ccu.table_name ||
                                                                      ')'
                         ELSE tc.constraint_type END END AS column_constr
           , kcu.column_name
        FROM
            information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                     ON tc.constraint_name = kcu.constraint_name
                         AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                     ON ccu.constraint_name = tc.constraint_name
        WHERE
            tc.table_name = '{table_name}') it
    GROUP BY
        column_name) t1 ON t.column_name = t1.column_name;