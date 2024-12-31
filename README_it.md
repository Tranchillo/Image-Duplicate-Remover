
# Image Duplicate Remover

## Descrizione
**Image Duplicate Remover** è uno script Python progettato per identificare immagini duplicate in una cartella, raggrupparle in base alla loro somiglianza e produrre un set unico di immagini. Lo script utilizza algoritmi di hashing e calcolo della similarità per confrontare le immagini.

### Funzionalità principali:
- Raggruppa immagini simili in cartelle dedicate.
- Estrae un'immagine rappresentativa da ciascun gruppo e la sposta nella cartella delle immagini non simili.
- Rimuove automaticamente le cartelle dei gruppi dopo aver estratto le immagini rappresentative.

---

## Requisiti
Assicurati di avere Python 3.7 o versioni successive installato. Inoltre, lo script richiede le seguenti librerie Python:

- `numpy`
- `Pillow`
- `scikit-image`
- `imagehash`

---

## Installazione delle dipendenze
### Metodo 1: Utilizzo di un ambiente virtuale (consigliato)
1. Crea un ambiente virtuale:
   ```bash
   python -m venv venv
   ```
2. Attiva l'ambiente virtuale:
   - Su Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Su macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. Installa le dipendenze richieste:
   ```bash
   pip install numpy Pillow scikit-image imagehash
   ```
4. Esegui lo script all'interno dell'ambiente virtuale.

### Metodo 2: Installazione globale
Esegui il seguente comando per installare le dipendenze nel tuo ambiente globale di Python:
```bash
pip install numpy Pillow scikit-image imagehash
```

---

## Utilizzo
1. Posiziona le immagini da elaborare nella cartella `input_images`. Se la cartella non esiste, verrà creata automaticamente al primo avvio dello script.
2. Esegui lo script utilizzando il seguente comando:
   ```bash
   python image_duplicate_remover.py
   ```
3. Una volta completata l'elaborazione:
   - Tutte le immagini uniche saranno salvate nella cartella `grouped_images/non_similar_images`.
   - Le cartelle dei gruppi (`group_`) verranno rimosse automaticamente.

---

## Esempio di struttura delle cartelle
Dopo l'elaborazione, la struttura delle cartelle sarà simile a questa:

```
input_images/
grouped_images/
    └── non_similar_images/
```

---

## Note
- Lo script funziona con i seguenti formati di immagine: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff`.
- Eventuali conflitti di nomi tra le immagini nella cartella `non_similar_images` verranno risolti automaticamente con una numerazione aggiuntiva.

---

## Supporto
Per qualsiasi problema o suggerimento, sentiti libero di contattare l'autore.
