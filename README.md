# Python Domain Check

This project contains a Python script and a PHP-based web interface that gathers information about domain names, such as registration details, geolocation, DNS information, and availability. The script can process domain names provided via the command line, read from a file, or uploaded via the web interface.

## Project Structure

Below is an overview of the files in this project and their functions:

### Files

- **`domain_lookup.py`**  
  The main script of the project. This script processes domain names and generates information such as registrant details, IP addresses, geolocation, and availability.  
  **Usage:**  
  ```bash
  python domain_lookup.py <domain_name> [-v] [-o output_file] [-f input_file] [-l limit]
  ```
  **Options:**
  - `-v` : Enables verbose mode for more detailed information.
  - `-o` : Writes the output to a specified file.
  - `-f` : Reads domain names from a file.
  - `-l` : Limits the number of domains processed from the input file.

- **`index.php`**  
  The main PHP file for the web interface. It allows users to upload a file of domain names, process them using the Python script, and view the results in real-time.

- **`kill_script.py`**  
  A Python script that terminates the `domain_lookup.py` process if it is running. This is triggered via the "Kill Running Script" button in the web interface.

- **`kill_script.php`**  
  A PHP script that executes `kill_script.py` to terminate the running Python process.

- **`style.css`**  
  The CSS file for styling the web interface, including buttons for uploading files, killing the script, and downloading results.

- **`output/output.txt`**  
  The file where the Python script writes its results. This file is updated in real-time and can be downloaded via the web interface.

- **`requirements.txt`**  
  A file listing the Python dependencies required to run the script.

## Features

- **Domain Validation**  
  Checks whether a domain name is valid and does not contain unwanted characters.

- **Retrieve WHOIS Information**  
  Collects registration details of domains, such as registrant, registrar, and dates.

- **Retrieve Geolocation**  
  Determines the geographical location of a domain based on its IP address.

- **Check Availability**  
  Checks if a domain is available for registration.

- **Limit the Number of Domains**  
  Allows you to limit the number of domains processed from an input file using the `-l` flag.

- **Real-Time Results**  
  The web interface fetches and displays results in real-time as the Python script processes the domains.

- **Kill Running Script**  
  A "Kill Running Script" button in the web interface allows you to terminate the Python script if it is running.

- **Output to File**  
  Writes the results to a specified file (`output/output.txt`), which can be downloaded via the web interface.

## Usage Examples

### Command-Line Usage

- Check a domain via the command line:
  ```bash
  python domain_lookup.py example.com -v
  ```

- Process domains from a file:
  ```bash
  python domain_lookup.py -f domains.txt -o output.txt
  ```

- Process domains from a CSV file:
  ```bash
  python domain_lookup.py -f domeinnamen.csv -o output.txt
  ```

- Process domains from a CSV file in the `data` folder and save output to the `output` folder:
  ```bash
  python domain_lookup.py -f data/domeinnamen.csv -o output/output.txt
  ```

- Limit the number of domains processed:
  ```bash
  python domain_lookup.py -f data/domeinnamen.csv -o output/output.txt -l 200
  ```

### Web Interface Usage

1. Open the web interface in your browser (e.g., `http://localhost`).
2. Upload a file containing domain names (e.g., `domeinnamen.csv`).
3. Optionally, specify a limit for the number of domains to process.
4. Click "Process Domains" to start the Python script.
5. View the results in real-time in the "Real-Time Results" section.
6. Download the results using the "Download Output" button.
7. If needed, click "Kill Running Script" to terminate the Python script.

## Steps to Set Up

### Command-Line Setup

1. Place your input file (e.g., `domeinnamen.csv`) in the `data` folder.
2. Ensure the `output` folder exists. If it doesn’t, create it using:
   ```bash
   mkdir output
   ```
3. Run the script with the `-f` flag pointing to the input file in the `data` folder and the `-o` flag pointing to the output file in the `output` folder.
4. Optionally, use the `-l` flag to limit the number of domains processed.

### Web Interface Setup

1. Place all project files (`index.php`, `kill_script.py`, `domain_lookup.py`, `style.css`, etc.) in your web server's root directory (e.g., `Python_domaincheck`).
2. Ensure the `output` folder exists and is writable by the web server.
3. Start your web server (e.g., WAMP or XAMPP).
4. Open the web interface in your browser (e.g., `http://localhost/Python_domaincheck`).

## Requirements

- **Python 3.x**
- Required Python packages:
  - `requests`
  - `whois`
  - `psutil`
- Install the required packages with:
  ```bash
  pip install -r requirements.txt
  ```

## Notes

- Ensure you have an active internet connection to retrieve WHOIS and geolocation data.
- The script may generate errors if a domain is unreachable or if the WHOIS server does not return data.
- **IP-API has a limit of 45 requests per minute per IP.** If you exceed this limit, you may be temporarily banned for an hour.
- The script supports both `.txt` and `.csv` files for input.

## License

This project is free to use and modify.

## Credit

Acknowledgment goes to **slyfox1186** for making their code freely available, which allowed me to incorporate and adapt certain parts into this project.