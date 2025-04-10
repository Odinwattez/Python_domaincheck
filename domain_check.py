import os
import sys
import socket
import ssl
from datetime import datetime
import requests
import whois
import certifi

def safe_open_write(path, default_path='/default/path'):
    """ Safely open a file for writing, avoiding path traversal vulnerabilities. """
    if os.path.commonpath([os.path.abspath(path), default_path]) != default_path:
        raise ValueError("Unauthorized file path")
    return open(path, 'w')

def validate_domain(domain):
    """ Validate the domain to ensure it does not contain any unexpected characters that could lead to SSRF. """
    import re
    if not re.match(r"^[a-zA-Z0-9-\.]+$", domain):
        raise ValueError("Invalid domain name")
    return domain

def format_dates(dates):
    """ Format date objects for output. """
    if isinstance(dates, list):
        return dates[0].strftime('%m-%d-%Y %H:%M:%S UTC')
    elif dates:
        return dates.strftime('%m-%d-%Y %H:%M:%S UTC')
    else:
        return "N/A"

def get_reverse_ip(ip_address):
    """ Get the reverse DNS record for an IP address. """
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return "No reverse DNS record found"
    except Exception as e:
        return f"Error retrieving hostname - {e}"

def get_geolocation(ip_address):
    """ Fetch geolocation information for an IP address. """
    try:
        response = requests.get(f"http://ip-api.com/json/{validate_domain(ip_address)}")
        data = response.json()
        return f"Country: {data['country']}, City: {data['city']}, ISP: {data['isp']}"
    except Exception as e:
        return "Error retrieving geolocation"

