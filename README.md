# TC Recommender API

### Introduzione
Lo scopo del progetto TC Reccomender AI consiste nella realizzazione di un modulo di intelligenza arti-
ficiale, il quale dovrà essere integrato nel sito web Turing Careers; il modulo permetterà agli utenti di 
ottenere raccomandazioni adatte al tipo di utente, in particolare:
- Raccomandazione di Offerte di Lavoro a Sviluppatori;
- Raccomandazione di Profili di Sviluppatori a Datori di Lavoro;

Per quanto riguarda la realizzazione del sistema è possibile visionare:
- I Jupyter Notebook all'interno del package *[notebooks]*(https://github.com/antoninoLorenzo/RecommenderSystem_TC/tree/main/notebooks).
- La documentazione contenuta nel package *[docs]*(https://github.com/antoninoLorenzo/RecommenderSystem_TC/tree/main/docs).

### Installazione
**Dipendenze TC Recommender**:
- Python >= 3.12
- MySQL 8.0
- Terminale Bash


1. Clona la repository:
```
git clone https://github.com/antoninoLorenzo/RecommenderSystem_TC.git
```

2. Crea il database:
```
mysql -u[username] -p[password] < ./database/tabelleTuringCareers.sql && mysql -u[username -p[password] turing_careers < ./database/db_populator.db
```

3. Installa i package necessari tramite il seguente comando:
```
pip install -r requirements.txt
```
4. Esegui il seguente comando tramite un terminale bash specificando l'indirizzo su cui è stato 
effettuato il deploy del del database come [ip:port/connection] (es. localhost:3306/turing_careers), poi il nume utente e la password:
```
nohup python launcher.py —db-address [ip:port/connection] —db-user [Nome Utente] —db-psw [Password] > log.txt & echo $! > pid.txt
```

5. Apri le pagine demo nel package *[demo]*(https://github.com/antoninoLorenzo/RecommenderSystem_TC/tree/main/demo).

*Nota: Per l'installazione dell'intero sistema occorre seguire le istruzioni nella repository [Core](https://github.com/JacopoPassariello/TuringCareers)*
