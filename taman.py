import requests
import time
import sys
from colorama import Fore, Style

# Definisi headers yang digunakan
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://taman.fun/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def user_info(wallet_address):
    url = "https://api.taman.fun/mining"
    headers['wallet'] = wallet_address

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def auto_claim(wallet_address):
    url = "https://api.taman.fun/mining"
    headers['wallet'] = wallet_address

    try:
        while True:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if 'pointCanClaimed' in data and data['pointCanClaimed'] >= 2.5:
                    points_claimed = data['pointCanClaimed']

                    if 'secondsToFill' in data:
                        seconds_to_fill = data['secondsToFill']
                        print(f"Waiting for {seconds_to_fill} seconds before claiming...")

                        while seconds_to_fill > 0:
                            sys.stdout.write('\r')
                            sys.stdout.write(f"Waiting: [{'=' * (seconds_to_fill - 1)}] {seconds_to_fill}")
                            sys.stdout.flush()
                            time.sleep(1)
                            seconds_to_fill -= 1
                        sys.stdout.write('\r')
                        sys.stdout.write(" " * 50)
                        sys.stdout.write('\r')

                    claim_response = requests.post("https://api.taman.fun/claim", headers=headers)

                    if claim_response.status_code == 200:
                        return Fore.GREEN + f"Successfully claimed {points_claimed} points."
                    else:
                        print(f"Failed to claim points. Status code: {claim_response.status_code}")

                else:
                    print(Fore.RED + f"No points to claim at this time.")

            else:
                print(f"Failed to fetch mining information. Status code: {response.status_code}")

            time.sleep(10)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def read_wallet_addresses(file_path):
    try:
        with open(file_path, 'r') as file:
            wallet_addresses = [line.strip() for line in file.readlines()]
        return wallet_addresses
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return []

def print_welcome_message():
    print(r"""      
▒█▀▀▀█ █▀▀█ ░█▀█░ ▒█▄░▒█ 
░▀▀▀▄▄ ░░▀▄ █▄▄█▄ ▒█▒█▒█ 
▒█▄▄▄█ █▄▄█ ░░░█░ ▒█░░▀█
          """)
    print(Fore.GREEN + Style.BRIGHT + "Taman-Heroes Kombat BOT")
    print(Fore.RED + Style.BRIGHT + "Jangan di edit la bang :)\n\n")

def main():
    wallet_file = 'wallets.txt'
    wallet_addresses = read_wallet_addresses(wallet_file)

    if wallet_addresses:
        print_welcome_message()

        for wallet_address in wallet_addresses:
            user_info_result = user_info(wallet_address)

            if user_info_result:
                data = user_info_result['data']
                point = data['point']
                last_mining = data['lastMining']

                print(Fore.CYAN + f"\n================ Detail Mining ({wallet_address}) ================\n")
                print(Fore.LIGHTYELLOW_EX + f"Point        : {point}")
                print(Fore.LIGHTYELLOW_EX + f"Last Mining  : {last_mining}")
                print(Fore.CYAN + f"\n=============== Auto Claim Mining ({wallet_address}) ===============\n")

                auto_claim_result = auto_claim(wallet_address)

                if auto_claim_result:
                    print(auto_claim_result)

            else:
                print(f"Failed to fetch mining information for wallet: {wallet_address}")

        print("\nProgram selesai.")

if __name__ == "__main__":
    main()
