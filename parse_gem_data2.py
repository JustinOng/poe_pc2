from bs4 import BeautifulSoup
import json

def present_td(input):
    quests = input.text.encode("ascii").strip().split("\n")
    final = []
    for quest in quests:
        quest = quest.split(" - ")
        location = quest[0]
        
        name = quest[1].split(" ")
        final_part_name = name[-1]
        name = name[0:-1]
        out = ""
        for i in name:
            out += i[0].upper()
        
        out += final_part_name
        final.append(location+" - "+out)
    
    return ", ".join(final)

with open("gem_data.html") as f:
    soup = BeautifulSoup(f.read())

tr = soup.findAll("tr")

data = {}

for row in tr:
    reward_by_class = row.findAll("td")
    
    #skips over the header rows
    if not reward_by_class:
        continue
    
    #compress down the quest details into a single string
    #well maybe not quest_giver, but rather the vendor that sells the gems
    quest_links = row.find("th").findAll("a")
    quest_name = quest_links[0].text    
    quest_giver = quest_links[1].text
    quest_act = row.find("th").text.replace(quest_name, "").replace(quest_giver, "")
    
    quest_act = "A"+quest_act[-1]
    
    quest_string = "{0}({1}) after {2}".format(quest_giver, quest_act, quest_name)
    #print quest_string
    
    for i in range(len(reward_by_class)):
      gems = reward_by_class[i].findAll("a")
      
      for gem in gems:
        gem_name = gem.get("title")
        
        if gem_name not in data:
          data[gem_name] = [None] * 7
        
        data[gem_name][i] = (quest_string)

print json.dumps(data)