def get_ssl_info(domain_name):
    """ Retrieve SSL certificate information for a domain using specified CA bundle. """
    try:
        # Create a default SSL context with higher security settings
        context = ssl.create_default_context()
        # Load CA certificates from certifi
        context.load_verify_locations(certifi.where())

        # Create a secure socket connection
        with socket.create_connection((domain_name, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain_name) as ssock:
                cert = ssock.getpeercert()  # Retrieve the peer's certificate
                if 'notBefore' in cert and 'notAfter' in cert:
                    # Parse and format the validity dates
                    valid_from = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z').strftime('%m-%d-%Y %H:%M:%S UTC')
                    valid_until = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z').strftime('%m-%d-%Y %H:%M:%S UTC')
                    return f"SSL Valid from: {valid_from}, until: {valid_until}"
                else:
                    return "SSL Information: Validity dates not available"
    except ssl.CertificateError as e:
        return f"SSL Information: Error - {e}"
    except Exception as e:
        return f"SSL Information: Error - {e}"

def get_http_headers(domain_name):
    """ Fetch HTTP headers for a domain. """
    try:
        response = requests.get(f"http://{validate_domain(domain_name)}", timeout=10)
        headers = response.headers
        key_headers = ['Server', 'Content-Type', 'Last-Modified']
        header_info = "\n".join([f"  - {header}: {headers.get(header, 'Not Available')}" for header in key_headers])
        return header_info
    except requests.ConnectionError:
        return "Could not establish a connection"
    except requests.Timeout:
        return "Connection timed out"
    except Exception as e:
        return f"Error: {e}"

def calculate_domain_age(creation_date):
    """ Calculate the age of a domain from its creation date. """
    if isinstance(creation_date, list):
        creation_date = creation_date[0]
    if creation_date:
        age = datetime.now() - creation_date
        return f"Domain Age: {age.days // 365} Years, {age.days % 365} Days"
    return "Domain Age: N/A"

def display_info(domain_info, domain_name, verbose=False):
    """ Compile detailed domain information for display. """
    output = [f"\n{'=' * 40}\n\nDomain: {domain_name}"]

    # Additional domain info like registrant and registrar
    output.append(f"Registrant Name: {domain_info.name}")
    output.append(f"Registrant Organization: {domain_info.org}")
    output.append(f"Registrar: {domain_info.registrar}")

    # Date formatting and name servers
    output.append(f"\nCreation Date: {format_dates(domain_info.creation_date)}")
    output.append(f"Expiration Date: {format_dates(domain_info.expiration_date)}")
    output.append(f"Updated Date: {format_dates(domain_info.updated_date)}")

    nameservers = sorted(set([ns.lower() for ns in domain_info.name_servers]))
    if nameservers:
        output.append("\nName Servers:")
        for ns in nameservers:
            output.append(f"  - {ns}")

    if domain_info.dnssec:
        output.append(f"\nDNSSEC: {domain_info.dnssec}")

    if domain_info.emails:
        output.append("\nContact Emails:")
        if isinstance(domain_info.emails, list):
            output.extend([f"  - {email}" for email in domain_info.emails])
        else:
            output.append(f"  - {domain_info.emails}")

    try:
        ip_address = socket.gethostbyname(validate_domain(domain_name))
        output.append(f"\nIP Address: {ip_address}")
        output.append(f"Reverse IP: {get_reverse_ip(ip_address)}")
    except Exception as e:
        output.append(f"\nIP Address: Error retrieving IP - {e}")

    output.append(f"{calculate_domain_age(domain_info.creation_date)}")
    output.append(f"Geolocation: {get_geolocation(ip_address)}")

    http_headers = get_http_headers(domain_name)
    if http_headers.startswith("Error") or http_headers.startswith("Could not") or http_headers.startswith("Connection timed"):
        output.append(f"\nHTTP Header Information: {http_headers}")
    else:
        output.append("\nHTTP Header Information:")
        output.append(http_headers)

    ssl_info = get_ssl_info(domain_name)
    if "SSL Valid:" in ssl_info:
        output.append("\n" + ssl_info)
    else:
        output.append("\nSSL Information: " + ssl_info)

    if verbose:
        output.append("\n[Verbose Mode]")
        output.append(f"  Domain Status: {domain_info.status}")
        output.append(f"  Whois Server: {domain_info.whois_server}")

    return "\n".join(output)

def is_domain_available(domain):
    """ Check if a domain is available for registration. """
    try:
        whois_result = whois.whois(domain)
        return not whois_result.domain_name
    except:
        return True

def process_domains(domains, verbose=False, output_file=None, limit=None):
    """Process a list of domains and compile information."""
    if limit:
        domains = domains[:limit]  # Limit the number of domains to process

    if output_file:
        with open(output_file, 'w') as file:  # Clear the file at the start
            file.write("")  # Ensure the file is empty

    for i, domain in enumerate(domains, start=1):
        print(f"Processing domain {i}/{len(domains)}: {domain}")  # Show progress
        try:
            domain_info = whois.whois(domain)
            if not domain_info.status or "No match for domain" in str(domain_info.status):
                availability = is_domain_available(domain)
                result = f"Domain '{domain}' is {'available' if availability else 'not available'} for registration."
            else:
                result = display_info(domain_info, domain, verbose)
        except Exception as e:
            result = f"An error occurred while processing '{domain}': {e}"

        print(result)  # Print the result immediately

        # Write to the output file incrementally
        if output_file:
            with open(output_file, 'a') as file:
                file.write(result + "\n")

    # Append "END_OF_RESULTS" to signal the end of processing
    if output_file:
        with open(output_file, 'a') as file:
            file.write("END_OF_RESULTS\n")

# Read domain names from a text file
def read_domains_from_file(file_path):
    """ Read domain names from a text file. """
    try:
        with open(file_path, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
            return domains
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        sys.exit(1)

# Main function to handle command-line arguments and execute the script
# This function checks for the presence of command-line arguments and processes them accordingly.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <domain/subdomain> [-v] [-o output_file] [-f input_file] [-l limit]")
        sys.exit(1)

    verbose = "-v" in sys.argv
    output_file_flag = "-o" in sys.argv
    output_file = sys.argv[sys.argv.index("-o") + 1] if output_file_flag and sys.argv.index("-o") + 1 < len(sys.argv) else None
    file_flag = "-f" in sys.argv
    input_file = sys.argv[sys.argv.index("-f") + 1] if file_flag and sys.argv.index("-f") + 1 < len(sys.argv) else None
    limit_flag = "-l" in sys.argv
    limit = int(sys.argv[sys.argv.index("-l") + 1]) if limit_flag and sys.argv.index("-l") + 1 < len(sys.argv) else None

    domain_list = []

    # Read domains from file if -f is provided
    if input_file:
        domain_list.extend(read_domains_from_file(input_file))

    # Add domains from command-line arguments
    domain_list.extend([
        arg for arg in sys.argv[1:]
        if arg not in ["-v", "-o", "-f", "-l"] and arg != output_file and arg != input_file and (not limit_flag or arg != str(limit))
    ])

    if not domain_list:
        print("Error: No domains provided.")
        sys.exit(1)

    # Apply the limit to the domain list
    if limit:
        domain_list = domain_list[:limit]

    process_domains(domain_list, verbose, output_file)
