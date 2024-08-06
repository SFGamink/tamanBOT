import requests
import time
import signal
import sys
from colorama import Fore, Style

# Global headers definition
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

# Signal handler to catch interrupt signals
def signal_handler(sig, frame):
    raise KeyboardInterrupt

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

def mining(wallet_address, delay=60):
    url = "https://api.taman.fun/mining"
    headers['wallet'] = wallet_address

    while True:
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # Raises error for bad responses (4xx or 5xx)
            
            # Parse JSON response
            data = response.json()
            
            # Check if the claim was successful
            if data.get('success'):
                print(Fore.GREEN + "Claim berhasil!")
                return data
            else:
                # Check specific message to determine if it is a wait message
                if 'message' in data and data['message'] == 'You must wait 1 hour to claim point':
                    print(Fore.RED + "Claim gagal: You must wait 1 hour to claim point")
                else:
                    print(Fore.RED + "Claim gagal")

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Error fetching URL: {e}")

        # Countdown animation
        for remaining in range(delay, 0, -1):
            sys.stdout.write(f"\rRetrying in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        # Clear the line after countdown
        sys.stdout.write("\r" + " " * 30 + "\r")  # Clear the line
        sys.stdout.flush()  # Ensure the line is cleared
        print()  # Move to the next line
        return None

def user_info(wallet_address):
    url = "https://api.taman.fun/mining"
    headers['wallet'] = wallet_address

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch user info. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_task(wallet_address):
    url = "https://api.taman.fun/quests"
    headers['wallet'] = wallet_address

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        data = response.json()  # Convert JSON response to Python dictionary/list
        
        quest_ids = []  # List to store quest_ids for later use
        
        if 'data' in data:
            for quest_type in ['main', 'partner']:
                if quest_type in data['data']:
                    quests = data['data'][quest_type]
                    for quest in quests:
                        quest_id = quest['id']
                        quest_name = quest['name']
                        quest_status = quest['status']
                        quest_ids.append(quest_id)  # Collect quest_id
        
        return quest_ids
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error fetching data: {e}")
        return None

def clear_task(wallet_address, quest_id):
    url = "https://api.taman.fun/return-quest"
    headers['wallet'] = wallet_address
    body = {
        "questId": quest_id
    }
    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise exception for bad status codes
        result = response.json()
        
        if 'message' in result:
            if result['message'] == "User hasn't taken this quest yet":
                print(Fore.YELLOW + f"Anda sudah mengerjakan quest ini.")
            elif result['message'] == "Quest not done yet":
                print(Fore.RED + f"Clear Task Gagal")
            else:
                print(Fore.RED + f"Unexpected response: {result}")
        else:
            print(Fore.GREEN + f"Sukses mengerjakan quest.")
        
        return result
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error clearing task: {e}")
        return None

def read_wallet_addresses(file_path):
    wallet_addresses = []
    try:
        with open(file_path, 'r') as file:
            # Read all lines from the file and strip whitespace
            wallet_addresses = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return wallet_addresses

def print_welcome_message():
    print(r"""      
▒█▀▀▀█ █▀▀█ ░█▀█░ ▒█▄░▒█ 
░▀▀▀▄▄ ░░▀▄ █▄▄█▄ ▒█▒█▒█ 
▒█▄▄▄█ █▄▄█ ░░░█░ ▒█░░▀█
          """)
    print(Fore.GREEN + Style.BRIGHT + "Taman-Heroes Kombat BOT")
    print(Fore.RED + Style.BRIGHT + "Jangan di edit la bang :)\n\n")

def main():
    wallet_file = 'wallet.txt'
    wallet_addresses = read_wallet_addresses(wallet_file)

    if wallet_addresses:
        print_welcome_message()

        for index, wallet_address in enumerate(wallet_addresses, start=1):
            # Handle quests for the current wallet address before processing mining
            quest_ids = get_task(wallet_address)
            
            if quest_ids:
                # Ask for confirmation before clearing all tasks
                confirmation = input(Fore.WHITE + f"Apakah Anda yakin ingin menghapus semua quest ? (y/n): ")
                if confirmation.lower() == 'y':
                    print(Fore.CYAN + f"Menghapus semua quest...")
                    for quest_id in quest_ids:
                        response = clear_task(wallet_address, quest_id)

            user_info_result = user_info(wallet_address)

            if user_info_result:
                data = user_info_result['data']
                point = data['point']
                last_mining = data['lastMining']

                # Use Akun 1, Akun 2, etc. based on index
                akun_label = f"Akun {index}"

                print(Fore.CYAN + f"\n================= ({akun_label}) =================\n")
                print(Fore.LIGHTYELLOW_EX + f"Point        : {point}")
                print(Fore.LIGHTYELLOW_EX + f"Last Mining  : {last_mining}")
                print(Fore.CYAN + f"\n============== Auto Claim Mining ==============\n")

                try:
                    mining(wallet_address)  # Call mining function which will loop indefinitely
                except KeyboardInterrupt:
                    print(Fore.YELLOW + f"{akun_label} selesai. Pindah ke akun selanjutnya...")

if __name__ == "__main__":
    main()
