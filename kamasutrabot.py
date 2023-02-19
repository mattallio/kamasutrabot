import telebot, random, os, time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from keep_alive import keep_alive
from replit import db

API_KEY = os.environ['API_KEY']

kamasutra = telebot.TeleBot(API_KEY)

#adds the user in the database and initializes its properties
def addUser(message):
    if str(message.chat.id) not in db:
        db[str(message.chat.id)] = {}
        db[str(message.chat.id)]['partecipants'] = 1
        db[str(message.chat.id)]['difficulty'] = 0
        db[str(message.chat.id)]['timer'] = 1
        db[str(message.chat.id)]['checkDifficulty'] = 1
        db[str(message.chat.id)]['checkTimer'] = 1
        db[str(message.chat.id)]['checkPositions'] = 1
        db[str(message.chat.id)]['checkPartecipants'] = 1
        db[str(message.chat.id)]['checkAdventure'] = 1
        db[str(message.chat.id)]['checkSextoys'] = 1
        db[str(message.chat.id)]['checkSextoysPassive'] = 1
        db[str(message.chat.id)]['positions'] = 1
        db[str(message.chat.id)]['experience'] = 0
        db[str(message.chat.id)]['stop'] = 0
        db[str(message.chat.id)]['back'] = 0
        db[str(message.chat.id)]['selection'] = 0
        db[str(message.chat.id)]['partecpiants_selection'] = 0
        db[str(message.chat.id)]['sextoys_selection'] = 0
        db[str(message.chat.id)]['sextoys_selection_passive'] = 0
        db[str(message.chat.id)]['activetoys'] = [["Dildo",0],["Vibrator",0], ["Flashlight",0]]        #maybe cock pump
        db[str(message.chat.id)]['passivetoys'] = [["Nipple Clamps",0],["Anal Plug",0],["Cock Ring",0]]

#counts how many elements are there in a folder
def countFolder(commandFolder):
   dir_path = fr'{commandFolder}'
   count = 0
   # Iterate directory
   for path in os.listdir(dir_path):
      # check if current path is a file
      if os.path.isfile(os.path.join(dir_path, path)):
         count += 1
   #print('File count:', count)
   count = int(count/2)
   return count

