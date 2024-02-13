# RecommenderSystem_TC

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
