#Murder Mystery game
#Randazzo, Michael 2023-3-30
import copy
import random

#-----------------------------CLASSES-----------------------------------------

#Island status
class island:
    def __init__(self):
        self.time = 9 #starting time, 9:00
        self.AMorPM = 'AM' #AM or PM
        self.currentDay=1 #First day
        self.timeString = str(self.time)+':00 '+self.AMorPM

    class timeItself: #time object for alibis and such
        def __init__(self, island, suspects, rooms):
            self.time = island.time
            self.AMorPM = island.AMorPM
            self.currentDay = island.currentDay
            self.timeString = str(self.time)+':00 '+self.AMorPM
            self.suspects = copy.deepcopy(suspects) #list
            self.rooms = copy.deepcopy(rooms)
            
    def setTimeString(self):
        self.timeString = str(self.time)+':00 '+self.AMorPM

    def timeMoves(self): #moves time forward by 1
        self.time+=1
        if (self.time==12): #swaps from AM to PM and vice versa
            if (self.AMorPM=='AM'):
                self.AMorPM='PM'
            elif (self.AMorPM=='PM'):
                self.AMorPM='AM'
                self.currentDay+=1
                print("DAY "+str(self.currentDay)+'\n') #prints new day
        if (self.time==13): #swaps from 12:00 to 1:00
            self.time=1
        self.setTimeString() #set time
        print('The time is now '+self.timeString+'\n')


#Hours of action
class hour:
    def __init__(self, island, suspects, locations):
        self.island = island
        self.suspects = suspects
        self.rooms = locations

    def round(self): #runs through an hour
        self.island.timeMoves()
        for p in self.suspects:
            if p.alive:
                if not p.isCulprit: #will only check murderous intent if subject is not culprit    
                    p.murderousIntent() #sees whether suspect has murderous intent or not
                self.mentalProcess(p)

                if p.player:
                    playerMove(p)
                else:
                    p.moveAbout(None, rooms) #suspect moves

                if p.player: #player character spots another
                    for q in self.suspects:
                        if p.location==q.location and not p==q:
                            self.spottingString(p, q, p.location)
                
                if p.location.hasBody and not p.location.body.Found: #discovering body
                    self.discoveryString(p, p.location.body, p.location)
                    letsDoIt=interrogation(self.suspects, p.location, p.location.body, culp1.getMurderWeapon(), timeyWhimey.getMurderTime())

                    letsDoIt.runThrough() #goes through interrogation
                    p.location.body.Found=True
                    gogo.start=True
        
    
        for p in self.suspects: #searching for weapon
            if p.alive and p.mental < 80 and p.location.hasWeapon and not p.player:
                p.fetchWeapon(p.location.weapon, p.location)
                p.location.hasWeapon=False

        for p in self.suspects:
            if p.alive:
                for q in self.suspects: #going through everyone else in suspect list
                    #if both suspects are in the same room and first suspect has murderous intent
                    if q.location==p.location and p.murderIntent and p.hasWeapon and q.alive and not q.player:
                        if p!=q:
                            murder(p, q, p.weapon)
                            self.mentalProcess(p)
                            p.murderousIntent() #checking murderous intent again
                        elif p==q and p.mental < 20: #succumbs to despair and takes their own life
                            murder(p, p, p.weapon)
        store()
        gogo.go()

        input('>anything to continue')


    def mentalProcess(self, suspect): #mental degradation or advancement
        temp=random.randint(1,3)
        if temp==1: #1/3 chance for recovery
            temp = random.randint(0, 9)
            suspect.mental+=temp
        else: #2/3 chance for degradation
            temp = random.randint(0, 15)
            suspect.mental-=temp


    def moveString(suspect, place): #prints out who's moving if "GM Vision" is enabled
        if gmVision or suspect.player:
            print(suspect.fullname+' moved to '+place.name+'\n')

    def murderString(a, b, c): #prints out murder if GM Vision is enabled
        if gmVision:
            if a==b:
                print(a.fullname+' took their own life with a '+c.name)
            else:
                print(a.fullname+' murdered '+b.fullname+' with a '+c.name+'!\n')

    def discoveryString(self, discoverer, victim, room): #no gm vision since everyone gathers
        print(discoverer.fullname+' found the deceased body of '+victim.fullname+' in '+room.name+'\n')

    def spottingString(self, seer, spotted, room):
        print(seer.fullname+' saw '+spotted.fullname+' in '+room.name)


