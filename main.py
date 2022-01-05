#imports
import requests
import json
import discord
import subprocess
import time
import sys
from datetime import datetime, timedelta

#for later webhook use
def webhookSend(error):
  try:
    #create embed
    embed = discord.Embed(color=0xff0000, description=error+"\n\nNeed help? Click [here](https://discord.gg/5TMYSmwbTQ) for my Discord.")
    #put your webhook url below
    webhook_url = configJson["Discord_Webhook_URL"]
    #declare webhook
    webhook = discord.Webhook.from_url(webhook_url, adapter= discord.RequestsWebhookAdapter())
    #send error webhook as embed
    webhook.send(embed=embed)
  except:
    print("Exception Found: Invalid Discord Webhook URL\nPlease edit your config.json and restart.\n------------------------------")


while True:
  try:
    #open config file in read mode as var f
    with open("config.json", 'r') as f:
      #convert content of f as json (dict)
      configJson = json.loads(str(f.read()))
      f.close()

    #put your webhook url below
    webhook_url = configJson["Discord_Webhook_URL"]

    #declare webhook
    webhook = discord.Webhook.from_url(webhook_url, adapter= discord.RequestsWebhookAdapter())

    #this is your log file path
    logHostInfo = configJson["Display Host Information"]
    logWalletInfo = configJson["Display Wallet Information"]

    #get ScPrime path from json
    ScPath = configJson["ScPrime Install Path"]

    #check if log wallet
    if logWalletInfo:
      #conjoin path to command
      command = ScPath + '/spc wallet'
      #run terminal command to get wallet data
      spcWallet = subprocess.run(command, shell=True, capture_output=True)
      #convert to byte list at newlines
      byteList = spcWallet.stdout.splitlines()
      #decode bytes into py string list
      walletDictTxt=[x.decode('utf-8') for x in byteList]

      #check if log host
    if logHostInfo:
      #conjoin path to command
      command = ScPath + '/spc host -v'
      #run terminal command to get host data
      spcHost = subprocess.run(command, shell=True, capture_output=True)
      #convert to byte list at newlinse
      byteList = spcHost.stdout.splitlines()
      #decodes byt list to str list
      dictTxt = [x.decode('utf-8') for x in byteList]

    #global lists needed
    noKeys = ["Discord_Webhook_URL","ScPrime_Log_Path","Spc_Wallet_Log_Path"]
    sections = ["General Info","Host Internal Settings","Host Financials","RPC Stats","Storage Folders"]

    #declare vars
    skip = False
    webText = []

    #append a title for wallet to webtext if its not blank
    if logWalletInfo:
      webText.append("SPC WALLET")

    #loop through all keys and values of items
    for key, value in configJson.items():

      #check if section
      if key in sections:
        if value:
          skip = False
        else:
          skip = True

      #check if key is storage folders and path isnt blank
      if key == "Storage Folders" and value and logHostInfo:
        #get element that from dictTxt that starts with 'Storage Folders'
        starts = [n for n, l in enumerate(dictTxt) if l.startswith("Storage Folders:")]
        #get the index of that element in dictTxt
        folders = dictTxt[int(starts[0]):]
        #append every element in folders[] as a new element in webText[]
        for f in folders:
          webText.append(f)

      #check if true
      elif value == True and key not in noKeys:
        #check for wallet and walletLogFilePath
        if list(configJson).index(key) < 13 and logWalletInfo:
          #check if wallet status key
          if key == "Wallet status" and value == True and ":" not in key:
            #set local statusValue str var
            statusValue = ""
            #find the wallet status value
            nextValue = [i for i in walletDictTxt if ":" not in i]
            #add wallet status key + value
            statusValue = key+": " + nextValue[0]
            #append the statusValue to webText
            webText.append("    " + statusValue)
          #other config bools for wallet that are true
          elif ":" not in key and value:
            #get matching value in walletDictTxt from key
            result = [i for i in walletDictTxt if i.startswith(key)]
            #check for blank
            if result:
              #set trueValue to only the key
              trueValue = result[0]
              #append trueValue to webText
              webText.append("    " + trueValue)

        #scprime logging and check for blank log path
        elif logHostInfo:
          #check for skip
          if skip:
            #go to start of for
            continue
          #get sections tabs
          if key in sections:
            webText.append(key)
          else:
            #get matching value in dictTxt from key in pairs
            result = [i for i in dictTxt if key.strip().replace(" ","")+":" in i.replace(" ","")]
            #check for blank list
            if result:
              #set trueValue to only the key
              trueValue = result[0]
              webText.append(trueValue)

    #vars
    characterCount = 0
    Text = "**NO DATA**\nEnsure your config.json is set up correctly."
    #check if webText has data
    if webText:
      Text = ""
    #loop through elements in dictTxt list
    for element in webText:
      #add the length of each element to the total count
      characterCount += len(element)
      #check if its a section
      if element in sections or element.startswith("Storage Folders:"):
        Text = Text + "\n```\n" + element.upper() + "```"
      else:
        #split element into key:value at ':'
        newElement = element.replace("\n","").split(":",1)
        #append element to list in case of no value after ':'
        newElement.append("")
        #check for spc wallet
        if newElement[0] == "SPC WALLET":
          #format and add to Text var
          Text = Text + "\n```\n" + newElement[0] +"```"
        #all other entries
        else:
          #format and add to Text var
          Text = Text + "**" + newElement[0] + "** : " + newElement[1] +"\n"
      #exceeds 2000 char
      if characterCount > 1900:
        #send current message
        webhook.send(Text)
        #reset vars
        characterCount = 0
        Text = ""


    #check if blank
    if Text != "":
      #send webhook message
      webhook.send(Text)
    #print to console on success
    print("Webhook Message Sent Succesfully.")

  except Exception as ex:
    #get exception information
    exception_type, exception_object, exception_traceback = sys.exc_info()
    #get error and text
    error= "------------------------------\n"+str(exception_type).replace("'","").replace("<","").replace("class","").replace(">","").strip()+" Exception Occured - Check Your config.json and restart.\n>> "+str(ex)+", at line "+str(exception_traceback.tb_lineno)+"\n------------------------------"
    #print to console
    print(error)
    #try to send webhook message
    webhookSend(error[30:-30])
    #end program
    break


  #check if auto run
  if configJson["Auto Run Daily"] == True:
    try:
      #get time from config
      configTime = configJson["Time To Run in 24h Format (00:00)"].split(":",2)
      #get current time
      now = datetime.now()
      #sleep until time from config.json
      time.sleep(int((timedelta(hours=24) - (now - now.replace(hour=int(configTime[0]), minute=int(configTime[1]), second=0, microsecond=0))).total_seconds() % (24 * 3600)))
    except Exception as ex:
      #get exception information
      exception_type, exception_object, exception_traceback = sys.exc_info()
      #get error and text
      error= "------------------------------\n"+str(exception_type).replace("'","").replace("<","").replace("class","").replace(">","").strip()+" Exception Occured - Check Your Time in config.json and Restart.\n>> "+str(ex)+", at line "+str(exception_traceback.tb_lineno)+"\n------------------------------"
      #print to console
      print(error)
      #try to send as webhook message
      webhookSend(error[30:-30])
      #end program
      break
  else:
    #done, ran externally
    break
