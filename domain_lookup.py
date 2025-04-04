#  -  Usage: python domain_lookup.py reddit.com google.com -o output.txt

import sys
import socket
from datetime import datetime
import requests
import whois

# Validate the domain to ensure it does not contain any unexpected characters that could lead to SSRF.
# This function checks if the domain contains only valid characters (alphanumeric, hyphen, and dot).
def validate_domain(domain):
    """ Validate the domain to ensure it does not contain any unexpected characters that could lead to SSRF. """
    import re
    if not re.match(r"^[a-zA-Z0-9-\.]+$", domain):
        print(f"Warning: Skipping invalid domain '{domain}'")
        return None
    return domain

# Format date objects for output
# This function is used to format the creation, expiration, and updated dates of the domain.
def format_dates(dates):
    """ Format date objects for output. """
    if isinstance(dates, list):
        return dates[0].strftime('%m-%d-%Y %H:%M:%S UTC')
    elif dates:
        return dates.strftime('%m-%d-%Y %H:%M:%S UTC')
    else:
        return "N/A"

# Get the reverse DNS record for an IP address
def get_reverse_ip(ip_address):
    """ Get the reverse DNS record for an IP address. """
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return "No reverse DNS record found"
    except Exception as e:
        return f"Error retrieving hostname - {e}"

# Grabs the geolocation information for the IP address
# using the ip-api.com service
def get_geolocation(ip_address):
    """ Fetch geolocation information for an IP address. """
    try:
        response = requests.get(f"http://ip-api.com/json/{validate_domain(ip_address)}", timeout=5)
        data = response.json()
        return f"Country: {data['country']}, City: {data['city']}, ISP: {data['isp']}"
    except Exception as e:
        return "Error retrieving geolocation"

# Calculate the age of the domain based on its creation date

def calculate_domain_age(creation_date):
    """ Calculate the age of a domain from its creation date. """
    if isinstance(creation_date, list):
        creation_date = creation_date[0]
    if creation_date:
        age = datetime.now() - creation_date
        return f"Domain Age: {age.days // 365} Years, {age.days % 365} Days"
    return "Domain Age: N/A"

# Display detailed domain information
# This function compiles all the information about the domain into a formatted string for output.
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

    if verbose:
        output.append("\n[Verbose Mode]")
        output.append(f"  Domain Status: {domain_info.status}")
        output.append(f"  Whois Server: {domain_info.whois_server}")

    return "\n".join(output)

# Check if the domain is available for registration
# This function uses the whois library to check if the domain is available.
# But isn't foolproof as some registrars may not return accurate results.
def is_domain_available(domain):
    """ Check if a domain is available for registration. """
    try:
        whois_result = whois.whois(domain)
        return not whois_result.domain_name
    except:
        return True

# Process a list of domains and compile information
# This function iterates through the list of domains, checks their availability, and retrieves their WHOIS information.
def process_domains(domains, verbose=False, output_file=None, limit=None):
    """ Process a list of domains and compile information. """
    if limit:
        domains = domains[:limit]  # Limit the number of domains to process

    results = []
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
        results.append(result)

    # Write all results to the output file if specified
    if output_file:
        with open(output_file, 'w') as file:
            file.write("\n".join(results))

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
