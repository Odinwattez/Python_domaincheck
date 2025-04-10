from flask import Flask, request, jsonify, Response, send_from_directory
import os
import socket
from datetime import datetime
import requests
import whois
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory to store uploaded files
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure the directory exists

# Validate the domain to ensure it does not contain any unexpected characters
def validate_domain(domain):
    import re
    if not re.match(r"^[a-zA-Z0-9-\.]+$", domain):
        return None
    return domain

# Format date objects for output
def format_dates(dates):
    if isinstance(dates, list):
        return dates[0].strftime('%m-%d-%Y %H:%M:%S UTC')
    elif dates:
        return dates.strftime('%m-%d-%Y %H:%M:%S UTC')
    else:
        return "N/A"

# Get the reverse DNS record for an IP address
def get_reverse_ip(ip_address):
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return "No reverse DNS record found"
    except Exception as e:
        return f"Error retrieving hostname - {e}"

# Fetch geolocation information for an IP address
def get_geolocation(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{validate_domain(ip_address)}", timeout=5)
        data = response.json()
        return f"Country: {data['country']}, City: {data['city']}, ISP: {data['isp']}"
    except Exception as e:
        return "Error retrieving geolocation"

# Calculate the age of the domain based on its creation date
def calculate_domain_age(creation_date):
    if isinstance(creation_date, list):
        creation_date = creation_date[0]
    if creation_date:
        age = datetime.now() - creation_date
        return f"{age.days // 365} Years, {age.days % 365} Days"
    return "N/A"

# Display detailed domain information
def display_info(domain_info, domain_name, verbose=False):
    output = {
        "domain": domain_name,
        "registrant_name": domain_info.name,
        "registrant_organization": domain_info.org,
        "registrar": domain_info.registrar,
        "creation_date": format_dates(domain_info.creation_date),
        "expiration_date": format_dates(domain_info.expiration_date),
        "updated_date": format_dates(domain_info.updated_date),
        "dnssec": domain_info.dnssec,
        "emails": domain_info.emails,
        "name_servers": sorted(set([ns.lower() for ns in domain_info.name_servers])),
        "ip_address": None,
        "reverse_ip": None,
        "geolocation": None,
        "domain_age": None,
    }

    try:
        ip_address = socket.gethostbyname(validate_domain(domain_name))
        output["ip_address"] = ip_address
        output["reverse_ip"] = get_reverse_ip(ip_address)
        output["geolocation"] = get_geolocation(ip_address)
        output["domain_age"] = calculate_domain_age(domain_info.creation_date)
    except Exception as e:
        output["error"] = f"Error retrieving IP or geolocation: {e}"

    return output

# Check if the domain is available for registration
def is_domain_available(domain):
    try:
        whois_result = whois.whois(domain)
        return not whois_result.domain_name
    except:
        return True

# Process a list of domains and compile information
def process_domains(domains, verbose=False):
    results = []
    for domain in domains:
        try:
            print(f"Processing domain: {domain}")  # Debugging
            domain_info = whois.whois(domain)
            print(f"WHOIS data for {domain}: {domain_info}")  # Debugging

            if not domain_info.status or "No match for domain" in str(domain_info.status):
                availability = not domain_info.domain_name
                results.append({
                    "domain": domain,
                    "available": availability,
                })
            else:
                results.append({
                    "domain": domain,
                    "registrar": domain_info.registrar,
                    "creation_date": domain_info.creation_date,
                    "expiration_date": domain_info.expiration_date,
                    "status": domain_info.status,
                })
        except Exception as e:
            print(f"Error processing domain {domain}: {e}")  # Debugging
            results.append({
                "domain": domain,
                "error": str(e),
            })
    return results

@app.route('/check_domains', methods=['POST'])
def check_domains():
    domains = []

    # Handle file upload
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.txt'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                domains.extend([line.strip() for line in f if line.strip()])
        elif file.filename.endswith('.csv'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                import csv
                reader = csv.reader(f)
                for row in reader:
                    domains.extend(row)

    # Remove duplicates and validate domains
    domains = list(set(filter(None, map(validate_domain, domains))))

    verbose = request.form.get('verbose', 'false').lower() == 'true'
    results = process_domains(domains, verbose)
    return jsonify(results)

@app.route('/templates/<path:filename>')
def serve_php(filename):
    # Serve PHP files from the templates folder
    return send_from_directory('templates', filename)

# Stream results in real time
@app.route('/stream_results')
def stream_results():
    def generate():
        output_file = 'output/output.txt'
        last_position = 0

        while True:
            try:
                with open(output_file, 'r') as file:
                    file.seek(last_position)
                    new_lines = file.readlines()
                    last_position = file.tell()

                    for line in new_lines:
                        yield f"data: {line.strip()}\n\n"

                        # Stop streaming if "END_OF_RESULTS" is encountered
                        if "END_OF_RESULTS" in line:
                            return

                time.sleep(1)  # Wait for 1 second before checking for new lines
            except FileNotFoundError:
                yield "data: Waiting for results...\n\n"
                time.sleep(1)

    return Response(generate(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)