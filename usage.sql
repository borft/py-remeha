SELECT 
	TO_CHAR(sample, 'YYYY-MM'),  
	MAX(verbruik_passief_koelen) - MIN(verbruik_passief_koelen) AS koelen, 
	MAX(verbruik_cv_compressor) - MIN(verbruik_cv_compressor) AS ch_cpr, 
	MAX(verbruik_cv_cpr_en_ee) - MIN(verbruik_cv_cpr_en_ee) AS ch_cpr_ee,
	MAX(verbruik_tapwater_compressor) - MIN(verbruik_tapwater_compressor) AS dhw_cpr, 
	MAX(verbruik_tapwater_cpree) - MIN(verbruik_tapwater_cpree) AS dwh_cpr_ee,
	MAX(verbruik_standby) - MIN(verbruik_standby) AS standby,
	MAX(verbruik_noodbedrijf_cv) - MIN(verbruik_noodbedrijf_cv) AS ch_emg,
	MAX(verbruik_noodbedrijf_tapwater) - MIN(verbruik_noodbedrijf_tapwater) AS dwh_emg,
	MAX(verbruik_regeneratie) - MIN(verbruik_regeneratie) AS reg,
	COUNT(*)/COUNT(DISTINCT(date(sample))) AS "# / day",
	COUNT(DISTINCT(date(sample))) AS "# days"
FROM remeha 
GROUP BY ROLLUP(TO_CHAR(sample, 'YYYY-MM') )
ORDER BY TO_CHAR(sample, 'YYYY-MM') desc;

