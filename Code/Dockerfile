# Offizielles Python Runtime als Basisimage verwenden
FROM python:3.9-slim

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Abhängigkeiten kopieren
COPY requirements.txt .

# Benötigte Pakete installieren
RUN pip install --no-cache-dir -r requirements.txt

# Den Inhalt des lokalen src-Verzeichnisses in das Arbeitsverzeichnis kopieren
COPY . .

# Befehl, der beim Start des Containers ausgeführt wird
# Startet die Flask-App über app.py, wo app.run() definiert ist
CMD ["python", "app.py"]