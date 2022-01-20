BIDBID_STAGE_SELF_SINGLE
collegati due investitori se hanno investito in stessa company e stesso round. No decadenza. 
Self-arco pure. No loans. No line credit. Solo se data e ammontare disponibile.


Covariates.csv è stato creato tramite .ipnyb covariates da CB_covariates

Orgorg4 = togli tutto quello che concerne il debito, line of credit, loan - questo perché non vogliamo dare centralità ad investitori che mettono soldi in prestito. I link vengono fatti solo se in un round si tira su un ammontare di denaro diverso da 0 secondo CB insight. Orgorg4 è espansivo perché due startup sono collegate se hanno ricevuto un investimento a distanza massima di 7 anni (periodo di investimento medio che possiamo forse giustificare vedendo la letteratura). Due aziende non sono collegate se lo stesso investitore ha investito a distanza di 7 anni, se hanno il collegamento il collegamento nel corso del tempo rimarrà. 

Bidbid = aggiunto il self. Alcune misure, tipo la degree centrality, contano il fatto che ci sia un self_loop come degree. In teoria i due networks sono abbastanza puliti. Se c'erano cose su cui organizzarci. Due settimane. Coerente con investment period di un private equity fund. 

Puoi fare delle prove tra 5/10 anni e vedere come cambia in termini di robustezza. 
