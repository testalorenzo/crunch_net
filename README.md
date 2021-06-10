# crunch_net
## update June, 10th 2021
You need only to look at the new folder "data".



Crunchbase health care 51K firms - let's connect them

DATASETS
- partial: ultimo scraping ancora da unire. Please Marco check length of columns.
- tot1: prime 30K di aziende (più recenti) da sistemare data la presenza di doppioni (sraping non perfetto)...
- tot2: tutte i round con rispettivi investitori, città, regione, country, continente e coordinate città
- df_investors: info su investors, da sistemare

CODICI 
- network_scraping.py: file per scraping (disordinato e illeggibile)
- investors__scraping: file per scraping investors
- coordinates: file per sistemare il dataset from scraping e prendere coordinate

DRIVE
-df_tot_org: dati completi per le transazioni
-df_tot_inv: dati completi per investors
_Warning_: casi di omonimia regione-città