#finding out the culprit
class interrogation:
    def __init__(self, suspects, murderRoom, victim, weapon, murderTime):
        self.suspects = suspects
        self.murderRoom = murderRoom
        self.victim=victim
        self.weapon = weapon
        self.time=murderTime
        self.culprit = culp1.getCulprit()

    def runThrough(self):
        print('It seems that '+self.victim.fullname+' was murdered by a '+self.weapon.name)
        input(">anything to continue")


        alibis=alibi(self.suspects[0], self.time)
        for p in self.suspects:
            if p.alive:
                alibis=alibi(p, self.time)
                alibis.alibiString()

        print("Who is the culprit? (enter number)")
        for p in self.suspects:
            print(str(self.suspects.index(p))+'. '+p.fullname)
        thought=input()
        if thought==str(self.suspects.index(self.culprit)):
            thought=int(thought)
            print(self.suspects[thought].fullname+' was exiled into the stormy sea, never to be seen again.')
            print('...')
            input('>anything to continue')

            print('But, tensions continue to build.\n')
            self.suspects[thought].alive=False #culprit is gone
            store()
            for p in range (0, 3):
                Rokkenjima.timeMoves()
                store()
        elif thought=='':
            print('dummy text')
        else:
            thought=int(thought)
            print(self.suspects[thought].fullname+' was exiled into the stormy sea, never to be seen again.')
            print('...')
            input('>anything to continue')

            print('But, the true culprit still lurked.\n')
            end=''
            end+='With the group lulled into a false sense of security, the true culprit, '+self.culprit.fullname
            end+=', managed to kill our detective, '+self.suspects[len(self.suspects)-1].fullname+'.'
            end+=' With everyone thrown into panic and paranoia, they soon picked everyone off, one after the other.'
            end+=' Once the storm cleared, they escaped the island. \nThe truth of these impossible murders... would never be fully known.'
            print(end)
            raise SystemExit(0) #game end


#murder attempt
def murder(attacker, victim, weapon):
    victim.alive=False #victim is dead
    weapon.used=True #weapon is now used
    attacker.isCulprit=True #the attacker is now a culprit
    hour.murderString(attacker, victim, weapon)
    victim.location.body=victim
    victim.location.hasBody=True
    temp=timeyWhimey.getCurrentTime()
    timeyWhimey.setMurderTime(temp) #sets murder time
    murderWeapon=weapon
    culp1.setCulprit(attacker)
    culp1.setMurderWeapon(murderWeapon)
    gogo.reset()


#culprit stuff
class culp:
    def __init__(self, culprit, weapon):
        self.culprit=culprit
        self.weapon=weapon

    def setCulprit(self, c):
        self.culprit=c

    def getCulprit(self):
        return self.culprit

    def setMurderWeapon(self, m):
        self.weapon=m

    def getMurderWeapon(self):
        return self.weapon


#waiting for the authorities
class countdown:
    def __init__(self):
        self.start=False
        self.count=0

    def go(self):
        if self.start:
            self.count+=1
            self.rescue()
            if gmVision:
                print(self.count)

    def reset(self):
        self.count=0

    def rescue(self):
        if (self.count > 10 and not culp1.getCulprit().alive) or self.count > 24: #10 hours have passed and culprit has been exiled
            rescue='Eventually, after what felt like years of turmoil, the storm cleared up. '
            rescue+='The authorities arrived on the island soon after, rescuing everyone still alive. \n'
            rescue+='Thus concludes our tale of murder...'
            print(rescue)

            raise SystemExit(0) #game end

            

