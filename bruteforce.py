from bit import Key
from multiprocessing import cpu_count, Process
from requests import get
from time import time, sleep
import os
import threading

# Function to read addresses from files in a directory
def read_addresses_from_directory(directory):
    wallets = set()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                addresses = file.read().split('\n')
                wallets.update(addresses)
    if '' in wallets:
        wallets.remove('')
    return wallets

# Define the input and output directories
input_directory = 'database/latest'
output_file = 'found.txt'

# Read addresses from the input directory
wallets = read_addresses_from_directory(input_directory)

max_p = 115792089237316195423570985008687907852837564279074904382605163141518161494336

# Lock for thread safety when updating hashrate and addresses generated
hashrate_lock = threading.Lock()
addresses_generated_lock = threading.Lock()

# Initialize variables for hashrate monitoring
hashrate = 0
addresses_generated = 0

# Randomized Brute Force function
def random_brute_force(r, sep_p):
    print(f'Instance: {r + 1} - Generating random addresses...')
    while True:
        pk = Key()
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')

        # Update addresses generated count
        with addresses_generated_lock:
            global addresses_generated
            addresses_generated += 1

# Function to calculate hashrate
def calculate_hashrate():
    global hashrate, addresses_generated
    while True:
        sleep(10)  # Calculate hashrate every 10 seconds
        with hashrate_lock:
            hashrate = addresses_generated / 10  # Calculate hashrate as addresses per second
            addresses_generated = 0

# Start the hashrate calculation thread
hashrate_thread = threading.Thread(target=calculate_hashrate)
hashrate_thread.daemon = True
hashrate_thread.start()

# Traditional Brute Force function
def traditional_brute_force(r, sep_p):
    sint = sep_p * r if sep_p * r != 0 else 1
    mint = sep_p * (r + 1)
    print(f'Instance: {r + 1} - Generating addresses...')
    while sint < mint:
        pk = Key.from_int(sint)
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')
        sint += 1

# Online Brute Force function
def online_brute_force():
    print('Instance: 1 - Generating random addresses...')
    while True:
        pk = Key()
        print(f'Instance: 1 - Generated: {pk.address} wif: {pk.to_wif()}')
        print('Instance: 1 - Checking balance...')
        try:
            balance = int(get(f'https://blockchain.info/q/addressbalance/{pk.address}/').text)
        except ValueError:
            print(f'Instance: 1 - Error reading balance from: {pk.address}')
            continue
        print(f'Instance: 1 - {pk.address} has balance: {balance}')
        if balance > 0:
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')
            print(f'Instance: 1 - Added address to {output_file}')
        print('Sleeping for 10 seconds...')
        sleep(10)

# Debug version of Randomized Brute Force
def debug_random_brute_force(r, sep_p):
    print(f'Instance: {r + 1} - Generating random addresses...')
    while True:
        pk = Key()
        print(f'Instance: {r + 1} - Generated: {pk.address}')
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')

# Debug version of Traditional Brute Force
def debug_traditional_brute_force(r, sep_p):
    sint = sep_p * r if sep_p * r != 0 else 1
    mint = sep_p * (r + 1)
    print(f'Instance: {r + 1} - Generating addresses...')
    while sint < mint:
        pk = Key.from_int(sint)
        print(f'Instance: {r + 1} - Generated: {pk.address}')
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')
        sint += 1

# Debug version of Online Brute Force
def debug_online_brute_force():
    print('Instance: 1 - Generating random addresses...')
    while True:
        pk = Key()
        print(f'Instance: 1 - Generated: {pk.address} wif: {pk.to_wif()}')
        print('Instance: 1 - Checking balance...')
        try:
            balance = int(get(f'https://blockchain.info/q/addressbalance/{pk.address}/').text)
        except ValueError:
            print(f'Instance: 1 - Error reading balance from: {pk.address}')
            continue
        print(f'Instance: 1 - {pk.address} has balance: {balance}')
        if balance > 0:
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')
            print(f'Instance: 1 - Added address to {output_file}')
        print('Sleeping for 10 seconds...')
        sleep(10)

