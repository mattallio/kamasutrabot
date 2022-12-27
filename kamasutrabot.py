import telebot, random, os, time
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from keep_alive import keep_alive

API_KEY = os.environ['API_KEY']

kamasutra = telebot.TeleBot(API_KEY)

partecipants = 1
difficulty = 0
timer = 1
checkDifficulty = 1
checkTimer = 1
checkPositions = 1
checkAdventure = 1
checkPartecipants = 1
checkSextoys = 1
checkSextoysPassive = 1
positions = 1
experience = 0
stop = 0
back = 0
selection = 0
partecipants_selection = 0
sextoys_selection = 0
sextoys_selection_passive = 0
activetoys = [["Dildo",0],["Vibrator",0], ["Flashlight",0]]      #maybe cock pump
passivetoys = [["Nipple Clamps",0],["Anal Plug",0],["Cock Ring",0]]

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

def sendPhotos(message, folder, time_per_position):
    folder_len = countFolder(folder)
    i = 0
    timePassed = 0
    while i < positions and stop != 1:
        randomNum = random.randint(1,folder_len)
        photo = open(fr"{folder}/{randomNum}.png", "rb")
        text = open(fr"{folder}/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        timePassed = 0
        while timePassed < time_per_position and stop != 1:
            time.sleep(1)
            timePassed += 1
        i += 1
    return timePassed

def usingActiveToys(message, folders, time_per_position):
    global positions, passivetoys, timer, stop
    actualPositions = positions
    timePassed = 0
    passiveNum = 0
    for i in range(0,len(passivetoys)):
        if passivetoys[i][1] == 1:
            passiveNum += 1
    for j in folders:
        folder = f"single/{j}"
        if j != folders[len(folders)-1]:
            randPositions = random.randint(1, int((actualPositions/2)+1))
            actualPositions -= randPositions
            if random.randint(0,1) == 0 and passiveNum!=0:
                check = 0
                while check == 0 and passiveNum != 0 and stop != 1:
                    randomPassiveToy = random.randint(0, len(passivetoys)-1)
                    if passivetoys[randomPassiveToy][1] == 1:
                        check = 1
                        title = f"single/{passivetoys[randomPassiveToy][0]}.png"
                        photo = open(title, "rb")           
                        kamasutra.send_photo(message.chat.id, photo)
                        kamasutra.send_message(message.chat.id, f"Time to put your {passivetoys[randomPassiveToy][0]} on!")
                        passivetoys[randomPassiveToy][1] = 0
                        passiveNum -= 1
                        photo.close()
        else:
            randPositions = actualPositions
            check = 0
            while check == 0 and passiveNum != 0 and stop != 1:
                randomPassiveToy = random.randint(0, len(passivetoys)-1)
                if passivetoys[randomPassiveToy][1] == 1:
                    check = 1
                    title = f"single/{passivetoys[randomPassiveToy][0]}.png"
                    photo = open(title, "rb")
                    kamasutra.send_photo(message.chat.id, photo)
                    kamasutra.send_message(message.chat.id, f"Time to put your {passivetoys[randomPassiveToy][0]} on!")
                    passivetoys[randomPassiveToy][1] = 0
                    passiveNum -= 1
                    photo.close()
        folder_len = countFolder(folder)
        i = 0
        timePassed = 0
        while i < randPositions and stop != 1:
            randomNum = random.randint(1,folder_len)
            photo = open(fr"{folder}/{randomNum}.png", "rb")
            text = open(fr"{folder}/{randomNum}.txt", "r")
            textt = text.read()
            kamasutra.send_photo(message.chat.id, photo)
            kamasutra.send_message(message.chat.id, textt)
            photo.close()
            timePassed = 0
            while timePassed < time_per_position and stop != 1:
                time.sleep(1)
                timePassed += 1
            i += 1

def adventure(message):
    global activetoys, passivetoys, partecipants, difficulty, timer, positions, checkDifficulty, checkTimer, checkPositions, experience, stop, checkAdventure, back
    timer = timer*60
    time_per_position = timer/positions
    markup = ReplyKeyboardMarkup()
    starting = KeyboardButton("START THE ADVENTURE")
    markup.add(starting)
    kamasutra.send_message(message.chat.id, "Setup completed!")
    time.sleep(1)
    kamasutra.send_message(message.chat.id, "Shall we proceed?", reply_markup=markup)
    while checkAdventure != 0:
        time.sleep(1)
        if back == 1:
            quit()
    if partecipants == 1:
        toysnum = 0
        for i in range(0,len(activetoys)):
            if activetoys[i][1] == 1:
                toysnum +=1
        folders = []
        if toysnum > 0:
            toysRandnum = random.randint(1, toysnum)
            i=0
            while i < toysRandnum:
                randomToy = random.randint(0, len(activetoys)-1)
                if activetoys[randomToy][1] == 1:
                    activetoys[randomToy][1] = 2
                    i += 1
            for i in range(0,len(activetoys)):
                if activetoys[i][1] == 2:
                    folders.append(activetoys[i][0])
            usingActiveToys(message, folders, time_per_position)
        else:
            kamasutra.send_message(message.chat.id, "You will use no active toys in this session")
            kamasutra.send_message(message.chat.id, "This feature is not ready yet, come back soon!")
    elif partecipants == 2:
        sendPhotos(message, f"couple/level{difficulty}", time_per_position)
    elif partecipants == 3:
        sendPhotos(message, "trio", time_per_position)
    experience = 0
    if stop != 1:
        checkAdventure = 1
        kamasutra.send_message(message.chat.id, "I hope that was a positive experience, come back soon!")
        time.sleep(2)
        home(message)

def setPositions(message):
    global positions, checkPositions, back
    markup = ReplyKeyboardMarkup()
    add1pos = KeyboardButton("+1 Position")
    remove1pos = KeyboardButton("-1 Position")
    backButton = KeyboardButton("Back to Timer")
    confirmPositions = KeyboardButton("CONFIRM POSITIONS")
    markup.add(add1pos, remove1pos, backButton, confirmPositions)
    kamasutra.send_message(message.chat.id, "How many positions would you like to try?", reply_markup=markup)
    kamasutra.send_message(message.chat.id, f"Positions: {positions}")
    back = 0
    while checkPositions != 0:
        time.sleep(1)
        if stop == 1:
            quit()
    checkPositions = 1
    kamasutra.send_message(message.chat.id, f"You have selected {positions} positions")

def setTimer(message):
    global timer, checkTimer, selection
    selection = 1
    markup = ReplyKeyboardMarkup()
    add5min = KeyboardButton("+5 Min")
    remove5min = KeyboardButton("-5 Min")
    add1min = KeyboardButton("+1 Min")
    remove1min = KeyboardButton("-1 Min")
    confirmTimer = KeyboardButton("CONFIRM TIMER")
    markup.add(add1min, remove1min, add5min, remove5min, confirmTimer)
    kamasutra.send_message(message.chat.id, "How long would you like the experience to last?", reply_markup=markup)
    kamasutra.send_message(message.chat.id, f"Timer: {timer} minutes")
    while checkTimer!= 0:
        time.sleep(1)
        if stop == 1:
            quit()
    checkTimer = 1
    kamasutra.send_message(message.chat.id, f"The adventure will last: {timer} minutes")
    setPositions(message)

def setDifficulty(message):
    global checkDifficulty, stop, difficulty
    markup = ReplyKeyboardMarkup()
    level1 = KeyboardButton("<3")
    level2 = KeyboardButton("<3 <3")
    level3 = KeyboardButton("<3 <3 <3")
    level4 = KeyboardButton("<3 <3 <3 <3")
    markup.add(level1,level2,level3,level4)
    kamasutra.send_message(message.chat.id, "Select the difficulty level", reply_markup=markup)
    while checkDifficulty != 0:
        time.sleep(1)
        if stop == 1:
            quit()
    checkDifficulty = 1
    kamasutra.send_message(message.chat.id, f"Difficulty: {difficulty}")
    setTimer(message)

def setPassivetoys(message):
    global sextoys_selection_passive, checkSextoysPassive
    sextoys_selection_passive = 1
    markup = ReplyKeyboardMarkup()
    clamps = KeyboardButton("Nipple Clamps")
    plug = KeyboardButton("Anal Plug")
    ring = KeyboardButton("Cock Ring")
    letsgo = KeyboardButton("LET'S GO")
    markup.add(clamps, plug, ring, letsgo)
    kamasutra.send_message(message.chat.id, "Do you have any of these toys?", reply_markup=markup)
    while checkSextoysPassive!= 0:
        time.sleep(1)
        if stop == 1:
            quit()
    sextoys_selection_passive = 0
    setTimer(message)

def setActivetoys(message):
    global sextoys_selection, checkSextoys
    sextoys_selection = 1
    markup = ReplyKeyboardMarkup()
    dildo = KeyboardButton("Dildo")
    vibrator = KeyboardButton("Vibrator")
    flashlight = KeyboardButton("Flashlight")
    #pump = KeyboardButton("Cock Pump") 
    confirm = KeyboardButton("ALL DONE")
    markup.add(dildo,vibrator,flashlight,confirm)
    kamasutra.send_message(message.chat.id, "Click on every toy that you have", reply_markup=markup)
    while checkSextoys!= 0:
        time.sleep(1)
        if stop == 1:
            quit()
    sextoys_selection = 0
    setPassivetoys(message)

def setPartecipants(message):
    global checkPartecipants, partecipants, partecipants_selection
    partecipants_selection = 1
    markup = ReplyKeyboardMarkup()
    single = KeyboardButton("Single")
    couple = KeyboardButton("Couple")
    trio = KeyboardButton("Trio")
    markup.add(single,couple,trio)
    kamasutra.send_message(message.chat.id, "Who wants to jump in this adventure?", reply_markup=markup)
    while checkPartecipants != 0:
        time.sleep(1)
        if stop == 1:
            quit()
    checkPartecipants = 1
    kamasutra.send_message(message.chat.id, f"Partecipants: {partecipants}")
    partecipants_selection = 0
    if partecipants == 1:
        setActivetoys(message)
    elif partecipants == 2:
        setDifficulty(message)
    else:
        setTimer(message)
    
@kamasutra.message_handler(commands=["start"])
def start(message):
    global activetoys, passivetoys, checkSextoysPassive, sextoys_selection_passive, checkSextoys, sextoys_selection, partecipants_selection, selection,difficulty, timer, positions, experience, checkPartecipants,stop, checkDifficulty, checkPositions, checkTimer, checkAdventure
    selection = 0
    partecipants_selection = 0
    timer = 0
    difficulty = 0
    checkDifficulty = 1
    checkTimer = 1
    checkPositions = 1
    checkPartecipants = 1
    positions = 1
    experience = 0
    timer = 1
    checkAdventure = 1
    sextoys_selection = 0
    sextoys_selection_passive = 0
    checkSextoys = 1
    checkSextoysPassive = 1
    activetoys = [["Dildo",0],["Vibrator",0], ["Flashlight",0]]
    passivetoys = [["Nipple Clamps",0],["Anal Plug",0],["Cock Ring",0]]
    markup = ReplyKeyboardMarkup(row_width=2)
    command1 = KeyboardButton("RANDOM POSITION")
    command2 = KeyboardButton("FULL EXPERIENCE")
    markup.add(command1,command2)
    kamasutra.send_message(message.chat.id, "Good to see you! How can I help you?", reply_markup=markup)
      
@kamasutra.message_handler(commands=["home"])
def home(message):
    global activetoys, passivetoys, checkSextoysPassive, sextoys_selection_passive, checkSextoys, sextoys_selection, partecipants_selection, selection,difficulty, timer, positions, experience, checkPartecipants,stop, checkDifficulty, checkPositions, checkTimer, checkAdventure
    selection = 0
    partecipants_selection = 0
    timer = 0
    difficulty = 0
    checkDifficulty = 1
    checkTimer = 1
    checkPositions = 1
    checkPartecipants = 1
    positions = 1
    experience = 0
    timer = 1
    checkAdventure = 1
    sextoys_selection = 0
    sextoys_selection_passive = 0
    checkSextoys = 1
    checkSextoysPassive = 1
    activetoys = [["Dildo",0],["Vibrator",0], ["Flashlight",0]]
    passivetoys = [["Nipple Clamps",0],["Anal Plug",0],["Cock Ring",0]]
    markup = ReplyKeyboardMarkup(row_width=2)
    command1 = KeyboardButton("RANDOM POSITION")
    command2 = KeyboardButton("FULL EXPERIENCE")
    markup.add(command1,command2)
    kamasutra.send_message(message.chat.id, "What shall we do next?", reply_markup=markup)

@kamasutra.message_handler(commands=["single"])
def randomSingle(message):
    global activetoys
    randomToy = random.randint(0, len(activetoys)-1)
    folderLen = countFolder(f"single/{activetoys[randomToy][0]}")
    randomNum = random.randint(1, folderLen)
    photo = open(fr"single/{activetoys[randomToy][0]}/{randomNum}.png", "rb")
    text = open(fr"single/{activetoys[randomToy][0]}/{randomNum}.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

@kamasutra.message_handler(commands=["couple"])
def randomCouple(message):
    randomLevel = random.randint(1,4)
    randomNum = random.randint(1, countFolder(f"couple/level{randomLevel}"))
    photo = open(fr"couple/level{randomLevel}/{randomNum}.png", "rb")
    text = open(fr"couple/level{randomLevel}/{randomNum}.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

@kamasutra.message_handler(commands=["trio"])
def randomTrio(message):
    randomNum = random.randint(1, countFolder("trio"))
    photo = open(rf"trio/{randomNum}.png", "rb")
    text = open(fr"trio/{randomNum}.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

@kamasutra.message_handler(commands=["pillow"])
def pillowDIY(message):
    photo = open(r"single/pillow.png", "rb")
    text = open(r"single/pillow.txt", "r")
    textt = text.read()
    kamasutra.send_photo(message.chat.id, photo)
    kamasutra.send_message(message.chat.id, textt)
    photo.close()
    text.close()

@kamasutra.message_handler(commands=["help"])
def help(message):
    commandList = open("help.txt", "r")
    commandList = commandList.read()
    kamasutra.send_message(message.chat.id, commandList)

@kamasutra.message_handler(func=lambda m:"RANDOM POSITION" in m.text.upper())
def command1(message):
    markup = ReplyKeyboardMarkup()
    level1 = KeyboardButton("<3")
    level2 = KeyboardButton("<3 <3")
    level3 = KeyboardButton("<3 <3 <3")
    level4 = KeyboardButton("<3 <3 <3 <3")
    randombutton = KeyboardButton("RANDOM")
    back = KeyboardButton("Go back")
    markup.add(back,randombutton,level1,level2,level3,level4)
    kamasutra.send_message(message.chat.id, "Choose the level of difficulty of the position, or let me choose", reply_markup=markup)

@kamasutra.message_handler(func=lambda m:"FULL EXPERIENCE" in m.text.upper())
def command2(message):
    global difficulty, timer, experience, stop, worksheet
    experience = 1
    stop = 0
    setPartecipants(message)

@kamasutra.message_handler(func=lambda m:"SINGLE" in m.text.upper())
def single(message):
    global partecipants, checkPartecipants, partecipants_selection
    if partecipants_selection == 1:
        partecipants = 1
        checkPartecipants = 0

@kamasutra.message_handler(func=lambda m:"COUPLE" in m.text.upper())
def couple(message):
    global partecipants, checkPartecipants, partecipants_selection
    if partecipants_selection == 1:
        partecipants = 2
        checkPartecipants = 0

@kamasutra.message_handler(func=lambda m:"TRIO" in m.text.upper())
def trio(message):
    global partecipants, checkPartecipants, partecipants_selection
    if partecipants_selection == 1:
        partecipants = 3
        checkPartecipants = 0

@kamasutra.message_handler(func=lambda m:"DILDO" in m.text.upper())
def dildo(message):
    global sextoys_selection, activetoys
    if sextoys_selection == 1:
        activetoys[0][1] = 1

@kamasutra.message_handler(func=lambda m:"VIBRATOR" in m.text.upper())
def vibrator(message):
    global sextoys_selection, activetoys
    if sextoys_selection == 1:
        activetoys[1][1] = 1

@kamasutra.message_handler(func=lambda m:"FLASHLIGHT" in m.text.upper())
def flashlight(message):
    global sextoys_selection, activetoys
    if sextoys_selection == 1:
       activetoys[2][1] = 1

"""@kamasutra.message_handler(func=lambda m:"COCK PUMP" in m.text.upper())
def pump(message):
    global sextoys_selection, activetoys
    if sextoys_selection == 1:
        activetoys[3][1] = 1
"""
@kamasutra.message_handler(func=lambda m:"NIPPLE CLAMPS" in m.text.upper())
def clamps(message):
    global sextoys_selection_passive, passivetoys
    if sextoys_selection_passive == 1:
        passivetoys[0][1] = 1

@kamasutra.message_handler(func=lambda m:"ANAL PLUG" in m.text.upper())
def plug(message):
    global sextoys_selection_passive, passivetoys
    if sextoys_selection_passive == 1:
        passivetoys[1][1] = 1

@kamasutra.message_handler(func=lambda m:"COCK RING" in m.text.upper())
def ring(message):
    global sextoys_selection_passive, passivetoys
    if sextoys_selection_passive == 1:
        passivetoys[2][1] = 1

@kamasutra.message_handler(func=lambda m:"ALL DONE" in m.text.upper())
def allDone(message):
    global sextoys_selection, checkSextoys
    if sextoys_selection == 1:
        checkSextoys = 0

@kamasutra.message_handler(func=lambda m:"LET'S GO" in m.text.upper())
def lesgo(message):
    global sextoys_selection_passive, checkSextoysPassive
    if sextoys_selection_passive == 1:
        checkSextoysPassive = 0

@kamasutra.message_handler(func=lambda m:"<3 <3 <3 <3" in m.text.upper())
def level4(message):
    global difficulty, checkDifficulty, experience
    difficulty = 4
    checkDifficulty = 0
    if experience == 0:
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
    global difficulty, checkDifficulty
    difficulty = 3
    checkDifficulty = 0
    if experience == 0:
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
    global difficulty, checkDifficulty
    difficulty = 2
    checkDifficulty = 0
    if experience == 0:
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
    global difficulty, checkDifficulty
    difficulty = 1
    checkDifficulty = 0
    if experience == 0:
        randomNum = random.randint(1,countFolder("couple/level1"))
        photo = open(fr"couple/level1/{randomNum}.png", "rb")
        text = open(fr"couple/level1/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()

@kamasutra.message_handler(func=lambda m:"BACK TO TIMER" in m.text.upper())
def gobackTimer(message):
    global stop, experience, checkPositions
    checkPositions = 0
    setTimer(message)

@kamasutra.message_handler(func=lambda m:"GO BACK" in m.text.upper())
def goback(message):
    global stop, experience, checkDifficulty 
    stop = 1
    experience = 0
    checkDifficulty = 1
    home(message)

@kamasutra.message_handler(func=lambda m:"CONFIRM TIMER" in m.text.upper())
def confirmTimer(message):
    global checkTimer
    checkTimer = 0
    
@kamasutra.message_handler(func=lambda m:"CONFIRM POSITIONS" in m.text.upper())
def confirmPositions(message):
    global checkPositions, selection
    checkPositions = 0
    selection = 0
    adventure(message)

@kamasutra.message_handler(func=lambda m:"+1 MIN" in m.text.upper())
def add1Time(message):
    global timer, selection
    if selection == 1:
        timer += 1
        kamasutra.send_message(message.chat.id, f"Timer: {timer} minutes")

@kamasutra.message_handler(func=lambda m:"-1 MIN" in m.text.upper())
def remove1Time(message):
    global timer, selection
    if selection == 1:
        if timer > 1:
            timer -= 1
            kamasutra.send_message(message.chat.id, f"Timer: {timer} minutes")
        else:
            kamasutra.send_message(message.chat.id, "Come on, you can last a bit more!")
            kamasutra.send_message(message.chat.id, f"Timer: {timer} minutes")

@kamasutra.message_handler(func=lambda m:"+5 MIN" in m.text.upper())
def add5Time(message):
    global timer, selection
    if selection == 1:
        timer += 5
        kamasutra.send_message(message.chat.id, f"Timer: {timer} minutes")

@kamasutra.message_handler(func=lambda m:"-5 MIN" in m.text.upper())
def remove5Time(message):
    global timer, selection
    if selection == 1:
        if timer > 5:
            timer -= 5
            kamasutra.send_message(message.chat.id, f"Timer: {timer} minutes")
        else:
            kamasutra.send_message(message.chat.id, "Come on, you can last a bit more!")
            kamasutra.send_message(message.chat.id, f"Timer: {timer} minutes")

@kamasutra.message_handler(func=lambda m:"+1 POSITION" in m.text.upper())
def addPosition(message):
    global positions, selection
    if selection == 1:
        positions += 1
        kamasutra.send_message(message.chat.id, f"Positions: {positions}")

@kamasutra.message_handler(func=lambda m:"-1 POSITION" in m.text.upper())
def removePosition(message):
    global positions, selection
    if selection == 1:
        if positions > 1:
            positions -= 1
            kamasutra.send_message(message.chat.id, f"Positions: {positions}")
        else:
            kamasutra.send_message(message.chat.id, "Come on, try at least one position!")
            kamasutra.send_message(message.chat.id, f"Positions: {positions}")

@kamasutra.message_handler(func=lambda m:"START THE ADVENTURE" in m.text.upper())
def startadventure(message):
    global checkAdventure
    checkAdventure = 0
    markup = ReplyKeyboardMarkup()
    next = KeyboardButton("Change")
    stopButton = KeyboardButton("Stop")
    markup.add(next,stopButton)
    kamasutra.send_message(message.chat.id, "Here we go!", reply_markup=markup)

@kamasutra.message_handler(func=lambda m:"RANDOM" in m.text.upper())
def randomPosition(message):
    global experience, activetoys
    if experience == 0:
        randomPartecipants = random.randint(1,3)
        if randomPartecipants == 1:
            randomToy = random.randint(0, len(activetoys)-1)
            folderLen = countFolder(f"single/{activetoys[randomToy][0]}")
            randomNum = random.randint(1, folderLen)
            photo = open(fr"single/{activetoys[randomToy][0]}/{randomNum}.png", "rb")
            text = open(fr"single/{activetoys[randomToy][0]}/{randomNum}.txt", "r")
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

@kamasutra.message_handler(func=lambda m:"CHANGE" in m.text.upper())
def changePosition(message):
    global difficulty, partecipants, activetoys
    if partecipants == 1:
        check = 1
        while check != 0:
            randomToy = random.randint(0, len(activetoys)-1)
            if activetoys[randomToy][1] == 2:
                folderLen = countFolder(f"single/{activetoys[randomToy][0]}")
                randomNum = random.randint(1, folderLen)
                photo = open(fr"single/{activetoys[randomToy][0]}/{randomNum}.png", "rb")
                text = open(fr"single/{activetoys[randomToy][0]}/{randomNum}.txt", "r")
                textt = text.read()
                kamasutra.send_photo(message.chat.id, photo)
                kamasutra.send_message(message.chat.id, textt)
                photo.close()
                text.close()
                check = 0
    if partecipants == 2:
        folderLen = countFolder(f"couple/level{difficulty}")
        randomNum = random.randint(1, folderLen)
        photo = open(fr"couple/level{difficulty}/{randomNum}.png", "rb")
        text = open(fr"couple/level{difficulty}/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()
    if partecipants == 3:
        randomNum = random.randint(1, countFolder("trio"))
        photo = open(rf"trio/{randomNum}.png", "rb")
        text = open(fr"trio/{randomNum}.txt", "r")
        textt = text.read()
        kamasutra.send_photo(message.chat.id, photo)
        kamasutra.send_message(message.chat.id, textt)
        photo.close()
        text.close()

@kamasutra.message_handler(func=lambda m:"STOP" in m.text.upper())
def stopping(message):
    global stop, checkAdventure
    if checkAdventure == 0:
        stop = 1
        home(message)

keep_alive()
kamasutra.polling()