#send the photos based on settings
def sendPhotos(message, folder, time_per_position):
    folder_len = countFolder(folder)
    i = 0
    timePassed = 0
    while i < db[str(message.chat.id)]['positions'] and db[str(message.chat.id)]['stop'] != 1:
        randomNum = random.randint(1,folder_len)
        photo = open(fr"{folder}/{randomNum}.png", "rb")
        text = open(fr"{folder}/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        timePassed = 0
        while timePassed < time_per_position and db[str(message.chat.id)]['stop'] != 1:
            time.sleep(1)
            timePassed += 1
        i += 1
    return timePassed

#randomly select how many sex toys to use between the selected ones
def usingActiveToys(message, folders, time_per_position):
    actualPositions = db[str(message.chat.id)]['positions']
    timePassed = 0
    passiveNum = 0
    for i in range(0,len(db[str(message.chat.id)]['passivetoys'])):
        if db[str(message.chat.id)]['passivetoys'][i][1] == 1:
            passiveNum += 1
    for j in folders:
        folder = f"single/{j}"
        if j != folders[len(folders)-1]:
            randPositions = random.randint(1, int((actualPositions/2)+1))
            actualPositions -= randPositions
            if random.randint(0,1) == 0 and passiveNum!=0:
                check = 0
                while check == 0 and passiveNum != 0 and db[str(message.chat.id)]['stop'] != 1:
                    randomPassiveToy = random.randint(0, len(db[str(message.chat.id)]['passivetoys'])-1)
                    if db[str(message.chat.id)]['passivetoys'][randomPassiveToy][1] == 1:
                        check = 1
                        title = f"single/{db[str(message.chat.id)]['passivetoys'][randomPassiveToy][0]}.png"
                        photo = open(title, "rb")           
                        kamasutra.send_photo(message.chat.id, photo)
                        kamasutra.send_message(message.chat.id, f"Time to put your {db[str(message.chat.id)]['passivetoys'][randomPassiveToy][0]} on!")
                        db[str(message.chat.id)]['passivetoys'][randomPassiveToy][1] = 0
                        passiveNum -= 1
                        photo.close()
        else:
            randPositions = actualPositions
            check = 0
            while check == 0 and passiveNum != 0 and db[str(message.chat.id)]['stop'] != 1:
                randomPassiveToy = random.randint(0, len(db[str(message.chat.id)]['passivetoys'])-1)
                if db[str(message.chat.id)]['passivetoys'][randomPassiveToy][1] == 1:
                    check = 1
                    title = f"single/{db[str(message.chat.id)]['passivetoys'][randomPassiveToy][0]}.png"
                    photo = open(title, "rb")
                    kamasutra.send_photo(message.chat.id, photo)
                    kamasutra.send_message(message.chat.id, f"Time to put your {db[str(message.chat.id)]['passivetoys'][randomPassiveToy][0]} on!")
                    db[str(message.chat.id)]['passivetoys'][randomPassiveToy][1] = 0
                    passiveNum -= 1
                    photo.close()
        folder_len = countFolder(folder)
        i = 0
        timePassed = 0
        while i < randPositions and db[str(message.chat.id)]['stop'] != 1:
            randomNum = random.randint(1,folder_len)
            photo = open(fr"{folder}/{randomNum}.png", "rb")
            text = open(fr"{folder}/{randomNum}.txt", "r")
            textt = text.read()
            kamasutra.send_photo(message.chat.id, photo)
            kamasutra.send_message(message.chat.id, textt)
            photo.close()
            timePassed = 0
            while timePassed < time_per_position and db[str(message.chat.id)]['stop'] != 1:
                time.sleep(1)
                timePassed += 1
            i += 1

#start the adventure
def adventure(message):
    db[str(message.chat.id)]['timer'] = db[str(message.chat.id)]['timer']*60
    time_per_position = db[str(message.chat.id)]['timer']/db[str(message.chat.id)]['positions']
    markup = ReplyKeyboardMarkup()
    starting = KeyboardButton("START THE ADVENTURE")
    markup.add(starting)
    kamasutra.send_message(message.chat.id, "Setup completed!")
    time.sleep(1)
    kamasutra.send_message(message.chat.id, "Shall we proceed?", reply_markup=markup)
    while db[str(message.chat.id)]['checkAdventure'] != 0:
        time.sleep(1)
        if db[str(message.chat.id)]['back'] == 1:
            quit()
    if db[str(message.chat.id)]['partecipants']== 1:
        toysnum = 0
        for i in range(0,len(db[str(message.chat.id)]['activetoys'])):
            if db[str(message.chat.id)]['activetoys'][i][1] == 1:
                toysnum +=1
        folders = []
        if toysnum > 0:
            toysRandnum = random.randint(1, toysnum)
            i=0
            while i < toysRandnum:
                randomToy = random.randint(0, len(db[str(message.chat.id)]['activetoys'])-1)
                if db[str(message.chat.id)]['activetoys'][randomToy][1] == 1:
                    db[str(message.chat.id)]['activetoys'][randomToy][1] = 2
                    i += 1
            for i in range(0,len(db[str(message.chat.id)]['activetoys'])):
                if db[str(message.chat.id)]['activetoys'][i][1] == 2:
                    folders.append(db[str(message.chat.id)]['activetoys'][i][0])
            usingActiveToys(message, folders, time_per_position)
        else:
            kamasutra.send_message(message.chat.id, "You will use no active toys in this session")
            kamasutra.send_message(message.chat.id, "This feature is not ready yet, come back soon!")
    elif db[str(message.chat.id)]['partecipants']== 2:
        sendPhotos(message, f"couple/level{db[str(message.chat.id)]['difficulty']}", time_per_position)
    elif db[str(message.chat.id)]['partecipants']== 3:
        sendPhotos(message, "trio", time_per_position)
    db[str(message.chat.id)]['experience'] = 0
    if db[str(message.chat.id)]['stop'] != 1:
        db[str(message.chat.id)]['checkAdventure'] = 1
        kamasutra.send_message(message.chat.id, "I hope that was a positive experience, come back soon!")
        time.sleep(2)
        home(message)

#set the number of positions
def setPositions(message):
    markup = ReplyKeyboardMarkup()
    add1pos = KeyboardButton("+1 Position")
    remove1pos = KeyboardButton("-1 Position")
    backButton = KeyboardButton("Back to Timer")
    confirmPositions = KeyboardButton("CONFIRM POSITIONS")
    markup.add(add1pos, remove1pos, backButton, confirmPositions)
    kamasutra.send_message(message.chat.id, "How many positions would you like to try?", reply_markup=markup)
    kamasutra.send_message(message.chat.id, f"Positions: {db[str(message.chat.id)]['positions']}")
    db[str(message.chat.id)]['back'] = 0
    while db[str(message.chat.id)]['checkPositions'] != 0:
        time.sleep(1)
        if db[str(message.chat.id)]['stop'] == 1:
            quit()
    db[str(message.chat.id)]['checkPositions'] = 1
    kamasutra.send_message(message.chat.id, f"You have selected {db[str(message.chat.id)]['positions']} positions")

#set the timer
def setTimer(message):
    db[str(message.chat.id)]['selection'] = 1
    markup = ReplyKeyboardMarkup()
    add5min = KeyboardButton("+5 Min")
    remove5min = KeyboardButton("-5 Min")
    add1min = KeyboardButton("+1 Min")
    remove1min = KeyboardButton("-1 Min")
    confirmTimer = KeyboardButton("CONFIRM TIMER")
    markup.add(add1min, remove1min, add5min, remove5min, confirmTimer)
    kamasutra.send_message(message.chat.id, "How long would you like the experience to last?", reply_markup=markup)
    kamasutra.send_message(message.chat.id, f"Timer: {db[str(message.chat.id)]['timer']} minutes")
    while db[str(message.chat.id)]['checkTimer']!= 0:
        time.sleep(1)
        if db[str(message.chat.id)]['stop'] == 1:
            quit()
    db[str(message.chat.id)]['checkTimer'] = 1
    kamasutra.send_message(message.chat.id, f"The adventure will last: {db[str(message.chat.id)]['timer']} minutes")
    setPositions(message)

#set the difficulty level
def setDifficulty(message):
    markup = ReplyKeyboardMarkup()
    level1 = KeyboardButton("<3")
    level2 = KeyboardButton("<3 <3")
    level3 = KeyboardButton("<3 <3 <3")
    level4 = KeyboardButton("<3 <3 <3 <3")
    markup.add(level1,level2,level3,level4)
    kamasutra.send_message(message.chat.id, "Select the difficulty level", reply_markup=markup)
    while db[str(message.chat.id)]['checkDifficulty'] != 0:
        time.sleep(1)
        if db[str(message.chat.id)]['stop'] == 1:
            quit()
    db[str(message.chat.id)]['checkDifficulty'] = 1
    kamasutra.send_message(message.chat.id, f"Difficulty: {db[str(message.chat.id)]['difficulty']}")
    setTimer(message)

#set which passive toys to use
def setPassivetoys(message):
    db[str(message.chat.id)]['sextoys_selection_passive'] = 1
    markup = ReplyKeyboardMarkup()
    clamps = KeyboardButton("Nipple Clamps")
    plug = KeyboardButton("Anal Plug")
    ring = KeyboardButton("Cock Ring")
    letsgo = KeyboardButton("LET'S GO")
    markup.add(clamps, plug, ring, letsgo)
    kamasutra.send_message(message.chat.id, "Do you have any of these toys?", reply_markup=markup)
    while db[str(message.chat.id)]['checkSextoysPassive']!= 0:
        time.sleep(1)
        if db[str(message.chat.id)]['stop'] == 1:
            quit()
    db[str(message.chat.id)]['sextoys_selection_passive'] = 0
    setTimer(message)

#set which active toys to use
def setActivetoys(message):
    db[str(message.chat.id)]['sextoys_selection'] = 1
    markup = ReplyKeyboardMarkup()
    dildo = KeyboardButton("Dildo")
    vibrator = KeyboardButton("Vibrator")
    flashlight = KeyboardButton("Flashlight")
    #pump = KeyboardButton("Cock Pump") 
    confirm = KeyboardButton("ALL DONE")
    markup.add(dildo,vibrator,flashlight,confirm)
    kamasutra.send_message(message.chat.id, "Click on every toy that you have", reply_markup=markup)
    while db[str(message.chat.id)]['checkSextoys']!= 0:
        time.sleep(1)
        if db[str(message.chat.id)]['stop'] == 1:
            quit()
    db[str(message.chat.id)]['sextoys_selection'] = 0
    setPassivetoys(message)

#set the partecipants' number
def setPartecipants(message):
    db[str(message.chat.id)]['partecipants_selection'] = 1
    markup = ReplyKeyboardMarkup()
    single = KeyboardButton("Single")
    couple = KeyboardButton("Couple")
    trio = KeyboardButton("Trio")
    markup.add(single,couple,trio)
    kamasutra.send_message(message.chat.id, "Who wants to jump in this adventure?", reply_markup=markup)
    while db[str(message.chat.id)]['checkPartecipants'] != 0:
        time.sleep(1)
        if db[str(message.chat.id)]['stop'] == 1:
            quit()
    db[str(message.chat.id)]['checkPartecipants'] = 1
    kamasutra.send_message(message.chat.id, f"Partecipants: {db[str(message.chat.id)]['partecipants']}")
    db[str(message.chat.id)]['partecipants_selection'] = 0
    if db[str(message.chat.id)]['partecipants']== 1:
        setActivetoys(message)
    elif db[str(message.chat.id)]['partecipants']== 2:
        setDifficulty(message)
    else:
        setTimer(message)

#command start   
@kamasutra.message_handler(commands=["start"])
def start(message):
    addUser(message)
    db[str(message.chat.id)]['selection'] = 0
    db[str(message.chat.id)]['partecipants_selection'] = 0
    db[str(message.chat.id)]['timer'] = 0
    db[str(message.chat.id)]['difficulty'] = 0
    db[str(message.chat.id)]['checkDifficulty'] = 1
    db[str(message.chat.id)]['checkTimer'] = 1
    db[str(message.chat.id)]['checkPositions'] = 1
    db[str(message.chat.id)]['checkPartecipants'] = 1
    db[str(message.chat.id)]['positions'] = 1
    db[str(message.chat.id)]['experience'] = 0
    db[str(message.chat.id)]['timer'] = 1
    db[str(message.chat.id)]['checkAdventure'] = 1
    db[str(message.chat.id)]['sextoys_selection'] = 0
    db[str(message.chat.id)]['sextoys_selection_passive'] = 0
    db[str(message.chat.id)]['checkSextoys'] = 1
    db[str(message.chat.id)][' checkSextoysPassive'] = 1
    db[str(message.chat.id)]['activetoys'] = [["Dildo",0],["Vibrator",0], ["Flashlight",0]]
    db[str(message.chat.id)]['passivetoys'] = [["Nipple Clamps",0],["Anal Plug",0],["Cock Ring",0]]
    markup = ReplyKeyboardMarkup(row_width=2)
    command1 = KeyboardButton("RANDOM POSITION")
    command2 = KeyboardButton("FULL EXPERIENCE")
    markup.add(command1,command2)
    kamasutra.send_message(message.chat.id, "Good to see you! How can I help you?", reply_markup=markup)

#command to return home
@kamasutra.message_handler(commands=["home"])
def home(message):
    addUser(message)
    db[str(message.chat.id)]['selection'] = 0
    db[str(message.chat.id)]['partecipants_selection'] = 0
    db[str(message.chat.id)]['timer'] = 0
    db[str(message.chat.id)]['difficulty'] = 0
    db[str(message.chat.id)]['checkDifficulty'] = 1
    db[str(message.chat.id)]['checkTimer'] = 1
    db[str(message.chat.id)]['checkPositions'] = 1
    db[str(message.chat.id)]['checkPartecipants'] = 1
    db[str(message.chat.id)]['positions'] = 1
    db[str(message.chat.id)]['experience'] = 0
    db[str(message.chat.id)]['timer'] = 1
    db[str(message.chat.id)]['checkAdventure'] = 1
    db[str(message.chat.id)]['sextoys_selection'] = 0
    db[str(message.chat.id)]['sextoys_selection_passive'] = 0
    db[str(message.chat.id)]['checkSextoys'] = 1
    db[str(message.chat.id)]['checkSextoysPassive'] = 1
    db[str(message.chat.id)]['activetoys'] = [["Dildo",0],["Vibrator",0], ["Flashlight",0]]
    db[str(message.chat.id)]['passivetoys'] = [["Nipple Clamps",0],["Anal Plug",0],["Cock Ring",0]]
    markup = ReplyKeyboardMarkup(row_width=2)
    command1 = KeyboardButton("RANDOM POSITION")
    command2 = KeyboardButton("FULL EXPERIENCE")
    markup.add(command1,command2)
    kamasutra.send_message(message.chat.id, "What shall we do next?", reply_markup=markup)

#command to send a random single image
@kamasutra.message_handler(commands=["single"])
def randomSingle(message):
    addUser(message)
    randomToy = random.randint(0, len(db[str(message.chat.id)]['activetoys'])-1)
    folderLen = countFolder(f"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}")
    randomNum = random.randint(1, folderLen)
    photo = open(fr"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}/{randomNum}.png", "rb")
    text = open(fr"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}/{randomNum}.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

#command to send a random couple image
@kamasutra.message_handler(commands=["couple"])
def randomCouple(message):
    addUser(message)
    randomLevel = random.randint(1,4)
    randomNum = random.randint(1, countFolder(f"couple/level{randomLevel}"))
    photo = open(fr"couple/level{randomLevel}/{randomNum}.png", "rb")
    text = open(fr"couple/level{randomLevel}/{randomNum}.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

#command to send a random trio image
@kamasutra.message_handler(commands=["trio"])
def randomTrio(message):
    addUser(message)
    randomNum = random.randint(1, countFolder("trio"))
    photo = open(rf"trio/{randomNum}.png", "rb")
    text = open(fr"trio/{randomNum}.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

#command to send the pillow instructions
@kamasutra.message_handler(commands=["pillow"])
def pillowDIY(message):
    addUser(message)
    photo = open(r"single/pillow.png", "rb")
    text = open(r"single/pillow.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

#command for help
@kamasutra.message_handler(commands=["help"])
def help(message):
    addUser(message)
    commandList = open("help.txt", "r")
    commandList = commandList.read()
    kamasutra.send_message(message.chat.id, commandList)

#send a random position of the selected difficulty level
@kamasutra.message_handler(func=lambda m:"RANDOM POSITION" in m.text.upper())
def command1(message):
    addUser(message)
    markup = ReplyKeyboardMarkup()
    level1 = KeyboardButton("<3")
    level2 = KeyboardButton("<3 <3")
    level3 = KeyboardButton("<3 <3 <3")
    level4 = KeyboardButton("<3 <3 <3 <3")
    randombutton = KeyboardButton("RANDOM")
    back = KeyboardButton("Go back")
    markup.add(back,randombutton,level1,level2,level3,level4)
    kamasutra.send_message(message.chat.id, "Choose the level of difficulty of the position, or let me choose", reply_markup=markup)

#the full experience starts
@kamasutra.message_handler(func=lambda m:"FULL EXPERIENCE" in m.text.upper())
def command2(message):
    addUser(message)
    db[str(message.chat.id)]['experience'] = 1
    db[str(message.chat.id)]['stop'] = 0
    setPartecipants(message)

#buttons to select the number of partecipants
@kamasutra.message_handler(func=lambda m:"SINGLE" in m.text.upper())
def single(message):
    addUser(message)
    if db[str(message.chat.id)]['partecipants_selection'] == 1:
        db[str(message.chat.id)]['partecipants']= 1
        db[str(message.chat.id)]['checkPartecipants'] = 0

@kamasutra.message_handler(func=lambda m:"COUPLE" in m.text.upper())
def couple(message):
    addUser(message)
    if db[str(message.chat.id)]['partecipants_selection'] == 1:
        db[str(message.chat.id)]['partecipants']= 2
        db[str(message.chat.id)]['checkPartecipants'] = 0

@kamasutra.message_handler(func=lambda m:"TRIO" in m.text.upper())
def trio(message):
    addUser(message)
    if db[str(message.chat.id)]['partecipants_selection'] == 1:
        db[str(message.chat.id)]['partecipants']= 3
        db[str(message.chat.id)]['checkPartecipants'] = 0

#buttons to select the active toys
@kamasutra.message_handler(func=lambda m:"DILDO" in m.text.upper())
def dildo(message):
    if db[str(message.chat.id)]['sextoys_selection'] == 1:
        if db[str(message.chat.id)]['activetoys'][0][1] == 0:
            db[str(message.chat.id)]['activetoys'][0][1] = 1
            kamasutra.send_message(message.chat.id, "Dildo selected! If you want to remove dildo tap again the 'DILDO' button, select all the toys you want to use and then click 'ALL DONE'")
        else:
            db[str(message.chat.id)]['activetoys'][0][1] = 0
            kamasutra.send_message(message.chat.id, "You removed Dildo!")

@kamasutra.message_handler(func=lambda m:"VIBRATOR" in m.text.upper())
def vibrator(message):
    if db[str(message.chat.id)]['sextoys_selection'] == 1:
        if db[str(message.chat.id)]['activetoys'][1][1] == 0:
            db[str(message.chat.id)]['activetoys'][1][1] = 1
            kamasutra.send_message(message.chat.id, "Vibrator selected! If you want to remove dildo tap again the 'VIBRATOR' button, select all the toys you want to use and then click 'ALL DONE'")
        else:
            db[str(message.chat.id)]['activetoys'][1][1] = 0
            kamasutra.send_message(message.chat.id, "You removed Vibrator!")
@kamasutra.message_handler(func=lambda m:"FLASHLIGHT" in m.text.upper())
def flashlight(message):
    if db[str(message.chat.id)]['sextoys_selection'] == 1:
        if db[str(message.chat.id)]['activetoys'][2][1] == 0:
            db[str(message.chat.id)]['activetoys'][2][1] = 1
            kamasutra.send_message(message.chat.id, "Flashlight selected! If you want to remove dildo tap again the 'FLASHLIGHT' button, select all the toys you want to use and then click 'ALL DONE'")
        else:
            db[str(message.chat.id)]['activetoys'][2][1] = 0
            kamasutra.send_message(message.chat.id, "You removed Flashlight!")

"""@kamasutra.message_handler(func=lambda m:"COCK PUMP" in m.text.upper())
def pump(message):
    if db[str(message.chat.id)]['sextoys_selection'] == 1:
        db[str(message.chat.id)]['activetoys'][3][1] = 1
"""

#buttons to select the passive toys
@kamasutra.message_handler(func=lambda m:"NIPPLE CLAMPS" in m.text.upper())
def clamps(message):
    if db[str(message.chat.id)]['sextoys_selection_passive'] == 1:
        if db[str(message.chat.id)]['passivetoys'][0][1] == 0:
            db[str(message.chat.id)]['passivetoys'][0][1] = 1
            kamasutra.send_message(message.chat.id, "Nipple Clamps selected! If you want to remove dildo tap again the 'NIPPLE CLAMPS' button, select all the toys you want to use and then click 'LET'S GO'")
        else:
            db[str(message.chat.id)]['passivetoys'][0][1] = 0
            kamasutra.send_message(message.chat.id, "You removed Nipple Clamps!")

@kamasutra.message_handler(func=lambda m:"ANAL PLUG" in m.text.upper())
def plug(message):
    if db[str(message.chat.id)]['sextoys_selection_passive'] == 1:
        if db[str(message.chat.id)]['passivetoys'][1][1] == 0:
            db[str(message.chat.id)]['passivetoys'][1][1] = 1
            kamasutra.send_message(message.chat.id, "Anal Plug selected! If you want to remove dildo tap again the 'ANAL PLUG' button, select all the toys you want to use and then click 'LET'S GO'")
        else:
            db[str(message.chat.id)]['passivetoys'][1][1] = 0
            kamasutra.send_message(message.chat.id, "You removed Anal Plug!")
            
@kamasutra.message_handler(func=lambda m:"COCK RING" in m.text.upper())
def ring(message):
    if db[str(message.chat.id)]['sextoys_selection_passive'] == 1:
        if db[str(message.chat.id)]['passivetoys'][2][1] == 0:
            db[str(message.chat.id)]['passivetoys'][2][1] = 1
            kamasutra.send_message(message.chat.id, "Cock Ring selected! If you want to remove dildo tap again the 'COCK RING' button, select all the toys you want to use and then click 'LET'S GO'")
        else:
            db[str(message.chat.id)]['passivetoys'][2][1] = 0
            kamasutra.send_message(message.chat.id, "You removed Cock Ring!")

#moves to the selection of the passive toys
@kamasutra.message_handler(func=lambda m:"ALL DONE" in m.text.upper())
def allDone(message):
    if db[str(message.chat.id)]['sextoys_selection'] == 1:
        db[str(message.chat.id)]['checkSextoys'] = 0

#start the single experience
@kamasutra.message_handler(func=lambda m:"LET'S GO" in m.text.upper())
def lesgo(message):
    if db[str(message.chat.id)]['sextoys_selection_passive'] == 1:
       db[str(message.chat.id)]['checkSextoysPassive'] = 0

#buttons to select the difficulty level
@kamasutra.message_handler(func=lambda m:"<3 <3 <3 <3" in m.text.upper())
def level4(message):
    db[str(message.chat.id)]['difficulty'] = 4
    db[str(message.chat.id)]['checkDifficulty'] = 0
    if db[str(message.chat.id)]['experience'] == 0:
        randomNum = random.randint(1,countFolder("couple/level4"))
        photo = open(fr"couple/level4/{randomNum}.png", "rb")
        text = open(fr"couple/level4/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close

@kamasutra.message_handler(func=lambda m:"<3 <3 <3" in m.text.upper())
def level3(message):
    db[str(message.chat.id)]['difficulty'] = 3
    db[str(message.chat.id)]['checkDifficulty'] = 0
    if db[str(message.chat.id)]['experience'] == 0:
        randomNum = random.randint(1,countFolder("couple/level3"))
        photo = open(fr"couple/level3/{randomNum}.png", "rb")
        text = open(fr"couple/level3/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()

@kamasutra.message_handler(func=lambda m:"<3 <3" in m.text.upper())
def level2(message):
    db[str(message.chat.id)]['difficulty'] = 2
    db[str(message.chat.id)]['checkDifficulty'] = 0
    if db[str(message.chat.id)]['experience'] == 0:
        randomNum = random.randint(1,countFolder("couple/level2"))
        photo = open(fr"couple/level2/{randomNum}.png", "rb")
        text = open(fr"couple/level2/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()

@kamasutra.message_handler(func=lambda m:"<3" in m.text.upper())
def level1(message):
    db[str(message.chat.id)]['difficulty'] = 1
    db[str(message.chat.id)]['checkDifficulty'] = 0
    if db[str(message.chat.id)]['experience'] == 0:
        randomNum = random.randint(1,countFolder("couple/level1"))
        photo = open(fr"couple/level1/{randomNum}.png", "rb")
        text = open(fr"couple/level1/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()

#settings' buttons
@kamasutra.message_handler(func=lambda m:"BACK TO TIMER" in m.text.upper())
def gobackTimer(message):
    db[str(message.chat.id)]['checkPositions'] = 0
    setTimer(message)

@kamasutra.message_handler(func=lambda m:"GO BACK" in m.text.upper())
def goback(message):
    db[str(message.chat.id)]['stop'] = 1
    db[str(message.chat.id)]['experience'] = 0
    db[str(message.chat.id)]['checkDifficulty'] = 1
    home(message)

@kamasutra.message_handler(func=lambda m:"CONFIRM TIMER" in m.text.upper())
def confirmTimer(message):
    db[str(message.chat.id)]['checkTimer'] = 0
    
@kamasutra.message_handler(func=lambda m:"CONFIRM POSITIONS" in m.text.upper())
def confirmPositions(message):
    db[str(message.chat.id)]['checkPositions'] = 0
    db[str(message.chat.id)]['selection'] = 0
    adventure(message)

@kamasutra.message_handler(func=lambda m:"+1 MIN" in m.text.upper())
def add1Time(message):
    if db[str(message.chat.id)]['selection'] == 1:
        db[str(message.chat.id)]['timer'] += 1
        kamasutra.send_message(message.chat.id, f"Timer: {db[str(message.chat.id)]['timer']} minutes")

@kamasutra.message_handler(func=lambda m:"-1 MIN" in m.text.upper())
def remove1Time(message):
    if db[str(message.chat.id)]['selection'] == 1:
        if db[str(message.chat.id)]['timer'] > 1:
            db[str(message.chat.id)]['timer'] -= 1
            kamasutra.send_message(message.chat.id, f"Timer: {db[str(message.chat.id)]['timer']} minutes")
        else:
            kamasutra.send_message(message.chat.id, "Come on, you can last a bit more!")
            kamasutra.send_message(message.chat.id, f"Timer: {db[str(message.chat.id)]['timer']} minutes")

@kamasutra.message_handler(func=lambda m:"+5 MIN" in m.text.upper())
def add5Time(message):
    if db[str(message.chat.id)]['selection'] == 1:
        db[str(message.chat.id)]['timer'] += 5
        kamasutra.send_message(message.chat.id, f"Timer: {db[str(message.chat.id)]['timer']} minutes")

@kamasutra.message_handler(func=lambda m:"-5 MIN" in m.text.upper())
def remove5Time(message):
    if db[str(message.chat.id)]['selection'] == 1:
        if db[str(message.chat.id)]['timer'] > 5:
            db[str(message.chat.id)]['timer'] -= 5
            kamasutra.send_message(message.chat.id, f"Timer: {db[str(message.chat.id)]['timer']} minutes")
        else:
            kamasutra.send_message(message.chat.id, "Come on, you can last a bit more!")
            kamasutra.send_message(message.chat.id, f"Timer: {db[str(message.chat.id)]['timer']} minutes")

@kamasutra.message_handler(func=lambda m:"+1 POSITION" in m.text.upper())
def addPosition(message):
    if db[str(message.chat.id)]['selection'] == 1:
        db[str(message.chat.id)]['positions'] += 1
        kamasutra.send_message(message.chat.id, f"Positions: {db[str(message.chat.id)]['positions']}")

@kamasutra.message_handler(func=lambda m:"-1 POSITION" in m.text.upper())
def removePosition(message):
    if db[str(message.chat.id)]['selection'] == 1:
        if db[str(message.chat.id)]['positions'] > 1:
            db[str(message.chat.id)]['positions'] -= 1
            kamasutra.send_message(message.chat.id, f"Positions: {db[str(message.chat.id)]['positions']}")
        else:
            kamasutra.send_message(message.chat.id, "Come on, try at least one position!")
            kamasutra.send_message(message.chat.id, f"Positions: {db[str(message.chat.id)]['positions']}")

#button to start the adventure
@kamasutra.message_handler(func=lambda m:"START THE ADVENTURE" in m.text.upper())
def startadventure(message):
    db[str(message.chat.id)]['checkAdventure'] = 0
    markup = ReplyKeyboardMarkup()
    next = KeyboardButton("Change")
    stopButton = KeyboardButton("Stop")
    markup.add(next,stopButton)
    kamasutra.send_message(message.chat.id, "Here we go!", reply_markup=markup)

#button to send a completely random image
@kamasutra.message_handler(func=lambda m:"RANDOM" in m.text.upper())
def randomPosition(message):
    addUser(message)
    if db[str(message.chat.id)]['experience'] == 0:
        randomPartecipants = random.randint(1,3)
        if randomPartecipants == 1:
            randomToy = random.randint(0, len(db[str(message.chat.id)]['activetoys'])-1)
            folderLen = countFolder(f"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}")
            randomNum = random.randint(1, folderLen)
            photo = open(fr"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}/{randomNum}.png", "rb")
            text = open(fr"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}/{randomNum}.txt", "r")
            textt = text.read()
            kamasutra.send_photo(message.chat.id, photo)
            kamasutra.send_message(message.chat.id, textt)
            photo.close()
            text.close()
        if randomPartecipants == 2:
            randomLevel = random.randint(1,4)
            randomNum = random.randint(1, countFolder(f"couple/level{randomLevel}"))
            photo = open(fr"couple/level{randomLevel}/{randomNum}.png", "rb")
            text = open(fr"couple/level{randomLevel}/{randomNum}.txt", "r")
            textt = text.read()
            kamasutra.send_photo(message.chat.id, photo)
            kamasutra.send_message(message.chat.id, textt)
            photo.close()
            text.close
        if randomPartecipants == 3:
            randomNum = random.randint(1, countFolder("trio"))
            photo = open(rf"trio/{randomNum}.png", "rb")
            text = open(fr"trio/{randomNum}.txt", "r")
            textt = text.read()
            kamasutra.send_photo(message.chat.id, photo)
            kamasutra.send_message(message.chat.id, textt)
            photo.close()
            text.close()

#button to change position
@kamasutra.message_handler(func=lambda m:"CHANGE" in m.text.upper())
def changePosition(message):
    if db[str(message.chat.id)]['partecipants']== 1:
        check = 1
        while check != 0:
            randomToy = random.randint(0, len(db[str(message.chat.id)]['activetoys'])-1)
            if db[str(message.chat.id)]['activetoys'][randomToy][1] == 2:
                folderLen = countFolder(f"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}")
                randomNum = random.randint(1, folderLen)
                photo = open(fr"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}/{randomNum}.png", "rb")
                text = open(fr"single/{db[str(message.chat.id)]['activetoys'][randomToy][0]}/{randomNum}.txt", "r")
                textt = text.read()
                kamasutra.send_photo(message.chat.id, photo)
                kamasutra.send_message(message.chat.id, textt)
                photo.close()
                text.close()
                check = 0
    if db[str(message.chat.id)]['partecipants']== 2:
        folderLen = countFolder(f"couple/level{db[str(message.chat.id)]['difficulty']}")
        randomNum = random.randint(1, folderLen)
        photo = open(fr"couple/level{db[str(message.chat.id)]['difficulty']}/{randomNum}.png", "rb")
        text = open(fr"couple/level{db[str(message.chat.id)]['difficulty']}/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()
    if db[str(message.chat.id)]['partecipants']== 3:
        randomNum = random.randint(1, countFolder("trio"))
        photo = open(rf"trio/{randomNum}.png", "rb")
        text = open(fr"trio/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()

#button to stop the experience
@kamasutra.message_handler(func=lambda m:"STOP" in m.text.upper())
def stopping(message):
    addUser(message)
    if db[str(message.chat.id)]['checkAdventure'] == 0:
        db[str(message.chat.id)]['stop'] = 1
        home(message)

keep_alive()
kamasutra.polling()