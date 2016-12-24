import argparse
import shlex
import json

CLASSES = ("Marauder", "Templar", "Witch", "Shadow", "Ranger", "Duelist", "Scion")

with open("gem_data.json") as f:
    gem_data = json.loads(f.read())

gem_parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
gem_parser.add_argument("name", nargs="?", default="", help="name of gem")
gem_parser.add_argument("class", nargs="?", default="", help="class to search")

def find(input):
    options, unknown = gem_parser.parse_known_args(input)
    options = vars(options)
    
    options["name"] = options["name"].title()
    options["class"] = options["class"].title()
    
    if not options["name"] in gem_data:
        return "{0} is not available from quests!".format(options["name"].title())
    
    result = set()
    if not options["class"]:
        for quest_info in gem_data[options["name"]]:
            if quest_info:
                for single_quest in quest_info.split(", "):
                    result.add(single_quest)
        
        return options["name"] + " is from " + ", ".join(result)
    
    else:
        i = [i for i in xrange(0, len(CLASSES)) if CLASSES[i] == options["class"]]
        
        if len(i) == 0:
            return "{0} is an invalid class!".format(options["class"])
        
        i = i[0]
        
        if gem_data[options["name"]][i]:
            return "{0} gets {1} from ".format(options["class"], options["name"]) + gem_data[options["name"]][i]
        else:
            return "{0} does not get {1}!".format(options["class"], options["name"])