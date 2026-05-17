SET SESSION group_concat_max_len = 2000000;

SET @db_name = 'power_trading';
SET @table_name = 'iex_weather_final';

SELECT GROUP_CONCAT(query SEPARATOR ' UNION ALL ')
INTO @final_query
FROM (
    SELECT CONCAT(
        'SELECT ''', COLUMN_NAME, ''' AS column_name, ',

        'AVG(t.`', COLUMN_NAME, '`) AS mean, ',

        '(SELECT AVG(m.val) FROM (',
            'SELECT `', COLUMN_NAME, '` AS val, ',
            'ROW_NUMBER() OVER (ORDER BY `', COLUMN_NAME, '`) AS rn, ',
            'COUNT(*) OVER () AS cnt ',
            'FROM `', @db_name, '`.`', @table_name, '` ',
            'WHERE `', COLUMN_NAME, '` IS NOT NULL',
        ') m ',
        'WHERE m.rn IN (FLOOR((m.cnt + 1)/2), FLOOR((m.cnt + 2)/2))) AS median, ',

        '(SELECT `', COLUMN_NAME, '` FROM `', @db_name, '`.`', @table_name, '` ',
        'WHERE `', COLUMN_NAME, '` IS NOT NULL ',
        'GROUP BY `', COLUMN_NAME, '` ',
        'ORDER BY COUNT(*) DESC, `', COLUMN_NAME, '` ASC LIMIT 1) AS mode ',

        'FROM `', @db_name, '`.`', @table_name, '` t ',
        'WHERE t.`', COLUMN_NAME, '` IS NOT NULL'
    ) AS query
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @db_name
      AND TABLE_NAME = @table_name
      AND DATA_TYPE IN (
          'int','bigint','smallint','tinyint','mediumint',
          'decimal','numeric','float','double','real'
      )
) q;

SELECT @final_query;

PREPARE stmt FROM @final_query;
EXECUTE stmt;

SET SESSION group_concat_max_len = 2000000;

SET @db_name = 'power_trading';
SET @table_name = 'iex_weather_final';

SELECT GROUP_CONCAT(query SEPARATOR ' UNION ALL ')
INTO @final_query
FROM (
    SELECT CONCAT(
        'SELECT ''', COLUMN_NAME, ''' AS column_name, ',
        'VAR_POP(`', COLUMN_NAME, '`) AS variance, ',
        'STDDEV_POP(`', COLUMN_NAME, '`) AS standard_deviation, ',
        'MIN(`', COLUMN_NAME, '`) AS minimum_value, ',
        'MAX(`', COLUMN_NAME, '`) AS maximum_value, ',
        'MAX(`', COLUMN_NAME, '`) - MIN(`', COLUMN_NAME, '`) AS range_value ',
        'FROM `', @db_name, '`.`', @table_name, '` ',
        'WHERE `', COLUMN_NAME, '` IS NOT NULL'
    ) AS query
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @db_name
      AND TABLE_NAME = @table_name
      AND DATA_TYPE IN (
          'int','bigint','smallint','tinyint','mediumint',
          'decimal','numeric','float','double','real'
      )
) q;

SELECT @final_query;

PREPARE stmt FROM @final_query;
EXECUTE stmt;

SET SESSION group_concat_max_len = 2000000;

SET @db_name = 'power_trading';
SET @table_name = 'iex_weather_final';

SELECT GROUP_CONCAT(query SEPARATOR ' UNION ALL ')
INTO @final_query
FROM (
    SELECT CONCAT(
        'SELECT ''', COLUMN_NAME, ''' AS column_name, ',
        'COUNT(`', COLUMN_NAME, '`) AS n, ',

        'AVG(POWER((`', COLUMN_NAME, '` - stats.mean_val) / NULLIF(stats.std_val, 0), 3)) AS skewness, ',

        'AVG(POWER((`', COLUMN_NAME, '` - stats.mean_val) / NULLIF(stats.std_val, 0), 4)) AS kurtosis, ',

        'AVG(POWER((`', COLUMN_NAME, '` - stats.mean_val) / NULLIF(stats.std_val, 0), 4)) - 3 AS excess_kurtosis ',

        'FROM `', @db_name, '`.`', @table_name, '` ',
        'CROSS JOIN (',
            'SELECT AVG(`', COLUMN_NAME, '`) AS mean_val, ',
            'STDDEV_POP(`', COLUMN_NAME, '`) AS std_val ',
            'FROM `', @db_name, '`.`', @table_name, '` ',
            'WHERE `', COLUMN_NAME, '` IS NOT NULL',
        ') stats ',
        'WHERE `', COLUMN_NAME, '` IS NOT NULL'
    ) AS query
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = @db_name
      AND TABLE_NAME = @table_name
      AND DATA_TYPE IN (
          'int','bigint','smallint','tinyint','mediumint',
          'decimal','numeric','float','double','real'
      )
) q;

SELECT @final_query;

PREPARE stmt FROM @final_query;
EXECUTE stmt;

DEALLOCATE PREPARE stmt;

