## GNPS LCMS Visualization Dashboard

We typitcally will deploy this locally. To bring everything up

```server-compose```

### URL Parameters

1. usi
1. xicmz

### Heroku Deployment

We are also trying to support a heroku deployment. This is why we have a Procfile. 


### Example Sources of Data

1. GNPS Analysis Tasks - mzspec:GNPS:TASK-d93bdbb5cdda40e48975e6e18a45c3ce-f.mwang87/data/Yao_Streptomyces/roseosporus/0518_s_BuOH.mzXML:scan:171
1. GNPS/MassIVE public datasets - mzspec:MSV000084951:AH22:scan:62886
1. MassiVE Proteomics datasets - mzspec:MSV000079514:Adult_CD4Tcells_bRP_Elite_28_f01:scan:62886
1. MassiVE Proteomics dataset large - mzspec:MSV000083508:ccms_peak_centroided/pituitary_hypophysis/Trypsin_HCD_QExactiveplus/01697_A01_P018020_S00_N01_R2.mzML:scan:62886
1. Metabolights public datasets - mzspec:MTBLS1124:QC07.mzML:scan:1

### Example Use Cases

**Quick analysis of QC data**

Here is the USI for a QC run

mzspec:MSV000085852:QC_0:scan:62886

What we can easily do is paste in the QC molecules and pull them out in one fell swoop:

271.0315;278.1902;279.0909;285.0205;311.0805;314.1381

You can try it out at this URL: 

http://dorresteintesthub.ucsd.edu:6548/?usi=mzspec:MSV000085852:QC_0:scan:62886?xicmz=271