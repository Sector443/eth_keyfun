import os
from eth_keys import keys
import eth_utils
import web3
from web3 import Web3, HTTPProvider
import random
import argparse
import time
import urllib3
import certifi
import json
from os import urandom
from colorama import init, Fore
init(autoreset=True)

parser = argparse.ArgumentParser(
    description='A small tool to bruteforce weak ethereum private keys and more', 
    epilog='''Created by Chirag Jariwala(CJHackerz)
    [https://github.com/cjhackerz]''')

parser.add_argument("-m", "--mode", metavar="0", type=int, default=0, help="Script mode [0: linear bruteforce, 1: range bruteforce, 2: secure keygen mode, 3: custom keygen mode]")
parser.add_argument("-b", "--check_balance", type=bool, default=False, metavar="True or False", help="Check balance on blockchain")
parser.add_argument("-c", "--chain", type=str, default="mainnet", metavar="mainnet", help="Chain: mainnet, ropsten, kovan, rinkeby. Defaults to mainnet")
parser.add_argument("--infura_key", type=str, metavar="INFURA_API_KEY", help="Infura API key, required with check balance option")
parser.add_argument("-x", "--eth_address", type=str, help="Ethereum public address [0x123abcd...]")
parser.add_argument("-pk", "--private_key", type=str, help="Custom private key to use with custom keygen mode")

args = parser.parse_args()

http =  urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

class brute_keys:
    pk_null_str = '0000000000000000000000000000000000000000000000000000000000000000'
    tmp_address = str()

    def chk_balance(self, eth_add):
        if args.infura_key == None:
            print(Fore.RED + "Error: Please specify infura api key with --infura_key")
        else:
            w3 = Web3(HTTPProvider('https://' + args.chain + '.infura.io/v3/' + args.infura_key))
            balance = eth_utils.from_wei(int(w3.eth.getBalance(eth_add)), 'ether')
            if float(balance) == 0:
                print(Fore.YELLOW + "Balance[{}]: ".format(args.chain) + Fore.RED + str(balance) + " ETH")
            else:
                print(Fore.YELLOW + "Balance [{}]: ".format(args.chain) + Fore.GREEN + str(balance) + " ETH")
    
    def linear_brute(self, y):
        print(Fore.RED + 'Running linear brute force mode...')
        print(Fore.YELLOW + "Address: " + Fore.WHITE + y + "\n")
        s_time = time.time()
        for i in range(0, 2**256 + 1):
            n_hex = eth_utils.to_hex(i)
            pk_str = self.pk_null_str[len(n_hex[2:]):] + n_hex[2:]
            key = Web3.toBytes(hexstr=pk_str)
            pk = keys.PrivateKey(key)
            pbk = keys.private_key_to_public_key(pk)
            pbk_hash = Web3.sha3(hexstr=str(pbk))
            address = Web3.toHex(pbk_hash[-20:])
            chksum = Web3.toChecksumAddress(address)
            if y == chksum:
                e_time = time.time()
                t_time = e_time - s_time
                print(Fore.GREEN + "Found successfully! execution time: " + str(t_time) + " seconds")
                print(Fore.YELLOW + "Private key: " + Fore.WHITE + "0x" + pk_str)
                print(Fore.YELLOW + "Public key: " + Fore.WHITE + str(pbk))
                break
    
    def range_brute(self, y):
        _range_ = input(Fore.GREEN + "Please enter numeric range [1-100]: ").split("-")
        print(Fore.RED + 'Running numeric range brute force mode...')
        print(Fore.YELLOW + "Address: " + Fore.WHITE + y + "\n")
        s_time = time.time()
        for i in range(int(_range_[0]), int(_range_[1])):
            n_hex = eth_utils.to_hex(i)
            pk_str = self.pk_null_str[len(n_hex[2:]):] + n_hex[2:]
            key = Web3.toBytes(hexstr=pk_str)
            pk = keys.PrivateKey(key)
            pbk = keys.private_key_to_public_key(pk)
            pbk_hash = Web3.sha3(hexstr=str(pbk))
            address = Web3.toHex(pbk_hash[-20:])
            chksum = Web3.toChecksumAddress(address)
            if y == chksum:
                e_time = time.time()
                t_time = e_time - s_time
                print(Fore.GREEN + "Found successfully! execution time: " + str(t_time) + " seconds")
                print(Fore.YELLOW + "Private key: " + Fore.WHITE + "0x" + pk_str)
                print(Fore.YELLOW + "Public key: " + Fore.WHITE + str(pbk))
                break
        print(Fore.YELLOW + "Sorry, your private key was not found in given numaric range...")

    def gen_key(self):
        print(Fore.RED + "Please wait while we get quantum numbers...\n")
        r = http.request('GET', 'https://qrng.anu.edu.au/API/jsonI.php?length=256&type=hex16&size=32')
        data = json.loads(r.data.decode('utf-8'))
        random_bytes = urandom(1)
        n = int.from_bytes(random_bytes, byteorder='big')
        
        pk_str = data['data'][n]
        key = Web3.toBytes(hexstr=pk_str)
        pk = keys.PrivateKey(key)
        pbk = keys.private_key_to_public_key(pk)
        pbk_hash = Web3.sha3(hexstr=str(pbk))
        address = Web3.toHex(pbk_hash[-20:])
        chksum = Web3.toChecksumAddress(address)
        self.tmp_address = chksum
        print(Fore.YELLOW + "Private key: " + Fore.WHITE + "0x" + pk_str)
        print(Fore.YELLOW + "Public key: " + Fore.WHITE + str(pbk) + "\n")
        print(Fore.YELLOW + "Address: " + Fore.WHITE + chksum + "\n")

    def gen_key_custom(self):
            i = int(input("Enter any number between 1 - 2^256: "))
            n_hex = eth_utils.to_hex(i)
            pk_str = self.pk_null_str[len(n_hex[2:]):] + n_hex[2:]
            key = Web3.toBytes(hexstr=pk_str)
            pk = keys.PrivateKey(key)
            pbk = keys.private_key_to_public_key(pk)
            pbk_hash = Web3.sha3(hexstr=str(pbk))
            address = Web3.toHex(pbk_hash[-20:])
            chksum = Web3.toChecksumAddress(address)
            print(Fore.YELLOW + "Private key: " + Fore.WHITE + "0x" + pk_str)
            print(Fore.YELLOW + "Public key: " + Fore.WHITE + str(pbk) + "\n")
            print(Fore.YELLOW + "Address: " + Fore.WHITE + chksum + "\n")

if __name__ == '__main__':
    x = brute_keys()

    if args.mode == 0:
        if args.eth_address == None:
            print(Fore.RED + "Error: Please specify ethereum public address with -x that you want to bruteforce!")
        else:
            x.linear_brute(args.eth_address)
            if args.check_balance:
                x.chk_balance(args.eth_address)
        
    if args.mode == 1:
        if args.eth_address == None:
            print(Fore.RED + "Error: Please specify ethereum public address with -x that you want to bruteforce!")
        else:
            x.range_brute(args.eth_address)
            if args.check_balance:
                x.chk_balance(args.eth_address)

    if args.mode == 2:
        x.gen_key()
        if args.check_balance:
            x.chk_balance(x.tmp_address)

    if args.mode == 3:
        x.gen_key_custom()
        if args.check_balance:
            x.chk_balance(x.tmp_address)

#written by CJHackerz (Sector443)