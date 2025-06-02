import json, sys, hashlib
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def printtagstext():
    print("Tags:")
    print("Type")
    print("0 - Battleship")
    print("1 - Farmer/Mission Ship")
    print("2 - Storage/Factory")
    print("3 - Recreational/Miscellaneous")
    print("Specifiers, you can add these to eachother.")
    print("# - Ammo     | Target    | Type         |")
    print("0 - Flak     | Iron      | Mats         |")
    print("1 - Punch    | Explo     | Shipbuilder  |")
    print("2 - Standard | Cores     | Ammo Factory |")
    print("3 - Slug     | Flux/Rub  | Autotrader   |")
    print("4 - Sniper   | PVP Event | Scrapper     |")
    print("5 - Scatter  | Canary    | Casino       |")
    print("6 - Yank     | Pits      | RPG          |")
    print("7 - None     | Vulture   | Parkour      |")

def forceint(query):
    noerror = True
    exits = ["q", "Q", "exit", "help", "EXIT", "HELP", "esc", "ESC", "qq", "QQ", "qqq", "QQQ", "^C", "^C^C", "break", "pass", "quit"]
    while noerror:
        print(query)
        try: 
            return int(input())
        except ValueError:
            print("Invalid Input (Enter q to exit).")
            if str(input()) in exits:
                return 0

def design_info():
    li = Vividict()
    print("Design Name: ")
    li['name'] = str(input())
    print("Enter \"#UNK\" to set designer as unknown")
    print("Designer 1: ")
    li['designer 1'] = str(input())
    print("Designer 2: ")
    li['designer 2'] = str(input())
    print("Designer 3: ")
    li['designer 3'] = str(input())
    li['width'] = forceint("Width of Design? Interior Dimension in blocks.")
    li['height'] = forceint("Height of Design? Interior Dimension in blocks.")
    printtagstext()
    li['tags'] = str(forceint("Please enter the tags in the form of:\n <Type><Specifiers>"))
    return li

def specifertofull(tag):
    out = ""
    type = ["Battleship", "Farmer/Mission Ship", "Storage/Factory", "Recreational/Miscellaneous"]
    spec_ammo = ["Flak", "Punch", "Standard", "Slug", "Sniper", "Scatter", "Yank", "None"]
    spec_target = ["Iron", "Explo", "Cores", "Flux/Rub", "PVP Event", "Canary", "Pits", "Vulture"]
    spec_type = ["Mats", "Shipbuilder", "Ammo Factory", "Autotrader", "Scrapper", "Casino", "RPG", "Parkour"]
    out += type[int(tag[:1])] + " - "
    ty = tag[:1]
    if ty == "0":
        for i in range(len(tag[1:])):
             out += spec_ammo[int(tag[1:][i])] + "/"
    elif ty == "1":
        for i in range(len(tag[1:])):
             out += spec_target[int(tag[1:][i])] + "/"
    else:
        for i in range(len(tag[1:])):
             out += spec_type[int(tag[1:][i])] + "/"
    return out

def main():
    print("#############")
    print("  BP SORTER  ")
    print("#############")
    print("Create new design? (y/n)")
    new_des = input() == "y"
    if new_des:
        des_info = design_info()
        key = hashlib.sha1(str(des_info['name']).encode("UTF-8")).hexdigest()
        print("Paste in the bp below:")
        with open(str(key+".txt"), "w", encoding="latin-1") as f:
            f.write(str(input()))
        try:
            with open("designs.json", "r", encoding="utf-8") as f:
                data = Vividict(json.loads(f.read()))
        except FileNotFoundError:
            data = Vividict()
        data[key] = des_info
        with open("designs.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(data))
    else:
        print("Filter for designs by Tag, or enter ALL:")
        printtagstext()
        tag = str(input())
        print("-----------------------------------------")
        if tag == "ALL":
            try:
                with open("designs.json", "r", encoding="utf-8") as f:
                    data = json.loads(f.read())
            except FileNotFoundError:
                print("No Designs Loaded.")
                sys.exit(0)
            for item in data:
                print(data[item]['name'].ljust(32, " ") + " - " + specifertofull(data[item]['tags']))
        else:
            try:
                with open("designs.json", "r", encoding="utf-8") as f:
                    data = json.loads(f.read())
            except FileNotFoundError:
                print("No Designs Loaded.")
                sys.exit(0)
            for item in data:
                if str(data[item]['tags'])[:len(tag)] == tag:
                    key = item + ".txt"
                    break
            with open(key, "r", encoding="utf-8") as f:
                print(f.read())
    sys.exit(0)

if __name__ == "__main__":
    main()