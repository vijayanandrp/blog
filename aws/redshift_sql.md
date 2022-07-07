```sql
SELECT MAX(TO_DATE(REGEXP_SUBSTR(values, '[0-9]{8}'), 'YYYYMMDD', FALSE)) AS max_date,
       MIN(TO_DATE(REGEXP_SUBSTR(values, '[0-9]{8}'), 'YYYYMMDD', FALSE)) AS min_date
FROM SVV_EXTERNAL_PARTITIONS
WHERE schemaname = 'spectrum_tables'
  AND tablename = 'facebook_report';
```
