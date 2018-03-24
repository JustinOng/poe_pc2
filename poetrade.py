import requests
import cfscrape
import logging
from datetime import date, timedelta
from bs4 import BeautifulSoup

BASE_URL = "http://poe.trade"
league = "Standard"

scraper = cfscrape.create_scraper()

def Config(**kwargs):
    global league
    
    if kwargs["league"]:
        league = kwargs["league"]

def BuildParameters(**kwargs):
    payload = {
        "league": league,
        "type": "",
        "base": "",
        "name": "",
        "dmg_min": "",
        "dmg_max": "",
        "aps_min": "",
        "aps_max": "",
        "crit_min": "",
        "crit_max": "",
        "dps_min": "",
        "dps_max": "",
        "edps_min": "",
        "edps_max": "",
        "pdps_min": "",
        "pdps_max": "",
        "armour_min": "",
        "armour_max": "",
        "evasion_min": "",
        "evasion_max": "",
        "shield_min": "",
        "shield_max": "",
        "block_min": "",
        "block_max": "",
        "sockets_min": "",
        "sockets_max": "",
        "link_min": "",
        "link_max": "",
        "sockets_r": "",
        "sockets_g": "",
        "sockets_b": "",
        "sockets_w": "",
        "linked_r": "",
        "linked_g": "",
        "linked_b": "",
        "linked_w": "",
        "rlevel_min": "",
        "rlevel_max": "",
        "rstr_min": "",
        "rstr_max": "",
        "rdex_min": "",
        "rdex_max": "",
        "rint_min": "",
        "rint_max": "",
        "impl": "",
        "impl_min": "",
        "impl_max": "",
        "mods": "",
        "modexclude": "",
        "modmin": "",
        "modmax": "",
        "mods": "",
        "modexclude": "",
        "modmin": "",
        "modmax": "",
        "q_min": "",
        "q_max": "",
        "level_min": "",
        "level_max": "",
        "mapq_min": "",
        "mapq_max": "",
        "rarity": "",
        "seller": "",
        "thread": "",
        "time": str(date.today() - timedelta(days=7)),
        "corrupted": "",
        "online": "",
        "has_buyout": "1",
        "altart": "",
        "capquality": "x",
        "buyout_min": "",
        "buyout_max": "",
        "buyout_currency": "",
        "crafted": "",
        "identified": ""
    }
    
    ARGUMENTS = ["name", "base", "q_min", "q_max", "corrupted", "identified", "online", "league", "link_min", "link_max"]
    
    for argument in ARGUMENTS:
        if argument in kwargs:
            payload[argument] = kwargs[argument]
    
    return payload

def GetPageLink(**kwargs):
    payload = BuildParameters(**kwargs)
    
    logging.debug("Querying "+BASE_URL+"/search...")
    r = scraper.post(BASE_URL+"/search", data=payload, allow_redirects=False)
    logging.debug("Response received.")
    
    soup = BeautifulSoup(r.text, "html.parser")
        
    finalLink = soup.find("a").get("href")
    
    return finalLink

def GetItemsPage(link, sorted=False):
    
    if sorted:
        payload = {
            "sort": "price_in_chaos",
            "bare": "true"
        }
    else:
        payload = {}
    
    logging.debug("Querying "+link+"...")
    r = scraper.post(link, data = payload)
    logging.debug("Response received.")
    
    return r.text