SELECT 
	TO_CHAR(sample, 'YYYY-MM'),  
	MAX(verbruik_passief_koelen) - MIN(verbruik_passief_koelen) AS koelen, 
	MAX(verbruik_cv_compressor) - MIN(verbruik_cv_compressor) AS verwarmen, 
	MAX(verbruik_tapwater_compressor) - MIN(verbruik_tapwater_compressor) AS warm_water 
FROM remeha 
GROUP BY TO_CHAR(sample, 'YYYY-MM') 
ORDER BY TO_CHAR(sample, 'YYYY-MM') desc;

