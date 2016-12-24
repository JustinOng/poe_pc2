# -*- coding: UTF-8 -*-
"""var e = document.querySelector(".wikitable").querySelectorAll("tr");

var data = [];
for(var i in e) {
  var row = e[i];
  if (typeof(row) != "object") continue;
  var tds = row.querySelectorAll("td");
  if (tds.length > 0) {
    var tmp = {};
    for(var j in tds) {
      if (j == 0) {
        tmp["name"] = tds[j].querySelector("a").innerText;
      }
      else if (j == 1) {
        tmp["level"] = tds[j].innerText;
      }
      else if (j == 2) {
        tmp["tier"] = tds[j].innerText;
      }
      else if (j == 4) {
        tmp["boss_difficulty"] = tds[j].innerText;
      }
      else if (j == 5) {
        tmp["layout"] = tds[j].innerText;
      }
      else if (j == 6) {
        if (tds[j].querySelector("a")) {
          tmp["boss"] = tds[j].querySelector("a").innerText;
        }
        else {
          tmp["boss"] = tds[j].innerText;
        }
      }
    }
    
    data.push(tmp);
  }
}

copy(JSON.stringify(data));"""

from fuzzywuzzy import fuzz

map_data = [{"name":"Crypt Map","level":"68","tier":"1","boss_difficulty":"2","layout":"Crypt","boss":"Pagan Bishop of Agony"},{"name":"The Coward's Trial","level":"68","tier":"1","boss_difficulty":"2","layout":"Crypt","boss":"Infector of Dreams"},{"name":"Desert Map","level":"68","tier":"1","boss_difficulty":"5","layout":"Dried Lake","boss":"Mirage of Bones"},{"name":"Dunes Map","level":"68","tier":"1","boss_difficulty":"3","layout":"The Coast","boss":"The Blacksmith"},{"name":"Dungeon Map","level":"68","tier":"1","boss_difficulty":"4","layout":"Prison","boss":"Penitentiary Incarcerator"},{"name":"Grotto Map","level":"68","tier":"1","boss_difficulty":"1","layout":"Caverns","boss":"Fire and Fury"},{"name":"Pit Map","level":"68","tier":"1","boss_difficulty":"2","layout":"Daresso's Dream","boss":"Tore, Towering Ancient"},{"name":"Tropical Island Map","level":"68","tier":"1","boss_difficulty":"2","layout":"The Southern Forest","boss":"Blood Progenitor"},{"name":"Untainted Paradise","level":"68","tier":"N/A","boss_difficulty":"2","layout":"The Southern Forest","boss":"Clutch Queen"},{"name":"Arcade Map","level":"69","tier":"2","boss_difficulty":"1","layout":"Sarn","boss":"Herald of Thunder"},{"name":"Cemetery Map","level":"69","tier":"2","boss_difficulty":"1","layout":"Fellshrine Ruins","boss":"Thunderskull"},{"name":"Channel Map","level":"69","tier":"2","boss_difficulty":"4","layout":"The Aqueduct","boss":"The Winged Death"},{"name":"Mountain Ledge Map","level":"69","tier":"2","boss_difficulty":"2","layout":"The Ledge","boss":"Champion of Frost"},{"name":"Maelström of Chaos","level":"69","tier":"2","boss_difficulty":"3","layout":"The Ledge","boss":"Merveil, the Reflection"},{"name":"Sewer Map","level":"69","tier":"2","boss_difficulty":"2","layout":"Sewers","boss":"Belcer, the Pirate Lord"},{"name":"Thicket Map","level":"69","tier":"2","boss_difficulty":"3","layout":"Dread Thicket","boss":"Steelpoint the Avenger"},{"name":"Wharf Map","level":"69","tier":"2","boss_difficulty":"3","layout":"Docks","boss":"Bramblemist"},{"name":"The Apex of Sacrifice","level":"70","tier":"N/A","boss_difficulty":"5","layout":"Ancient Pyramid","boss":"Atziri, Queen of the Vaal"},{"name":"Ghetto Map","level":"70","tier":"3","boss_difficulty":"3","layout":"The Slums","boss":"The Reaver"},{"name":"Mud Geyser Map","level":"70","tier":"3","boss_difficulty":"3","layout":"Fetid Pool","boss":"Skullbeak"},{"name":"Museum Map","level":"70","tier":"3","boss_difficulty":"5","layout":"Library","boss":"The Fallen Queen"},{"name":"Quarry Map","level":"70","tier":"3","boss_difficulty":"4","layout":"Mines","boss":"Void Anomaly"},{"name":"Reef Map","level":"70","tier":"3","boss_difficulty":"3","layout":"Tidal Island","boss":"Asphyxia"},{"name":"Mao Kun","level":"70","tier":"3","boss_difficulty":"4","layout":"Tidal Island","boss":"Fairgraves, Never Dying"},{"name":"Spider Lair Map","level":"70","tier":"3","boss_difficulty":"3","layout":"The Weaver's Chambers","boss":"Hybrid Widow"},{"name":"Vaal Pyramid Map","level":"70","tier":"3","boss_difficulty":"2","layout":"Ancient Pyramid","boss":"Atziri's Chosen"},{"name":"Vaults of Atziri","level":"70","tier":"3","boss_difficulty":"0","layout":"Ancient Pyramid","boss":"(none)"},{"name":"Arena Map","level":"71","tier":"4","boss_difficulty":"3","layout":"The Grand Arena","boss":"Avatar of the Forge"},{"name":"Overgrown Shrine Map","level":"71","tier":"4","boss_difficulty":"3","layout":"Chamber of Sins","boss":"Hybrid Widow"},{"name":"Acton's Nightmare","level":"71","tier":"4","boss_difficulty":"2","layout":"Chamber of Sins","boss":"Thorn"},{"name":"Promenade Map","level":"71","tier":"4","boss_difficulty":"3","layout":"The Ebony Barracks","boss":"Blackguard Avenger"},{"name":"Hall of Grandmasters","level":"71","tier":"4","boss_difficulty":"5","layout":"The Ebony Barracks","boss":"several"},{"name":"Phantasmagoria Map","level":"71","tier":"4","boss_difficulty":"3","layout":"Belly of the Beast","boss":"Thraxia"},{"name":"Shore Map","level":"71","tier":"4","boss_difficulty":"3","layout":"The Coast","boss":"Glace"},{"name":"Spider Forest Map","level":"71","tier":"4","boss_difficulty":"3","layout":"The Blackwood","boss":"The Blacksmith"},{"name":"Tunnel Map","level":"71","tier":"4","boss_difficulty":"1","layout":"Submerged Passage","boss":"Lady of the Brood"},{"name":"Bog Map","level":"72","tier":"5","boss_difficulty":"1","layout":"Fetid Pool","boss":"Slitherskin"},{"name":"Caer Blaidd, Wolfpack's Den","level":"72","tier":"5","boss_difficulty":"3","layout":"The Den","boss":"Solus, Pack Alpha"},{"name":"Coves Map","level":"72","tier":"5","boss_difficulty":"1","layout":"The Coves","boss":"Master of the Blade"},{"name":"Graveyard Map","level":"72","tier":"5","boss_difficulty":"4","layout":"Fellshrine Ruins","boss":"Merveil, the Reflection"},{"name":"Pier Map","level":"72","tier":"5","boss_difficulty":"1","layout":"The Docks","boss":"Flame of Truth"},{"name":"Underground Sea Map","level":"72","tier":"5","boss_difficulty":"1","layout":"The Den","boss":"The Idol Beyond"},{"name":"Villa Map","level":"72","tier":"5","boss_difficulty":"3","layout":"The Sceptre of God","boss":"Excellis Aurafix"},{"name":"Arachnid Nest Map","level":"73","tier":"6","boss_difficulty":"3","layout":"The Weaver's Chambers","boss":"Lord of the Bow"},{"name":"Catacomb Map","level":"73","tier":"6","boss_difficulty":"2","layout":"The Catacombs","boss":"Xixic"},{"name":"Olmec's Sanctum","level":"73","tier":"6","boss_difficulty":"4","layout":"The Catacombs","boss":"Olmec, the All Stone"},{"name":"Colonnade Map","level":"73","tier":"6","boss_difficulty":"4","layout":"Battlefront","boss":"Carnage"},{"name":"Dry Woods Map","level":"73","tier":"6","boss_difficulty":"2","layout":"The Old Fields","boss":"Spirit of Nadia"},{"name":"Strand Map","level":"73","tier":"6","boss_difficulty":"3","layout":"Twilight Strand","boss":"Massier"},{"name":"Whakawairua Tuahu","level":"73","tier":"6","boss_difficulty":"5","layout":"Twilight Strand","boss":"Tormented Temptress"},{"name":"Temple Map","level":"73","tier":"6","boss_difficulty":"4","layout":"Solaris","boss":"The Wicked One"},{"name":"Poorjoy's Asylum","level":"73","tier":"6","boss_difficulty":"5","layout":"Solaris","boss":"Mistress Hyseria"},{"name":"Jungle Valley Map","level":"74","tier":"7","boss_difficulty":"5","layout":"The Riverways","boss":"Spinner of False Hope"},{"name":"Terrace Map","level":"74","tier":"7","boss_difficulty":"4","layout":"The Hedge Maze","boss":"Sallazzang"},{"name":"Abandoned Cavern Map","level":"74","tier":"7","boss_difficulty":"3","layout":"Cavern of Wrath","boss":"The Eroding One"},{"name":"Oba's Cursed Trove","level":"74","tier":"7","boss_difficulty":"1","layout":"Mixed (Act 1, Act 2)","boss":"(none)"},{"name":"Torture Chamber Map","level":"74","tier":"7","boss_difficulty":"4","layout":"Prison","boss":"Shock and Horror"},{"name":"Waste Pool Map","level":"74","tier":"7","boss_difficulty":"3","layout":"Sewers","boss":"Asphyxia"},{"name":"Canyon Map","level":"75","tier":"8","boss_difficulty":"3","layout":"The Climb","boss":"Lord of the Bow"},{"name":"Cells Map","level":"75","tier":"8","boss_difficulty":"3","layout":"Crematorium","boss":"Harbinger"},{"name":"Dark Forest Map","level":"75","tier":"8","boss_difficulty":"2","layout":"Western Forest","boss":"Oak the Mighty"},{"name":"Dry Peninsula Map","level":"75","tier":"8","boss_difficulty":"2","layout":"The Southern Forest","boss":"Titan of the Grove"},{"name":"Orchard Map","level":"75","tier":"8","boss_difficulty":"5","layout":"The Imperial Gardens","boss":"Tunneltrap"},{"name":"Arid Lake Map","level":"76","tier":"9","boss_difficulty":"2","layout":"Fetid Pool","boss":"Drought Maddened Rhoa"},{"name":"Gorge Map","level":"76","tier":"9","boss_difficulty":"1","layout":"The Climb","boss":"Master of the Blade"},{"name":"Malformation Map","level":"76","tier":"9","boss_difficulty":"4","layout":"The Belly of the Beast","boss":"Nightmare Manifest"},{"name":"Residence Map","level":"76","tier":"9","boss_difficulty":"5","layout":"The Sceptre of God","boss":"The High Templar"},{"name":"Underground River Map","level":"76","tier":"9","boss_difficulty":"1","layout":"Cavern of Wrath","boss":"Beast of the Pits"},{"name":"Chateau Map","level":"77","tier":"10","boss_difficulty":"","layout":"Labyrinth","boss":"Hephaeus, The Hammer"},{"name":"Bazaar Map","level":"77","tier":"10","boss_difficulty":"3","layout":"Marketplace","boss":"Dialla's Wrath"},{"name":"Necropolis Map","level":"77","tier":"10","boss_difficulty":"4","layout":"Church Dungeon","boss":"Merveil, the Reflection"},{"name":"Death and Taxes","level":"77","tier":"10","boss_difficulty":"5","layout":"Church Dungeon","boss":"Avatar of Ash"},{"name":"Plateau Map","level":"77","tier":"10","boss_difficulty":"2","layout":"The Ledge","boss":"Drought Maddened Rhoa"},{"name":"Volcano Map","level":"77","tier":"10","boss_difficulty":"4","layout":"Kaom's Path","boss":"Forest of Flames"},{"name":"Academy Map","level":"78","tier":"11","boss_difficulty":"4","layout":"The Library","boss":"The Arbiter of Knowledge"},{"name":"Crematorium Map","level":"78","tier":"11","boss_difficulty":"4","layout":"Prison-like","boss":"Megaera"},{"name":"Precinct Map","level":"78","tier":"11","boss_difficulty":"3","layout":"The Slums","boss":"Lady Stormflay"},{"name":"Springs Map","level":"78","tier":"11","boss_difficulty":"3","layout":"Forest","boss":"Witch of the Cauldron"},{"name":"Arsenal Map","level":"79","tier":"12","boss_difficulty":"1","layout":"The Warehouse District","boss":"Volcanus"},{"name":"Overgrown Ruin Map","level":"79","tier":"12","boss_difficulty":"3","layout":"Chamber of Sins","boss":"Loathe"},{"name":"Shipyard Map","level":"79","tier":"12","boss_difficulty":"2","layout":"The Docks","boss":"Warmonger"},{"name":"Village Ruin Map","level":"79","tier":"12","boss_difficulty":"5","layout":"The Old Fields","boss":"Stonebeak, Battle Fowl"},{"name":"The Alluring Abyss","level":"80","tier":"N/A","boss_difficulty":"5","layout":"Ancient Pyramid","boss":"Atziri, Queen of the Vaal"},{"name":"Courtyard Map","level":"80","tier":"13","boss_difficulty":"4","layout":"The Imperial Gardens","boss":"Oriath's Vigil"},{"name":"Excavation Map","level":"80","tier":"13","boss_difficulty":"5","layout":"The Mines","boss":"Champion of the Hollows"},{"name":"Wasteland Map","level":"80","tier":"13","boss_difficulty":"4","layout":"The Dried Lake","boss":"The Brittle Emperor"},{"name":"Waterways Map","level":"80","tier":"13","boss_difficulty":"3","layout":"The Aqueduct","boss":"Fragment of Winter"},{"name":"Conservatory Map","level":"81","tier":"14","boss_difficulty":"4","layout":"Ancient Pyramid","boss":"Shadow of the Vaal"},{"name":"Palace Map","level":"81","tier":"14","boss_difficulty":"5","layout":"The Upper Sceptre","boss":"God's Chosen"},{"name":"Shrine Map","level":"81","tier":"14","boss_difficulty":"4","layout":"Lunaris Temple","boss":"Piety the Empyrian"},{"name":"Vaal Temple Map","level":"81","tier":"14","boss_difficulty":"5","layout":"Ancient Pyramid","boss":"K'aj Q'ura"},{"name":"Abyss Map","level":"82","tier":"15","boss_difficulty":"3","layout":"Kaom's Stronghold","boss":"The Infernal King"},{"name":"Colosseum Map","level":"82","tier":"15","boss_difficulty":"5","layout":"Daresso's Dream","boss":"Ambrius, Legion Slayer"},{"name":"Core Map","level":"82","tier":"15","boss_difficulty":"5","layout":"The Black Core","boss":"Prodigy of Pain"}]

def format_map_info(map):
  return "{name}[T{tier},L{level}]: {layout} with {boss}[{boss_difficulty}]".format(**map)

def cmp(map1, map2):
  return map1["ratio"] - map2["ratio"]

def get_info(map_name):
  for map in map_data:
    if map_name.lower() == map["name"].lower():
      return format_map_info(map)
  
  results = []
  #if simple name matching didnt work, then use fuzzy matching
  for map in map_data:
    map["ratio"] = fuzz.partial_ratio(map_name.lower(), map["name"].lower())
    results.append(map)
  
  results = sorted(results, cmp=cmp)
  
  return format_map_info(results[-1])
  
  return "Map {0} not found!".format(map_name)