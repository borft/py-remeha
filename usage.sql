SELECT 
	TO_CHAR(sample, 'YYYY-MM'),  
	MAX(verbruik_passief_koelen) - MIN(verbruik_passief_koelen) AS koelen, 
	MAX(verbruik_cv_compressor) - MIN(verbruik_cv_compressor) AS verwarmen_wp, 
	MAX(verbruik_cv_cpr_en_ee) - MIN(verbruik_cv_cpr_en_ee) AS verwarmen_element,
	MAX(verbruik_tapwater_compressor) - MIN(verbruik_tapwater_compressor) AS warm_water, 
	MAX(verbruik_standby) - MIN(verbruik_standby) AS standby
FROM remeha 
GROUP BY ROLLUP(TO_CHAR(sample, 'YYYY-MM') )
ORDER BY TO_CHAR(sample, 'YYYY-MM') desc;

