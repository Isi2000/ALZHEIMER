# ALZHEIMER

## AGGIORNAMENTI PER COLLABORATORI

**27/10:** Il programma di download del dataset funziona! Va più veloce di quello che mi aspettassi. Salva i dati in formato json, servirebbe che qualcuno si imparasse un po' di big data analysis per capire un modo intelligente per costruire il grafo sfruttando il calcolo parallelo.

Eventualmente si potrebbe provare a scaricare tutti i 220000 articoli con le rispettive citazioni, ma ci sono alcune criticità:

- Bisognerebbe cambiare il sistema di acquisizione e fornire il parametro delle date all'url. In pratica molto semplice ma bisogna stare attenti a non acquisire dizionari vuoti per numeri di batch in certi intervalli di date che vanno oltre il numero di articoli. (spero sia chiaro) --> c'e' da scrivere del codice nuovo e assicurarsi che sia ben ottimizzato
- Il dataset diventerebbe enorme, quindi l'esperto di big data dovrebbe essere sicuro.
- Potrebbe volerci molto tempo per l'acquisizione di tutti i dati e occupare relativamente molto spazio in formato json, quindi serve una pianificazione abbastanza meticolosa in maniera tale da acquisirli bene al primo colpo senza dover stare a scancherare.
