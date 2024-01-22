# RecommenderSystem_TC

## TODO
**Dataset Offerte**
- Descrizioni incomplete
- Lingua richiesta non acquisita correttamente (sempre 'Italiano')
- Debug della procedura di pulizia per le Location ([demo/notebooks/location_cleaning.py](https://github.com/antoninoLorenzo/RecommenderSystem_TC/blob/main/demo/notebooks/location_cleaning.py))

**Dataset Developer**
- La generazione dipenda da Dataset Offerte e Dataset Skill, in particolare bisognerebbe prevedere l'uso di una porzione/un dataset completamente diverso per le Offerte in modo da non introdurre bias nell'utilizzo dei dataset durante la progettazione del sistema di raccomandazione.

## Link Utili
[indbscan](https://pypi.org/project/incdbscan/) : Implementazione dell'algoritmo DBSCAN Iterativo, permette l'aggiunta e la rimozione di Item dai Cluster generati.
