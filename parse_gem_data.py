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
    
    gem_name = row.find("th").find("a").text
    
    if len(reward_by_class) < 7:
        if len(reward_by_class) == 1:
            info = present_td(reward_by_class[0].find("p"))
            
            data[gem_name] = [info]*7
        else:
            print gem_name +" has broken up <td>s! Must be added manually."
        
        continue
    
    data[gem_name] = []
    
    for td in reward_by_class:
        info = td.find("p")
        
        info = present_td(info) if info else False
        
        data[gem_name].append(info)

print json.dumps(data)