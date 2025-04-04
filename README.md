# Python Domain Check

This project contains a Python script that gathers information about domain names, such as registration details, geolocation, DNS information, and availability. The script can process domain names provided via the command line or read from a file.

## Project Structure

Below is an overview of the files in this project and their functions:

### Files

- **`domain_lookup.py`**  
  The main script of the project. This script processes domain names and generates information such as registrant details, IP addresses, geolocation, and availability.  
  **Usage:**  
  ```bash
  python domain_lookup.py <domain_name> [-v] [-o output_file] [-f input_file]
  ```
  **Options:**
  - `-v`: Enables verbose mode for more detailed information.
  - `-o`: Writes the output to a specified file.
  - `-f`: Reads domain names from a file.

- **`domains.txt`**  
  A text file containing a list of domain names that can be processed by the script.

- **`domeinnamen.csv`**  
  A CSV file with an extensive list of domain names.

- **`activedomains.json`**  
  A JSON file containing a list of active domain names, including duplicates.

- **`activedomains_unique.json`**  
  A JSON file containing a list of unique active domain names.

- **`activedomains_unique_sorted.json`**  
  A JSON file containing a sorted list of unique active domain names.

- **`output.txt`**  
  A sample file where the script's output is stored. This file contains detailed information about the processed domain names.

- **`test.txt`**  
  An empty file that can be used for testing purposes.

- **`requirements.txt`**  
  A file listing the Python dependencies required to run the script.

## Features

### Domain Validation
Checks whether a domain name is valid and does not contain unwanted characters.

### Retrieve WHOIS Information
Collects registration details of domains, such as registrant, registrar, and dates.

### Retrieve Geolocation
Determines the geographical location of a domain based on its IP address.

### Check Availability
Checks if a domain is available for registration.

### Output to File
Writes the results to a specified file.

## Usage Examples

**Check a domain via the command line**
```bash
python domain_lookup.py example.com -v
```

**Process domains from a file**
```bash
python domain_lookup.py -f domains.txt -o output.txt
```

**Process domains from a CSV file**
```bash
python domain_lookup.py -f domeinnamen.csv -o output.txt
```

**Process domains from a CSV file in the `data` folder and save output to the `output` folder**
```bash
python domain_lookup.py -f data/domeinnamen.csv -o output/output.txt
```

### Steps:
1. Place your input file (e.g., `domeinnamen.csv`) in the `data` folder.
2. Ensure the `output` folder exists. If it doesn’t, create it using:
   ```bash
   mkdir output
   ```
3. Run the script with the `-f` flag pointing to the input file in the `data` folder and the `-o` flag pointing to the output file in the `output` folder.

## Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `whois`
  - `certifi`

Install the required packages with:
```bash
pip install -r requirements.txt
```

## Notes

- Ensure you have an active internet connection to retrieve WHOIS and geolocation data.
- The script may generate errors if a domain is unreachable or if the WHOIS server does not return data.
- IP-API has a limit of 45 requests per minute per IP. If you exceed this limit, you may be temporarily banned for an hour.
- The script supports both `.txt` and `.csv` files for input.

## License

This project is free to use and modify.

## Credit

I want to give some credit to slyfox1186 for making his code free to use, Making it possible for me to use some parts of his code.