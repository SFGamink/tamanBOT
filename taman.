import requests
import time
import sys
from colorama import Fore, Style  # Menambahkan colorama untuk warna teks

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
    headers['wallet'] = wallet_address  # Mengatur wallet_address dalam headers

    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data  # Returning the entire response JSON for potential future use
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def auto_claim(wallet_address):
    url = "https://api.taman.fun/mining"
    headers['wallet'] = wallet_address  # Mengatur wallet_address dalam headers

    try:
        while True:
            # Perform GET request to fetch mining info
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()

                # Check if there are points that can be claimed
                if 'pointCanClaimed' in data and data['pointCanClaimed'] >= 2.5:
                    points_claimed = data['pointCanClaimed']

                    # Check if secondsToFill is provided in the response
                    if 'secondsToFill' in data:
                        seconds_to_fill = data['secondsToFill']
                        print(f"Waiting for {seconds_to_fill} seconds before claiming...")

                        # Animate loading until secondsToFill reaches 0
                        while seconds_to_fill > 0:
                            sys.stdout.write('\r')
                            sys.stdout.write(f"Waiting: [{'=' * (seconds_to_fill - 1)}] {seconds_to_fill}")
                            sys.stdout.flush()
                            time.sleep(1)
                            seconds_to_fill -= 1
                        sys.stdout.write('\r')
                        sys.stdout.write(" " * 50)
                        sys.stdout.write('\r')

                    # Perform claim operation here (if there's an API endpoint for claiming)
                    claim_response = requests.post("https://api.taman.fun/claim", headers=headers)

                    if claim_response.status_code == 200:
                        return Fore.GREEN + f"Successfully claimed {points_claimed} points."
                    else:
                        print(f"Failed to claim points. Status code: {claim_response.status_code}")

                else:
                    print(Fore.RED + f"No points to claim at this time.")

            else:
                print(f"Failed to fetch mining information. Status code: {response.status_code}")

            time.sleep(10)  # Tunggu 10 detik sebelum memeriksa lagi

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def read_wallet_address(file_path):
    try:
        with open(file_path, 'r') as file:
            wallet_address = file.read().strip()
        return wallet_address
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

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
    wallet_address = read_wallet_address(wallet_file)

    if wallet_address:
        # Menampilkan pesan selamat datang
        print_welcome_message()

        # Lakukan pengambilan info mining terlebih dahulu
        user_info_result = user_info(wallet_address)

        if user_info_result:
            data = user_info_result['data']
            point = data['point']
            last_mining = data['lastMining']

            print(Fore.CYAN + f"\n================ Detail Mining ================\n")
            print(Fore.LIGHTYELLOW_EX + f"Point        : {point}")
            print(Fore.LIGHTYELLOW_EX + f"Last Mining  : {last_mining}")
            print(Fore.CYAN + f"\n=============== Auto Claim Mining ===============\n")

        else:
            print("Failed to fetch mining information.")

        # Mulai auto_claim di background setelah menampilkan info mining
        auto_claim_result = auto_claim(wallet_address)

        if auto_claim_result:
            print(auto_claim_result)

        print("\nProgram selesai.")

if __name__ == "__main__":
    main()
