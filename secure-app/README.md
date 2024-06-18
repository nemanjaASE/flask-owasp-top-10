# Prikaz sigurne web aplikacije

## Postupak instalacije i pokretanja

### 1. Kreiranje i aktiviranje virtualnog okruženja

```shell
cd secure-app
python -m venv venv
# Na Windowsu
venv\Scripts\activate
# Na MacOS/Linux-u
source venv/bin/activate
```

### 2. Instaliranje zavisnosti

```shell
pip install -r requirements.txt
```

### 3. Pokretanje aplikacije

```shell
python run.py
```

Aplikaciji se pristupa na: http://127.0.0.1:5001/

### Napomena:

#### Za deaktivaciju virtualnog okruženja koristiti

```shell
deactivate
```
