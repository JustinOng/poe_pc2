#!/usr/bin/env python
# -*- coding: latin-1 -*-

import re
import os
import traceback
import time
import logging
import argparse
import shlex
import win32gui
import win32api
import win32con
import schedule
import random
from bs4 import BeautifulSoup
from collections import Counter
from NumericStringParser import NumericStringParser

import poetrade
import poegem
import poetexttoname
import poeunique
import poecadiro
import poemap

LEAGUE = "Incursion"
LEAGUE_HC = "Hardcore Legacy"
LOG_FILE = "C:\Program Files (x86)\Grinding Gear Games\Path of Exile\logs\Client.txt"

def online():
  return
  if win32gui.FindWindow(None, "Path of Exile"):
    r = requests.post("http://control.poe.xyz.is/ something removed")


previous_said = None
def display(text):
    #global g_hwnd
    g_hwnd = win32gui.FindWindow(None, "Path of Exile")
    print text
    global previous_said
    previous_said = text
    
    if not g_hwnd:
        g_hwnd = win32gui.FindWindow(None, "Path of Exile")

    if not g_hwnd:
        print "Cannot locate window with \"Path of Exile\"!"
        return
    
    win32api.PostMessage(g_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    
    for c in text:
        win32api.PostMessage(g_hwnd, win32con.WM_CHAR, ord(c), 0)
    
    win32api.PostMessage(g_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

def shortenPrice(price):
    if not price: return ""
    
    price = price.split(" ")
    numericalValue = float(price[0])
    try:
        currencyType = CURRENCY_MAP[price[1]][0 if numericalValue == 1 else 1]
    except:
        currencyType = price[1]
    
    if numericalValue == int(numericalValue):
        numericalValue = int(numericalValue)
    
    NO_SPACE_CURRENCY_TYPES = ["c"]
    
    return str(numericalValue) + ("" if currencyType in NO_SPACE_CURRENCY_TYPES else " ") +currencyType

CURRENCY_MAP = {"chromatic": ["chrome", "chromes"], "alteration": ["alt", "alts"], "jewellers": ["jew", "jews"], "alchemy": ["alch", "alches"], "chaos": ["c", "c"], "exalted": ["ex", "ex"]}

#POSSIBLE_MODULES = ["pc", "math", "gem", "talisman"]

logging.basicConfig(level=logging.DEBUG)
poetrade.Config(league=LEAGUE)

pc_parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
pc_parser.add_argument("--base", nargs="?", const=None)
pc_parser.add_argument("--corrupted", help="'any', 'yes', or 'no'", nargs="?", const="yes")
pc_parser.add_argument("--identified", help="'any', 'yes', or 'no'", nargs="?", const="yes")
pc_parser.add_argument("--all", action="store_true")
pc_parser.add_argument("--quality", nargs="?", const=None)
pc_parser.add_argument("--links", nargs="?", const=None)
pc_parser.add_argument("--hc", action="store_true")
pc_parser.add_argument("--rarity", nargs="?", const=None)
pc_parser.add_argument("name", nargs="?", default="", help="name of item")

#line_regex = re.compile("\[INFO Client [0-9]+\] ([^a-zA-Z_])?([a-zA-Z_]+): (.*)")
line_regex = re.compile("\[INFO Client [0-9]+\] (.*?): (.*)")
range_regex = re.compile("(\d*)\-(\d*)")

log_file_handler = open(LOG_FILE, "r")
#read and "dump" all the contents so readline() will only get new lines
log_file_handler.read()

nsp = NumericStringParser()

logging.info("Listening...")

g_hwnd = None

previous_line = ""

link = False

#configure online scheduler
#schedule.every(4.5).minutes.do(online)

while True:
    try:
        line = log_file_handler.readline()
        
        if line:
            line = line.strip()
            
            match = re.findall(line_regex, line)
            
            if match:                
                #findall returns a array of tuples
                match = match[0]
                
                if previous_line == str(match):
                    continue
                
                previous_line = str(match)
                
                #print match[0]+match[1]+": "+match[1]
                
                if match[0].startswith("&"):
                    simple_args = match[1].split(" ")
                    
                    #do a simple split to test for the first word being pc as shlex.split will choke on unclosed '
                    if len(simple_args) == 0:# or simple_args[0] not in POSSIBLE_MODULES:
                        continue
                    
                    if simple_args[0] == "pc" and simple_args[1] == "Rarity:":
                        long_string = " ".join(simple_args[1:])
                        
                        name = poetexttoname.Parse(long_string)
                        
                        args = ["pc", name]
                    else:
                        args = shlex.split(match[1].replace("'", "&QUOTE"))
                        
                        args = [i.replace("&QUOTE", "'") for i in args]
                    
                    if args[0] == "pc":
                        args = args[1:]
                        
                        options, unknown = pc_parser.parse_known_args(args)
                        
                        options = vars(options)
                        
                        if unknown:
                            options["name"] = options["name"] + " " + " ".join(unknown)
                        
                        #validate yes/no/any options
                        ARGUMENTS_YES_NO_ANY = ["corrupted", "identified"]
                                                
                        for argument in ARGUMENTS_YES_NO_ANY:
                            if options[argument] not in [0, None, "yes", "no", "any"]:
                                display("&Unknown parameter for --"+argument+": "+options[argument])
                                continue
                            
                            #if corrrupted not set, set to default value of non corrupted
                            if argument == "corrupted" and options["corrupted"] == None:
                                options["corrupted"] = "0"
                            elif "vaal" in options["name"].lower():
                                options["corrupted"] = "1"
                            
                            #None if flag not present, = 0 if only flag present, = yes/no/any by user
                            if options[argument] == None or options[argument] == "any":
                                options[argument] = ""
                            elif options[argument] == 0 or options[argument] == "yes":
                                options[argument] = "1"
                            elif options[argument] == "no":
                                options[argument] = "0"
                                                
                        #validate quality
                        #quality can be None when flag not present/flag not given a value
                        if options["quality"]:
                            quality_match = re.findall(range_regex, options["quality"])
                            if len(quality_match) != 1 or len(quality_match[0]) != 2:
                                display("&Unknown parameter for --quality: "+options["quality"])
                                continue
                            
                            options["q_min"] = quality_match[0][0]
                            options["q_max"] = quality_match[0][1]
                        
                        del options["quality"]
                        
                        if options["links"]:
                          print(options["links"])
                          options["link_min"] = int(options["links"])
                          options["link_max"] = int(options["links"])
                        
                        del options["links"]
                                                
                        #change None to blank
                        if options["base"] == None:
                            options["base"] = ""
                        
                        #change True/False to "x"/""
                        if options["all"]:
                            options["online"] = ""
                        else:
                            options["online"] = "x"
                        
                        #set league
                        if options["hc"]:
                            options["league"] = LEAGUE_HC
                        
                        #set unique
                        if options["rarity"] == None:
                            options["rarity"] = ""
                        
                        #base has to have each word capitalised
                        options["base"] = options["base"].title()
                        
                        print options
                        
                        link = poetrade.GetPageLink(**options)
                        
                        print link
                        page = poetrade.GetItemsPage(link, sorted=False)
                        
                        soup = BeautifulSoup(page, "html.parser");
        
                        items = soup.find_all("tbody", class_="item")
                        
                        if len(items) == 0:
                            if unknown:
                                display("&No items found! Is \""+options["name"]+"\" correct?")
                            else:
                                display("&No items found!")
                            continue
                        
                        prices = Counter()
                        lowestPrice = []
                        
                        valid_items = 0
                        i = 0
                        while valid_items < 10:
                            try:
                                if float(items[i].get("data-buyout").split(" ")[0]) != 0:
                                  lowestPrice.append(shortenPrice(items[i].get("data-buyout")))
                                  valid_items += 1
                                i += 1
                            except:
                                break
                        
                        previousPrice = ""
                        groupedLowestPrice = []
                        for price in lowestPrice:
                          if price != previousPrice:
                            groupedLowestPrice.append([price, 1])
                          else:
                            groupedLowestPrice[-1][1] += 1
                          
                          previousPrice = price
                        
                        print groupedLowestPrice
                        
                        lowestPrice = []
                        for i in groupedLowestPrice:
                          if i[1] > 1:
                            lowestPrice.append("{0} ({1})".format(i[0], i[1]))
                          else:
                            lowestPrice.append(i[0])
                        
                        lowestPrice = ", ".join(lowestPrice)
                        
                        for item in items:
                            prices[item.get("data-buyout")] += 1
                        
                        commonPrice = "Most common: "+shortenPrice(prices.most_common(1)[0][0])+ "("+str(prices.most_common(1)[0][1])+")"
                        
                        item = soup.find("a").text.strip()
                        
                        display("&"+item+("(online)" if options["online"] == "x" else "")+("(hc)" if options["hc"] else "")+" on http://poe.trade ("+str(len(items))+" item"+("s" if len(items) > 1 else "")+"): "+commonPrice+", Lowest: "+lowestPrice)
                    elif args[0] == "math":
                        time.sleep(0.5)
                        try:
                            expr = "".join(simple_args[1:])
                            logging.info("Math: " + expr)
                            display("&Evaluated to: "+ str(round(nsp.eval(expr), 2)))
                        except:
                            display("&Error!")
                    elif args[0] == "gem":
                        args = args[1:]
                        result = poegem.find(args)
                        display("&"+result)
                    elif args[0] == "talisman":
                        if len(args) != 6:
                            display("&Error: Provide 5 levels!")
                            continue
                        
                        levels = args[1:6]
                        levels = [int(i) for i in levels]
                        levels.sort()
                        
                        print levels
                        
                        average = (levels[0]*1+levels[1]*2+levels[2]*2+levels[3]*2+levels[4]*3)/10
                        display("&Talisman Level: "+str(int(average)))
                    elif args[0] == "cad":
                        name = False
                        
                        try:
                          for i in [1,2]:
                            if simple_args[i] == "Rarity:":
                              long_string = " ".join(simple_args[i:])                          
                              name = poetexttoname.Parse(long_string)
                        except IndexError:
                          pass
                        
                        try:
                          #Store
                          int(args[1])
                          if not name:
                            name = " ".join(args[2:])
                          
                          print name
                          if not poeunique.isUnique(name):
                            display("&Invalid unique!")
                            continue
                          
                          poecadiro.Store(name, args[1])
                        except ValueError:
                          #if first value is not a number, treat the rest as a item name
                          if not name:
                            name = " ".join(args[1:])
                          
                          if not poeunique.isUnique(name):
                            display("&Invalid unique!")
                            continue
                          
                          result = poecadiro.Get(name)
                          if result:
                            display("&{0}: Min: {1}, Max: {2}, Average: {3}".format(name, result[0], result[1], result[2]))
                          else:
                            display("&No info on {0}!".format(args[-1]))
                        
                    elif args[0] == "map":
                        map_name = " ".join(args[1:])
                        display(poemap.get_info(map_name))
                    elif args[0] == "repeat" or args[0] == "!r":
                        if previous_said:
                            display(previous_said)
                    elif args[0] == "random":
                        display("&"+str(random.randrange(1,10)))
                elif match[0] == "@To pc":
                    if match[1] == "me":
                        g_hwnd = win32gui.FindWindow(None, "Path of Exile")
                    elif match[1] == "open":
                        if link:
                            logging.info("Opening "+link)
                            os.startfile(link)
        else:
            time.sleep(0.01)
    except KeyboardInterrupt:
        break
    except:
        print traceback.format_exc()