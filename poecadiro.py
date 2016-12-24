
DATA_FILE = "cadiro.txt"

def Store(item, price):
  with open(DATA_FILE, "a+") as f:
    f.write("{0} {1}\n".format(price, item))

def Get(item):
  print "Looking up "+item
  prices = []
  with open(DATA_FILE, "r+") as f:
    for line in f.readlines():
      if line.split(" ", 1)[1].strip().upper() == item.strip().upper():
        prices.append(int(line.split(" ")[0]))
  
  if len(prices) == 0:
    return False
  
  sum = 0
  for price in prices:
    sum += price
  
  return (min(prices), max(prices), sum/len(prices))