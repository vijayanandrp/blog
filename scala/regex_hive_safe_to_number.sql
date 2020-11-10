SELECT 

 CASE WHEN  '1234' RLIKE '(?!.{5,})^(0|-*[0-9]*)$|(?!.{6,})^-([0-9]*)$'
 THEN CAST("1234" AS INT) ELSE NULL END AS fillnum1 
 
, CASE WHEN  CAST('-1000' AS STRING) RLIKE '(?!.{5,})^([0-9]+)$|(?!.{6,})^-([0-9]+)$'
 THEN CAST("-1000" AS INT) ELSE NULL END AS fillnum1
 
, CASE WHEN  '0000' RLIKE '(?!.{5,})^([0-9]+)$|(?!.{6,})^-([0-9]+)$'
 THEN CAST("0000" AS INT) ELSE NULL END AS fillnum1
 
, CASE WHEN  '1' RLIKE '(?!.{5,})^([0-9]+)$|(?!.{6,})^-([0-9]+)$'
 THEN CAST("" AS INT) ELSE NULL END AS fillnum1
 
 , CASE WHEN  '-0001' RLIKE '(?!.{5,})^([0-9]+)$|(?!.{6,})^-([0-9]+)$'
 THEN CAST("-0001" AS INT) ELSE NULL END AS fillnum1
, CASE WHEN  'XYZ1' RLIKE '^(?!.{5,})^([0-9]+)$|(?!.{6,})^-([0-9]+)$'
 THEN CAST("" AS INT) ELSE NULL END AS fillnum1
 
, CASE WHEN  CAST('' AS STRING) RLIKE '(?!.{5,})^([0-9]+)$|(?!.{6,})^-([0-9]+)$'
 THEN 'EMPtY' ELSE NULL END AS fillnum1
 
from dual LIMIT 5000;

-- (?!.{5,})^([0-9]+)$|(?!.{6,})^-([0-9]+)$ (SKIP EMPTY STRING)
-- (?!.{5,})^(0|-*[0-9]*)$|(?!.{6,})^-([0-9]*)$
