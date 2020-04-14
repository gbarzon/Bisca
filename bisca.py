import pygame
import math
import numpy as np
import time
from client_bisca import requestHandler

# define layout constants
global width
global height
width, height = 612, 407
width, height = 2*width, 2*height

global card_wdt
global card_hgt
card_wdt = 120
card_hgt = 180
global card_offset_x
global card_offset_y
card_offset_x = 20
card_offset_y = 250

global puntata_wdt
global puntata_hgt
puntata_wdt = 75
puntata_hgt = 75
global puntata_offset_x
global puntata_offset_y
puntata_offset_x = 20


class Bisca():
    
    def __init__(self):
        pass
        #1
        pygame.init()
        pygame.font.init()
        print("Game initialisation")

        #2
        #initialize the screen
        self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Bisca")
        #3
        #initialize pygame clock
        self.clock=pygame.time.Clock()
        self.initGraphics()
        self.initCards()
        self.request = requestHandler()

        #current state
        #0 -> insert username
        #1 -> insert http
        #2 -> waiting for all the players
        #3 -> current game
        self.currentState=0
        self.hasToSaved=False
        
        self.tempState=False
        self.lastText=''

        self.time = time.time()
        self.dictToSend = None #last saved dict waiting to be sent

        self.askWhoWin = False
        self.stringWhoWin = []
        self.stringWhoLoseLives = []
        self.lastHand = []

        self.userCards = []

        # initialize empty state
        self.puntataClicked=-1
        self.cardClicked=-1
        self.hasStarted=False
        self.text=''
        self.flashes=0

    #UPLOAD IMAGES
    def initGraphics(self):
        self.bckgrnd=pygame.image.load("img/background.jpg")
        self.bckgrnd=pygame.transform.scale(self.bckgrnd, [width, height])
        self.rect=pygame.transform.scale(pygame.image.load("img/rect.png"), [card_wdt, card_hgt])
        self.rect_highlight=pygame.transform.scale(pygame.image.load("img/rect_highlight.jpg"), [card_wdt+10, card_hgt+10])
        self.rect_stripes=pygame.transform.scale(pygame.image.load("img/rect_stripes.jpg"), [card_wdt+10, card_hgt+10])
        self.dashed=pygame.transform.scale(pygame.image.load("img/dashed.png"), [card_wdt, card_hgt])
        self.reddashed=pygame.transform.scale(pygame.image.load("img/red_dashed.jpg"), [card_wdt, card_hgt])
        self.checked=pygame.transform.scale(pygame.image.load("img/checked.png"), [120, 120])
        self.puntata_dashed=pygame.transform.scale(pygame.image.load("img/dashed.png"), [puntata_wdt, puntata_hgt])
        self.puntata_reddashed=pygame.transform.scale(pygame.image.load("img/rect_highlight.jpg"), [puntata_wdt, puntata_hgt])
        self.puntata_checked=pygame.transform.scale(pygame.image.load("img/checked.png"), [puntata_wdt, puntata_hgt])
        self.rect_asso=pygame.transform.scale(pygame.image.load("img/rect_asso.png"), [180, 80])

    def initCards(self):
        semi = ["DENARI", "COPPE", "SPADE", "BASTONI"]
        figure = ["RE", "CAVALLO", "FANTE", "SETTE", "SEI",
                "CINQUE", "QUATTRO", "TRE", "DUE", "ASSO"]
        self.mazzo = [ [i,j] for i in semi for j in figure ]

        self.img_cards = []
        for i,x in enumerate(self.mazzo):
            card = pygame.image.load("carte/"+x[0]+"_"+x[1]+".jpeg")
            card = pygame.transform.scale(card, [card_wdt, card_hgt])
            self.img_cards.append(card)
        
    #0. BACKGROUND     
    def drawBoard(self):
        #Draw background
        self.screen.blit(self.bckgrnd, [0, 0])

        #Draw title
        myfont = pygame.font.SysFont(None, 100)
        titolo = myfont.render("BISCA", 1, (0,0,255))
        wdt = titolo.get_rect().width
        self.screen.blit(titolo, (width/2-wdt/2, 20))

        
    #1. USERNAME
    def drawUsername(self):
        #Draw inserisci
        myfont = pygame.font.SysFont(None, 30)
        text = myfont.render("Inserisci il tuo Username", 1, (255,255,255))
        wdt = text.get_rect().width            
        self.screen.blit(text, (width/2-wdt/2, height/2-20))
        text = myfont.render("Premi Invio per proseguire", 1, (255,255,255))
        wdt = text.get_rect().width          
        self.screen.blit(text, (width/2-wdt/2, height/2))
        #Draw box
        input_box = pygame.Rect(width/2-200, height/2+25, 400, 32)
        color = pygame.Color('dodgerblue2')
        pygame.draw.rect(self.screen, color, input_box, 2)
        #Draw text
        text = myfont.render(self.text, 1, (255,0,0))
        wdt = text.get_rect().width            
        self.screen.blit(text, (width/2-wdt/2, height/2+30))
        #Save username and GoOn
        if self.hasToSaved==True:
            if self.text=='':
                return
            self.userName=self.text
            self.text=''
            self.hasToSaved=False
            self.currentState +=1


    #2. LOGIN
    def drawLogin(self):
        #Draw scritte
        myfont = pygame.font.SysFont(None, 30)
        if self.tempState==False:
            text1 = myfont.render("Benvenuto "+str(self.userName), 1, (255,255,255))
            wdt1 = text1.get_rect().width            
            text2 = myfont.render("Inserisci la formula magica", 1, (255,255,255))
            wdt2 = text2.get_rect().width            
            text3 = myfont.render("Per tentare la sorte premi Invio", 1, (255,255,255))
            wdt3 = text3.get_rect().width            
            text4 = myfont.render("E attendi qualche secondo", 1, (255,255,255))
            wdt4 = text4.get_rect().width            
        else:
            text1 = myfont.render("L'indirizzo "+str(self.lastText)+" non ha funzionato", 1, (255,255,255))
            wdt1 = text1.get_rect().width            
            text2 = myfont.render("Riprova o inserisci un nuovo indirizzo", 1, (255,255,255))
            wdt2 = text2.get_rect().width            
            text3 = myfont.render("Per tentare la sorte premi Invio", 1, (255,255,255))
            wdt3 = text3.get_rect().width            
            text4 = myfont.render("E attendi qualche secondo", 1, (255,255,255))
            wdt4 = text4.get_rect().width
        self.screen.blit(text1, (width/2-wdt1/2, height/2-60))
        self.screen.blit(text2, (width/2-wdt2/2, height/2-20))
        self.screen.blit(text3, (width/2-wdt3/2, height/2))
        self.screen.blit(text4, (width/2-wdt4/2, height/2+20))

        #Draw box
        input_box = pygame.Rect(width/2-200, height/2+50, 400, 32)
        color = pygame.Color('dodgerblue2')
        pygame.draw.rect(self.screen, color, input_box, 2)
        #Draw text
        text = myfont.render(self.text, 1, (255,0,0))
        wdt = text.get_rect().width            
        self.screen.blit(text, (width/2-wdt/2, height/2+55))
        #Draw start botton
        
        #Save username and GoOn
        if self.hasToSaved==True:
            if self.text=='':
                return
            self.time = time.time()
            self.request.insertURL(self.text)
            msgback = self.request.sendRequest({'state':'1','name':self.userName})
            print(msgback)

            if msgback == -1:
                self.tempState=True
                self.lastText = self.text
                self.text = ''
                self.hasToSaved = False
                return
            
            if 'State' in msgback.keys():
                if msgback['State'] == '2':
                    self.text=''
                    self.playersName = msgback['Users'].split(',')
                    self.currentState = 2
                    self.hasToSaved = False
                else:
                    self.handleMsgBack(msgback)

        
    #3. WAITING LIST
    def drawWaitingList(self):
        myfont = pygame.font.SysFont(None, 32)
        text = myfont.render("Attendi l'inizio della partita...", 1, (255,255,255))
        self.screen.blit(text, (50, 120))
        text = myfont.render("Giocatori attualmente collegati:", 1, (255,255,255))
        self.screen.blit(text, (50, 190))
        #Draw players name
        for i,name in enumerate(self.playersName):
            text = myfont.render(name, 1, (255,255,255))
            self.screen.blit(text, (50, 230+i*25))
        #Draw start button
        if self.userName == 'Jack' or self.userName == self.playersName[0]:
            self.screen.blit(self.checked, (width-200, height-200))

        self.waitUntilCanGet({'state':'2', 'user': self.userName})
        

    def startGameClicked(self, mouse):
        if not (self.userName == 'Jack' or self.userName == self.playersName[0]):
            return
        if not self.currentState == 2:
            return
        if mouse[1] > height-200 and mouse[1]< height-80:
            if mouse[0] > width-200 and mouse[0]< width-80:
                self.waitUntilCanGet({'state':'START', 'user': self.userName}, toSave=True)


    # SERVER COMUNICATION AND DICT READING FUNCTIONS
    def handleMsgBack(self, msgback):
        if msgback == -1:
            print('Riprova')
            return
            
        if 'State' in msgback.keys():
            if msgback['State'] == '2':
                self.playersName = msgback['Users'].split(',')
            elif msgback['State'] == '3':
                self.handleDict(msgback)
            elif msgback['State'] == '4':
                self.handleDict(msgback)
            elif msgback['State'] == '99':
                self.handleDict(msgback)
        self.dictToSend = None
        
    def handleDict(self, myDict):
        self.currentState = int(myDict['State'])
        self.playersName = myDict['Users'] #1
        self.n = len(self.playersName)
        self.playersLives = myDict['Lives'] #2
        self.numberOfCards = int(myDict['Ncards']) #3
        self.puntate = myDict['Puntate'] #4
        self.mani = myDict['Mani'] #5
        self.giocate = myDict['Giocate'] #6
        self.current = int(myDict['Current']) #7
        if not self.currentState == 99:
            if 'Usercards' in myDict.keys():
                self.userCards = myDict['Usercards'] #8
        if 'WhoWin' in myDict.keys():
            self.stringWhoWin = myDict['WhoWin']
        if 'WhoLoseLives' in myDict.keys():
            self.stringWhoLoseLives = myDict['WhoLoseLives']
        if 'LastHand' in myDict.keys():
            if not myDict['LastHand'] == self.lastHand:
                self.lastHand = myDict['LastHand']
                self.askWhoWin = True
        if 'Winner' in myDict.keys():
            self.winner = myDict['Winner']

        
    def waitUntilCanGet(self, myDict, toSave=False):
        # qui magari si potrebbe tenere in memoria l'ultimo dict da provare
        # a mandare di nuovo nel caso di fallito GET
        '''
        if not hasattr(self, 'n'):
            N = 7
        else:
            N = self.n -1
        N = 2
        '''
        # limit Nrequest / minute to server
        #reqPerPl = 40 / N #richieste per giocatore
        #timeBtwReq = int(60 / reqPerPl) #tempo tra due richieste
        timeBtwReq = 1.5 #tempo tra due richieste

        if toSave == True:
                print('Save dict to sent')
                self.dictToSend = myDict
                
        now = time.time()
        if not now - self.time > timeBtwReq:
            if not self.dictToSend == None:
                myfont = pygame.font.SysFont(None, 32)
                text = myfont.render("Caricamento...", 1, (255,255,255))
                self.screen.blit(text, (50, 50))
            return
            
        if not (self.dictToSend == None):
            print('Try to send a saved dict')
            myDict = self.dictToSend
        print('Richiesta inviata:')
        print(myDict)
        msgback = self.request.sendRequest(myDict)
        print('Messaggio ricevuto:')
        print(msgback)
        self.handleMsgBack(msgback)
        self.time = now

    
    #4. PUNTATE
    def handlePuntate(self):
        self.drawBank()
        self.drawUserCards()
        self.drawRunningInfo()
        self.drawPuntate()

        #if not self.current == self.playersName.index(self.userName):
        self.waitUntilCanGet({'state':'3', 'user': self.userName})
        
        
    def drawPuntate(self):
        self.drawBank()
        self.drawUserCards()

        #Draw text
        myfont = pygame.font.SysFont(None, 32)
        info = myfont.render("Quante mani punti di vincere?", 1, (255,255,255))
        self.screen.blit(info, (50, 150))

        #Draw box puntate
        n = self.numberOfCards + 1
        
        self.puntate_xs = [None] * n
        x = width/2 + 60 - (n+2)*puntata_wdt/2 - (n+1)/2*puntata_offset_x

        if not self.playersName[self.current] == self.userName:
            return
        
        myfont = pygame.font.SysFont(None, 50)
        # number of players already puntato
        m = len([num for num in self.puntate if num > -1])

        for i in range(n):
            x += puntata_wdt + puntata_offset_x
            self.puntate_xs[i] = x

            if not (m == self.n-1 and i == self.numberOfCards-sum(self.puntate)-1):
                self.screen.blit(self.puntata_dashed, [x, 100])

                number = myfont.render(str(i), 1, (0,0,0))
                wdt = number.get_rect().width
                self.screen.blit(number, (self.puntate_xs[i]+puntata_wdt/2-wdt/2, 125))
        
        if m == self.n-1 and self.puntataClicked == self.numberOfCards-sum(self.puntate)-1:
            return

        if self.puntataClicked > -1:
            self.screen.blit(self.puntata_reddashed, [self.puntate_xs[self.puntataClicked], 100])
            self.screen.blit(self.puntata_checked, (width-200, 100))
            number = myfont.render(str(self.puntataClicked), 1, (0,0,0))
            wdt = number.get_rect().width
            self.screen.blit(number, (self.puntate_xs[self.puntataClicked]+puntata_wdt/2-wdt/2, 125))

    def isPuntataClicked(self, mouse):
        if not self.playersName[self.current] == self.userName:
            return
        
        if mouse[1] < 100 or mouse[1]> 100+puntata_hgt:
            self.puntataClicked = -1
            return
        
        temp = (mouse[0] > np.array(self.puntate_xs))
        temp *= (mouse[0] < np.array(self.puntate_xs) + puntata_wdt)
        n = [i for i, x in enumerate(temp) if x]
        if len(n)==0:
            self.puntataClicked = -1
        else:
            m = len([num for num in self.puntate if num > -1])
            if m == self.n-1 and n[0] == self.numberOfCards-sum(self.puntate)-1:
                self.puntataClicked = -1
            else:
                print("hai cliccato la puntata {0}\n".format(n[0]))
                self.puntataClicked = n[0]

    def isPuntataCheckedClicked(self, mouse):
        if not self.playersName[self.current] == self.userName or self.puntataClicked == -1:
            return
        
        if not self.currentState == 3:
            return
        if mouse[1] > 100 and mouse[1]< 100 + puntata_hgt:
            if mouse[0] > width-200 and mouse[0]< width-200+puntata_wdt:
                myDict = {'state':'3',
                          'user':str(self.userName),
                          'puntata':str(self.puntataClicked)}
                self.waitUntilCanGet(myDict, toSave=True)
                self.puntataClicked = -1

    
    #5. GIOCO
    def handleGioco(self):
        self.drawBank()
        self.drawUserCards()
        self.drawRunningInfo()

        myfont = pygame.font.SysFont(None, 32)
        info = myfont.render("Scegli la tua carta", 1, (255,255,255))
        self.screen.blit(info, (50, 150))
    
        #if not self.current == self.playersName.index(self.userName):
        self.waitUntilCanGet({'state':'4', 'user': self.userName})

        
    def drawUserCards(self):
        n = len(self.userCards)
        myfont = pygame.font.SysFont(None, 32)
        
        if(n<1):
            return
        
        self.card_xs = [None] * n
        x = width/2 - (n+2)*card_wdt/2 - (n+1)/2*card_offset_x
        
        for i in range(n):
            #Draw cards
            x += card_wdt + card_offset_x
            self.card_xs[i] = x
            #self.screen.blit(self.rect, [x, height-card_offset_y])
            index_card = self.mazzo.index(self.userCards[i])
            self.screen.blit(self.img_cards[index_card], [x, height-card_offset_y])

        if self.cardClicked > -1:
            if self.userCards[self.cardClicked] == ['DENARI','ASSO']:
                self.screen.blit(self.rect_asso, (width-200, height-250))
                scritta = myfont.render('VINCERE', 1, (0,0,0))
                wdt = scritta.get_rect().width
                hgt = scritta.get_rect().height
                self.screen.blit(scritta, (width-110-wdt/2, height-215))

                self.screen.blit(self.rect_asso, (width-200, height-150))
                scritta = myfont.render('PERDERE', 1, (0,0,0))
                wdt = scritta.get_rect().width
                hgt = scritta.get_rect().height
                self.screen.blit(scritta, (width-110-wdt/2, height-115))
            else:
                self.screen.blit(self.checked, (width-200, height-200))

            self.screen.blit(self.rect_highlight, [self.card_xs[self.cardClicked]-5, height-card_offset_y-5])
            index_card = self.mazzo.index(self.userCards[self.cardClicked])
            self.screen.blit(self.img_cards[index_card], [self.card_xs[self.cardClicked], height-card_offset_y])


    def drawBank(self, whoWin=False):
        if whoWin == True:
            toDisplay = self.lastHand
        else:
            toDisplay = self.giocate
            
        n = self.n
        
        if(n<1):
            return
        
        myfont32 = pygame.font.SysFont(None, 32)
        myfont26 = pygame.font.SysFont(None, 26)
        myfont = pygame.font.SysFont(None, 32)


        self.bank_xs = [None] * n
        x = width/2 - (n+2)*card_wdt/2 - (n+1)/2*card_offset_x

        self.flashes += 1

        if self.flashes == 40:
            self.flashes = 0
        
        for i in range(n):
            #Draw card
            x += card_wdt + card_offset_x
            self.bank_xs[i] = x

            #Check if card already played or not
            if toDisplay[i] == -1:
                #Card not played yet
                if self.userName in self.playersName:
                    if i == self.playersName.index(self.userName):
                        self.screen.blit(self.rect_highlight, [x-5, height/2-card_offset_y/2-5])
                    else:
                        self.screen.blit(self.dashed, [x, height/2-card_offset_y/2])
                else:
                    self.screen.blit(self.dashed, [x, height/2-card_offset_y/2])
    
                if i == self.current and self.flashes > 20 and whoWin == False:
                    self.screen.blit(self.rect_stripes, [x-5, height/2-card_offset_y/2-5])
            else:
                #Card already played
                if self.userName in self.playersName:
                    if i == self.playersName.index(self.userName):
                        self.screen.blit(self.rect_highlight, [x-5, height/2-card_offset_y/2-5])
                if i == self.current and self.flashes > 20 and whoWin == False:
                    self.screen.blit(self.rect_stripes, [x-5, height/2-card_offset_y/2-5])
                #Print card's name
                index_card = self.mazzo.index(toDisplay[i][:2])
                self.screen.blit(self.img_cards[index_card], [x, height/2-card_offset_y/2])
    
                # Check if asso di denari
                if toDisplay[i] == ['DENARI','ASSO','VINCERE']:
                    scrittaAsso = myfont.render('VINCERE', 1, (0,0,255))
                    wdt = scrittaAsso.get_rect().width
                    self.screen.blit(scrittaAsso, (self.bank_xs[i]+card_wdt/2-wdt/2, height/2-card_offset_y/2+card_hgt/2+50))
                elif toDisplay[i] == ['DENARI','ASSO','PERDERE']:
                    scrittaAsso = myfont.render('PERDERE', 1, (0,0,255))
                    wdt = scrittaAsso.get_rect().width
                    self.screen.blit(scrittaAsso, (self.bank_xs[i]+card_wdt/2-wdt/2, height/2-card_offset_y/2+card_hgt/2+50))

                
            #Draw player name and respective life points
            name = myfont32.render(self.playersName[i], 1, (255,255,255))
            lives = myfont26.render("Vite: "+str(self.playersLives[i]), 1, (255,255,255))
            mani = myfont26.render("Mani vinte: "+str(self.mani[i]), 1, (255,255,255))
            if self.puntate[i] > -1:
                puntate = myfont26.render("Puntata: "+str(self.puntate[i]), 1, (255,255,255))
            else:
                puntate = myfont26.render("Puntata: "+"?", 1, (255,255,255))
                
            self.screen.blit(name, (x+10, height/2-card_offset_y/2-95))
            self.screen.blit(lives, (x+10, height/2-card_offset_y/2-70))
            self.screen.blit(puntate, (x+10, height/2-card_offset_y/2-50))
            #if self.currentState > 3:
            self.screen.blit(mani, (x+10, height/2-card_offset_y/2-30))


    def drawRunningInfo(self):
        myfont = pygame.font.SysFont(None, 32)
        info = myfont.render("E' il turno di: "+self.playersName[self.current], 1, (255,255,255))

        self.screen.blit(info, (50, 120))
        

    def isCardClicked(self,mouse):
        if not self.current == self.playersName.index(self.userName):
            return -1
        
        if mouse[1] < height-card_offset_y or mouse[1]> height-card_offset_y+card_hgt:
            self.cardClicked = -1
            return
        
        temp = (mouse[0] > np.array(self.card_xs))
        temp *= (mouse[0] < np.array(self.card_xs) + card_wdt)
        n = [i for i, x in enumerate(temp) if x]
        if len(n)==0:
            self.cardClicked = -1
        else:
            print("hai cliccato la carta {0}\n".format(n[0]))
            self.cardClicked = n[0]

    def isAssoClicked(self, mouse):
        if not self.playersName[self.current] == self.userName or self.cardClicked == -1:
            return
        if not (self.currentState == 4 and self.userCards[self.cardClicked] == ['DENARI','ASSO']):
            return

        if mouse[0] > width-200 and mouse[0]< width-20:
            if mouse[1] > height-250 and mouse[1]< height-170:
                print('Vincere premuto')
                myDict = {'state':'4',
                          'user':str(self.userName),
                          'carta': self.cardClicked,
                          'asso': 'vincere'}
            elif mouse[1] > height-150 and mouse[1]< height-70:
                print('Perdere premuto')
                myDict = {'state':'4',
                          'user':str(self.userName),
                          'carta': self.cardClicked,
                          'asso': 'perdere'}
                
            self.waitUntilCanGet(myDict, toSave=True)
            self.cardClicked = -1

    def isCardCheckedClicked(self, mouse):
        if not self.playersName[self.current] == self.userName or self.cardClicked == -1:
            return
        
        if not self.currentState == 4:
            return

        if self.userCards[self.cardClicked] == ['DENARI','ASSO']:
            return
        
        if mouse[1] > height-200 and mouse[1]< height-80:
            if mouse[0] > width-200 and mouse[0]< width-80:
                print('Checked premuto')
                myDict = {'state':'4',
                          'user':str(self.userName),
                          'carta': self.cardClicked}
                self.waitUntilCanGet(myDict, toSave=True)
                self.cardClicked = -1

                
    # WHO WIN
    def whoWin(self):
        print('Who win?')
        #self.drawUserCards()
        self.drawBoard()
        self.drawBank(whoWin=True)
        #self.drawRunningInfo()

        print('Chi ha vinto?')
        print(self.stringWhoWin)
        print('Chi ha perso vite?')
        print(self.stringWhoLoseLives)

        myfont = pygame.font.SysFont(None, 32)
        if not self.stringWhoWin == []:
            info = myfont.render(self.stringWhoWin, 1, (255,255,255))
            self.screen.blit(info, (100, height-card_offset_y))
        

        if not self.stringWhoLoseLives == []:
            for i, x in enumerate(self.stringWhoLoseLives):
                info = myfont.render(x, 1, (255,255,255))
                self.screen.blit(info, (width/2-80, height-card_offset_y+30*i))
        self.stringWhoLoseLives = []
        

    #99. END GAME
    def endGame(self):
        self.askWhoWin = False
        self.drawBoard()

        myfont = pygame.font.SysFont(None, 80)
        text = myfont.render(self.winner + ' ha vinto la partita', 1, (0,0,0))
        wdt = text.get_rect().width
        self.screen.blit(text, (width/2-wdt/2, height/2))

        

    #LOOP
    def update(self):
        #sleep to make the game 40 fps
        self.clock.tick(40)
        
        #clear the screen
        self.screen.fill(0)

        #check clicking events
        #TODO: qui potrei definire una funzione handle click che gestisce tutto per i cavoli suoi
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                #print("mouse clicked at position {0}\n".format(mouse))
                #self.cardClicked = self.isCardClicked(mouse)
                if self.currentState == 2:
                    self.startGameClicked(mouse)
                elif self.currentState == 3:
                    self.isPuntataCheckedClicked(mouse)
                    self.isPuntataClicked(mouse)
                elif self.currentState == 4:
                    self.isCardCheckedClicked(mouse)
                    self.isAssoClicked(mouse)
                    self.isCardClicked(mouse)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.hasToSaved=True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    
        #draw the board
        self.drawBoard()
        
        if self.currentState==0:
            self.drawUsername()
            
        elif self.currentState==1:
            self.drawLogin()

        elif self.currentState==2:
            self.drawWaitingList()

        elif self.currentState==3:
            self.handlePuntate()
            
        elif self.currentState==4:
            self.handleGioco()

        elif self.currentState==99:
            if self.askWhoWin:
                self.askWhoWin = False
                self.screen.fill(0)
                self.whoWin()
                pygame.display.flip()
                pygame.event.pump()
                print('Dormo')
                pygame.time.wait(4500)
                print('Mi sveglio')

            self.endGame()
        
        #update the screen
        pygame.display.flip()
        
        if self.askWhoWin:
            self.askWhoWin = False
            self.screen.fill(0)
            self.whoWin()
            pygame.display.flip()
            pygame.event.pump()
            print('Dormo')
            pygame.time.wait(4500)
            print('Mi sveglio')


# MAIN
bg=Bisca()

while 1:
    bg.update()