#Suspects of the island
class suspect:
    def __init__(self, chosenname, familyname):
        self.givenname=chosenname
        self.surname=familyname
        self.fullname=self.givenname+' '+self.surname
        self.isCulprit=False #by default no one is a culprit
        self.alive=True
        useless=room("Entrance")
        self.location=useless
        self.mental = 100
        self.weapon=None
        self.hasWeapon=False
        self.murderIntent=False
        self.Found=False

        self.player=False #is player character

    def setPlayer(self):
        self.player=True

    def setLocation(self, location): #will set current room
        self.location=location

    def fetchWeapon(self, weapon, location): #gets a weapon from the room
        self.weapon = weapon
        weapon.location=None
        self.hasWeapon=True

    def displayInfo(self): #displays all info about a suspect
        print('Name: '+self.fullname)
        print('Location: '+self.location.name)
        if (self.alive):
            status = "ALIVE"
        elif not(self.alive):
            status = "DEAD"
        print('Status: '+status)

    def moveAbout(self, choice, rooms): #suspect moves locations with each passage of time
        check=True
        move=None
        if not self.player:
        
            while check:
                move=rooms[random.randint(0, len(rooms)-1)]
                if move.hasBody and move.murderFound: #less likely to enter room with dead body
                    temp=random.randint(0, 100)
                    if temp>self.mental: #more likely to enter if low mental state
                        self.setLocation(move)
                        check=False
                else:
                    self.setLocation(move)
                    check=False
            hour.moveString(self, move)
        else:
            self.setLocation(choice)
            hour.moveString(self, choice)


    def murderousIntent(self): #checks if suspect has murderous intent
        temp=random.randint(0, 100)
        if (self.mental < temp):
            self.murderIntent=True
        else:
            self.murderIntent=False


#alibi for suspects
class alibi:
    def __init__(self, suspect, time):
        self.suspect=suspect
        self.time=time
        self.pastSelf=None
        #sets past self as suspect's self at given time
        for x in time.suspects:
            if suspect.fullname == x.fullname:
                self.pastSelf=x 

    def alibiString(self): #prints out alibi
        alibiStr=''
        if not self.suspect.isCulprit:
            alibiStr = self.suspect.fullname+' claims that they were in the '
            alibiStr += self.pastSelf.location.name+' at '+self.time.timeString+'.'
            for r in self.time.suspects:
                if r.location==self.pastSelf.location and not r==self.pastSelf:
                    alibiStr+=' They also saw '+r.fullname+' in the '+self.pastSelf.location.name+'.'
            alibiStr+='\n'
        elif self.suspect.isCulprit: #culprit will lie
            alibiStr=''
            peoplePresent=True
            roomNow=None
            for p in rooms:
                for q in self.time.suspects:
                    if q.location!=p: #if there's someone in the same room
                        peoplePresent=False
                        roomNow=p
            if not peoplePresent:
                alibiStr += self.suspect.fullname+ ' claims that they were in the '
                alibiStr += roomNow.name+' at '+self.time.timeString+'.\n'
            else:
                temp=random.randint(0, len(rooms))
                alibiStr += self.suspect.fullname+ ' claims that they were in the '
                alibiStr += rooms(temp)+' at '+self.time.timeString+'.\n'


        print(alibiStr)
        

class weapon:
    def __init__(self, name):
        self.name=name
        self.used=False #unused by default
        #self.lethality=lethal


#Rooms throughout the location
class room:
    def __init__(self, name):
        self.name=name
        self.weapon=None
        #self.peopleInRoom
        self.hasBody=False
        self.murderFound=False #if culprit has been discovered
        self.hasWeapon=False

    def setBody(self, body): #sets dead body
        self.body=body
        self.hasBody=True

    def setWeapon(self, weapon):
        self.weapon=weapon
        self.hasWeapon=True
        

#get time stuff
class timeStuff:
    def __init__(self, timeList):
        self.timeList=timeList
        self.currentTime=timeList[0]
        #self.murderTime=None #time of murder
        self.r=0 #index for time

    def getTimeList(self):
        return timeList

    def getCurrentTime(self):
        return timeList[len(timeList)-1]

    def setMurderTime(self, time):
        self.r=self.timeList.index(time)

    def getMurderTime(self):
        return self.timeList[self.r+1]


#choices for player character
def playerMove(player):
    print("Where do you want to move to? (input number)")
    for p in rooms:
        print(str(rooms.index(p))+'. '+p.name)
    print(str((len(rooms))+1)+'. Check status')
    choice=input()
    for q in rooms:
        if choice==str(rooms.index(q)):
            player.moveAbout(q, rooms)
    if choice==str((len(rooms))+1): #check status
        for p in Suspects:
            print(str(Suspects.index(p))+'. '+p.fullname)
        thought=input()
        for p in Suspects:
            if thought==str(Suspects.index(p)):
                p.displayInfo()


