# Python Domain Check

Dit project bevat een Python-script dat informatie over domeinnamen verzamelt, zoals registratiegegevens, geolocatie, DNS-informatie en beschikbaarheid. Het script kan domeinnamen verwerken die via de command-line worden opgegeven of uit een bestand worden gelezen.

## Projectstructuur

Hieronder staat een overzicht van de bestanden in dit project en hun functies:

### Bestanden

- **`domain_lookup.py`**  
  Het hoofdscript van het project. Dit script verwerkt domeinnamen en genereert informatie zoals registrantgegevens, IP-adressen, geolocatie en beschikbaarheid.  
  **Gebruik:**  
  ```bash
  python domain_lookup.py <domeinnaam> [-v] [-o output_file] [-f input_file]
  ```
  **Opties:**
  - `-v`: Schakelt verbose-modus in voor meer gedetailleerde informatie.
  - `-o`: Schrijft de uitvoer naar een opgegeven bestand.
  - `-f`: Leest domeinnamen uit een bestand.

- **`domains.txt`**  
  Een tekstbestand met een lijst van domeinnamen die verwerkt kunnen worden door het script.

- **`domeinnamen.csv`**  
  Een CSV-bestand met een uitgebreide lijst van domeinnamen.

- **`activedomains.json`**  
  Een JSON-bestand met een lijst van actieve domeinnamen, inclusief duplicaten.

- **`activedomains_unique.json`**  
  Een JSON-bestand met een lijst van unieke actieve domeinnamen.

- **`activedomains_unique_sorted.json`**  
  Een JSON-bestand met een gesorteerde lijst van unieke actieve domeinnamen.

- **`output.txt`**  
  Een voorbeeldbestand waarin de uitvoer van het script wordt opgeslagen. Dit bestand bevat gedetailleerde informatie over de verwerkte domeinnamen.

- **`test.txt`**  
  Een leeg bestand dat mogelijk gebruikt kan worden voor testdoeleinden.

## Functionaliteiten

### Domeinvalidatie
Controleert of een domeinnaam geldig is en geen ongewenste tekens bevat.

### WHOIS-informatie ophalen
Verzamelt registratiegegevens van domeinen, zoals registrant, registrar en datums.

### Geolocatie ophalen
Bepaalt de geografische locatie van een domein op basis van het IP-adres.

### Beschikbaarheid controleren
Controleert of een domein beschikbaar is voor registratie.

### Uitvoer naar bestand
Schrijft de resultaten naar een opgegeven bestand.

## Voorbeeldgebruik

**Domein controleren via de command-line**
```bash
python domain_lookup.py example.com -v
```

**Domeinen uit een bestand verwerken**
```bash
python domain_lookup.py -f domains.txt -o output.txt
```

## Vereisten

- Python 3.x
- Vereiste Python-pakketten:
  - `requests`
  - `whois`
  - `certifi`

Installeer de vereisten met:
```bash
pip install -r requirements.txt
```

## Opmerkingen

- Zorg ervoor dat je een actieve internetverbinding hebt om WHOIS- en geolocatiegegevens op te halen.
- Het script kan fouten genereren als een domein niet bereikbaar is of als de WHOIS-server geen gegevens retourneert.

## Licentie

Dit project is vrij te gebruiken en aan te passen. Voeg een licentie toe als dat nodig is.

