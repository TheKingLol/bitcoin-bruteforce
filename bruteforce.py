from bit import Key
from multiprocessing import cpu_count, Process
from requests import get
from time import sleep
import os

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
input_directory = '/database/latest'
output_file = 'found.txt'

# Read addresses from the input directory
wallets = read_addresses_from_directory(input_directory)

max_p = 115792089237316195423570985008687907852837564279074904382605163141518161494336

# random bruteforce
# Will randomly generate addresses
def RBF(r, sep_p):
    print(f'Instance: {r + 1} - Generating random addresses...')
    while True:
        pk = Key()
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')

# random bruteforce output
def debug_RBF(r, sep_p):
    print(f'Instance: {r + 1} - Generating random addresses...')
    while True:
        pk = Key()
        print(f'Instance: {r + 1} - Generated: {pk.address}')
        if pk.address in wallets:
            print(f'Instance: {r + 1} - Found: {pk.address}')
            with open(output_file, 'a') as result:
                result.write(f'{pk.to_wif()}\n')

# traditional bruteforce (slowest)
# Will try every INT from 0 to max possible
def TBF(r, sep_p):
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
    print(f'Instance: {r + 1}  - Done')

# online bruteforce (randomized)
def OBF():
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

# traditional bruteforce output
def debug_TBF(r, sep_p):
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
    print(f'Instance: {r + 1}  - Done')

# optimized traditional bruteforce
# Will try every INT between 10**75 and max possibility.
# This method is based on the best practice to get the safest address possible.
def OTBF(r, sep_p):
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
    print(f'Instance: {r + 1}  - Done')

# optimized traditional bruteforce output
def debug_OTBF(r, sep_p):
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
    print(f'Instance: {r + 1}  - Done')

def main():
    # Set bruteforce mode
    mode = (None, RBF, TBF, OTBF, OBF, debug_RBF, debug_TBF, debug_OTBF)

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

    if mode[option] and mode[option].__name__ != 'OBF':
        print(f'Starting bruteforce instances in mode: {mode[option].__name__} with {cpu_cores} core(s)\n')

        instances = []
        for i in range(cpu_cores):
            instance = Process(target=mode[option], args=(i, round(max_p / cpu_cores)))
            instances.append(instance)
            instance.start()

        for instance in instances:
            instance.join()

    elif mode[option].__name__ == 'OBF':
        print(f'Starting bruteforce in mode: {mode[option].__name__} (6 per minute to respect API rate limit)\n')
        OBF()

    print('Stopping...')

if __name__ == '__main__':
    main()