def intro(): #intro for the game
    print("Welcome to the Mystery of Python Island!")
    print("Recently, you have arrived on Somethingsomething Island, a private island owned by a wealthy family from Liechtenstein.")
    print("Unbeknownst to you... murder is just around the corner.")
    print("A number of rumors exist surrounding the Island. Legends of hidden gold, buried biological weapons, lost sacred religious texts, and even rumors of magical gnome servants.")
    print("Any number of things could be a motive for a murder, and something about this island seems to drive people mad... Not to mention, the typhoon keeping their boat from coming back.")
    print()
    print("As our designated Detective, you have the chance to save this group.")
    print("At each hour, you can choose to either move, or analyze another person's status, which can include being dead or alive, and their weapon. This is valuable, but also cuts you off from confirming alibis.")
    print("Whenever a body is found, everyone will be called together. The cause of death will be stated, and then, alibis will be spent out. Only the culprit can lie. Hint: Remember... even the dead could be the culprit!")
    print("Whoever you choose will be placed on a small raft, and exiled out to the stormy sea. If it was the culprit, the game will continue. If the choice was wrong, a massacre will occur.")
    print("If every culprit has been found and no murder occurs for 10 hours, the storm will calm and the authorities will come. If the culprit hasn't been found, but 24 hours have passed, the storm will still clear up.")
    print()
    print("Good luck!")
    input(">anything to continue")

#-----------------------------SETUP-----------------------------------------
Rokkenjima=island()

murderWeapon=weapon('dummy text') #I need this trust me

#Btlr=suspect('Battler','Ushiromiya')
#Jack=suspect('Jack','the Ripper')
#Poirot=suspect('Hercule','Poirot')

Joe=suspect('Joe','Raley')
Matt=suspect('Matt','Cremer')
Doc=suspect('The','Doc')
Jones=suspect('Flavius','Jones')
Lips=suspect('Victor','Lips, Ph.D')
Whooper=suspect('Whooper', '')

Suspects=[Joe,Matt,Doc,Jones,Lips,Whooper]


room1 = room('Parlor')
room2 = room('Kitchen')
room3 = room('Shed')
room4 = room('First Bedroom')
room5 = room('Second Bedroom')
room6 = room('Garden')
rooms = [room1, room2, room3, room4, room5, room6]


w1=weapon('kitchen knife')
weapons = [w1]
weapons.append(weapon('brick'))
weapons.append(weapon('candlestick'))
weapons.append(weapon('pipe bomb'))
weapons.append(weapon('gatling gun'))
weapons.append(weapon('shotgun'))
weapons.append(weapon('gnome servant'))
weapons.append(weapon('rusty spoon'))
weapons.append(weapon('katana'))

for p in rooms: #random weapons in random rooms
    temp=random.randint(0, 7)
    if temp > 0:
        w=random.randint(0, len(weapons)-1)
        p.setWeapon(weapons[w])
        #print(weapons[w].name+' is in '+p.name)
temp=random.randint(0, len(rooms)-1)
rooms[temp].setWeapon(weapons[0])

#Suspects = [Btlr, Jack, Poirot]

firstTime = Rokkenjima.timeItself(Rokkenjima, Suspects, rooms)
timeList = [firstTime]

def store(): #used for updating timeList
    timeList.append(Rokkenjima.timeItself(Rokkenjima, Suspects, rooms))


timeyWhimey=timeStuff(timeList)

#-----------------------------RUNNER-----------------------------------------
gmVision=False
print("Would you like to enable GM Vision? (Input 'Y' or 'N')")
choice=input()
if (choice=='Y'):
    gmVision=True
else:
    gmVision=False
    print("Please input your player character's first name:")
    name1=input()
    print("Please input your player character's last name:")
    name2=input()
    player1=suspect(name1, name2)
    player1.player=True
    Suspects.append(player1)

intro()
culp1=culp(None, None)
gogo=countdown()
runThrough=hour(Rokkenjima, Suspects, rooms)
print("Here is info on every suspect, before game start:")
for p in Suspects:
    p.displayInfo()
input(">anything to continue")
goOn=True
while(goOn):
    runThrough.round()