# Optimized Traditional Brute Force function with hashrate monitoring
def optimized_traditional_brute_force_with_hashrate(r, sep_p, time_interval=10):
    start_time = time()
    addresses_generated = 0

    sint = (sep_p * r) + 10 ** 75 if r == 0 else (sep_p * r)
    mint = (sep_p * (r + 1))
    print(f'Instance: {r + 1} - Generating addresses...')
    while sint < mint:
        pk = Key.from_int(sint)
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')
        sint += 1

        addresses_generated += 1

        # Calculate hashrate
        elapsed_time = time() - start_time
        if elapsed_time >= time_interval:
            with hashrate_lock:
                hashrate = addresses_generated / elapsed_time
                print(f'Instance: {r + 1} - Hashrate: {hashrate:.2f} addresses per second')

                # Reset counters
                start_time = time()
                addresses_generated = 0

# Debug version of Optimized Traditional Brute Force
def debug_optimized_traditional_brute_force(r, sep_p, time_interval=10):
    start_time = time()
    addresses_generated = 0

    sint = (sep_p * r) + 10 ** 75 if r == 0 else (sep_p * r)
    mint = (sep_p * (r + 1))
    print(f'Instance: {r + 1} - Generating addresses...')
    while sint < mint:
        pk = Key.from_int(sint)
        print(f'Instance: {r + 1} - Generated: {pk.address}')
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')
        sint += 1

        addresses_generated += 1

        # Calculate hashrate
        elapsed_time = time() - start_time
        if elapsed_time >= time_interval:
            with hashrate_lock:
                hashrate = addresses_generated / elapsed_time
                print(f'Instance: {r + 1} - Hashrate: {hashrate:.2f} addresses per second')

                # Reset counters
                start_time = time()
                addresses_generated = 0

def main():
    # Set bruteforce mode
    mode = (
        None,
        random_brute_force,
        traditional_brute_force,
        optimized_traditional_brute_force_with_hashrate,
        online_brute_force,
        debug_random_brute_force,
        debug_traditional_brute_force,
        debug_optimized_traditional_brute_force,
        debug_online_brute_force
    )

    # Print menu
    menu_string = 'Select bruteforce mode:\n'
    for count, function in enumerate(mode):
        try:
            if 'debug' in function.__name__:
                menu_string += f'{count} - {function.__name__} (Prints output)\n'
            else:
                menu_string += f'{count} - {function.__name__}\n'
        except AttributeError:
            menu_string += f'{count} - Exit\n'
    print(menu_string)

    try:
        choice = int(input('> '))
        if choice == 4:
            option = 4
            cpu_cores = 1
        elif choice != 0:
            print(f'How many cores do you want to use ({cpu_count()} available)')
            cpu_cores = int(input('> '))
            cpu_cores = cpu_cores if 0 < cpu_cores < cpu_count() else cpu_count()
            option = choice if 0 < choice <= len(mode) - 1 else 0
        else:
            option = 0
            cpu_cores = 0
    except ValueError:
        option = 0
        cpu_cores = 0

    if mode[option] and mode[option].__name__ != 'online_brute_force':
        time_interval = 10  # Set your desired time interval for hashrate monitoring (in seconds)
        print(f'Starting bruteforce instances in mode: {mode[option].__name__} with {cpu_cores} core(s)\n')

        instances = []
        for i in range(cpu_cores):
            instance = Process(target=mode[option], args=(i, round(max_p / cpu_cores), time_interval))
            instances.append(instance)
            instance.start()

        for instance in instances:
            instance.join()

    elif mode[option].__name__ == 'online_brute_force':
        print(f'Starting bruteforce in mode: {mode[option].__name__} (6 per minute to respect API rate limit)\n')
        online_brute_force()

    print('Stopping...')

if __name__ == '__main__':
    main()
