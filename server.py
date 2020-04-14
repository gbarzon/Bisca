
# A very simple Flask Hello World app for you to get started with...
from urllib.parse import urlparse
import json
import random
import copy

from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    return 'Ciaaaaaooaooooooo beeeeellllllll'

'''@app.route('/server_bisca')
def home_server():
    return 'Server bisca'
'''

@app.route('/server_bisca', methods=['GET'])
def hello_world():
        if request.method == 'GET':
                print(request)
                query = urlparse(request.url).query
                msg = dict(qc.split("=") for qc in query.split("&"))
                print(type(msg))
                print('Data received from GET:', msg)
                #data = request.json
                #print('Data received from GET:', data)
                #dictBack = myHandler.do_POST(myHandler, data)
                dictBack = myHandler.do_GET(myHandler, msg)
                response = app.response_class(
                        response=json.dumps(dictBack),
                        status=200,
                        mimetype='application/json'
                        )
                return response
        else:
                return 'Server bisca'


class myHandler():

        def startGame(myHandler):
                #Init game State
                random.shuffle(myHandler.users) #1. Randomize players order
                myHandler.n = len(myHandler.users) #Define number of players

                myHandler.playersLives = [3] * myHandler.n #2. Init number of lives
                myHandler.numberOfCards = 5 #3. Define number of cards
                myHandler.puntate = [-1] * myHandler.n #4. Init puntate
                myHandler.mani = [0] * myHandler.n #5. Init number of hands already won
                myHandler.giocate = [-1] * myHandler.n #6. Init cards current played
                myHandler.current = 0 #7. Define current player

                myHandler.stringWhoWin = []
                myHandler.stringWhoLoseLives = []
                myHandler.stringWhoKilled = []
                myHandler.lastHand = []

                myHandler.alreadyPlayed = 0

                myHandler.laststarter = 0
                myHandler.lastNofCards = 5

                myHandler.winner = None

                #Init mazzo
                myHandler.semi = ["DENARI", "COPPE", "SPADE", "BASTONI"]
                myHandler.figure = ["RE", "CAVALLO", "FANTE", "SETTE", "SEI",
                                    "CINQUE", "QUATTRO", "TRE", "DUE", "ASSO"]
                #myHandler.semi = ["DENARI"]
                #myHandler.figure = ["RE", "CAVALLO", "FANTE", "ASSO"]

                myHandler.valori = [ [i,j] for i in myHandler.semi for j in myHandler.figure ]
                myHandler.mazzo = random.sample(myHandler.valori, len(myHandler.valori))

                #Insert special values for Asso di denari
                myHandler.valori.insert(0, ['DENARI','ASSO','VINCERE'])
                myHandler.valori.append(['DENARI','ASSO','PERDERE'])

                #Give cards
                myHandler.giveCards(myHandler)

        def giveCards(myHandler):
                myHandler.mazzo = random.sample(myHandler.mazzo, len(myHandler.mazzo))
                #Give cards
                myHandler.cardsToEachPlayer = [myHandler.mazzo[myHandler.numberOfCards*i:myHandler.numberOfCards*(i+1)] for i in range(myHandler.n)]
                #Add bias as last element
                #So when delete cards, it not lose 1 dimension
                for i in range(myHandler.n):
                        myHandler.cardsToEachPlayer[i].append(['1'])
                print(myHandler.cardsToEachPlayer)
                if myHandler.lastNofCards == 1:
                        myHandler.giocate = myHandler.mazzo[:myHandler.n]
                        myHandler.cardsToEachPlayer = ['1'] * myHandler.n

        def calcolaPunteggio(myHandler):
                vitePerse = [abs(a - b) for a, b in zip(myHandler.puntate, myHandler.mani)]

                for i,x in enumerate(vitePerse):
                        if x==1:
                                myHandler.stringWhoLoseLives.append(str(myHandler.users[i])+' ha perso 1 vita')
                        elif x>1:
                                myHandler.stringWhoLoseLives.append(str(myHandler.users[i])+' ha perso '+str(x) +' vite')

                myHandler.playersLives = [a - b for a, b in zip(myHandler.playersLives, vitePerse)]
                myHandler.killPlayer(myHandler)

        def killPlayer(myHandler):
                # Compute loser
                loser = [i for i, x in enumerate(myHandler.playersLives) if x<1]
                if len(loser) <1 :
                        # no player to kill
                        return
                #Check if pareggio
                if len(loser) == myHandler.n:
                        best = max(myHandler.playersLives)
                        loser = [i for i,x in enumerate(myHandler.playersLives) if not x==best ]
                #Check if end Game
                if len(loser) == myHandler.n-1:
                        myHandler.currentState = 99
                        winnerPos = myHandler.playersLives.index(max(myHandler.playersLives))
                        myHandler.winner = myHandler.users[winnerPos]
                        return
                # Remove loser element from gameState
                for i in loser:
                        myHandler.stringWhoKilled.append(str(myHandler.users[i])+', hai perso')
                myHandler.users = [i for j, i in enumerate(myHandler.users) if j not in loser]
                myHandler.playersLives = [i for j, i in enumerate(myHandler.playersLives) if j not in loser]
                myHandler.n = len(myHandler.users)


        def whoWin(myHandler):
                print('Who win?')
                #Handle asso con una mano
                if myHadler.numberOfCards == 1 and ['DENARI','ASSO'] in myHandler.giocate:
                    userConAsso = myHandler.giocate.index(['DENARI','ASSO'])
                    if myHandler.puntate[userConAsso] == 0:
                        myHandler.giocate[userConAsso] = ['DENARI','ASSO','PERDERE']
                    elif myHandler.puntate[userConAsso] == 1:
                        myHandler.giocate[userConAsso] = ['DENARI','ASSO','VINCERE']
                        
                #Compute winner
                values = [myHandler.valori.index(i) for i in myHandler.giocate]
                winner = values.index(min(values))

                if not (myHandler.lastHand==myHandler.giocate or myHandler.giocate==[-1]*myHandler.n):
                        myHandler.stringWhoWin= str(myHandler.users[winner])+' ha vinto la mano'
                        myHandler.lastHand = myHandler.giocate
                myHandler.mani[winner] += 1 #Add one to hands won
                myHandler.current = winner #7. Reset new starter
                myHandler.giocate = [-1] * myHandler.n #6. Reset giocate
                myHandler.alreadyPlayed = 0 #Reset N already played
                myHandler.numberOfCards -= 1 #3. Subtract one from N of cards
                myHandler.stringWhoLoseLives = []
                print('NofCards: '+str(myHandler.numberOfCards))


        def handleGame(myHandler):
                myHandler.whoWin(myHandler)
                #print('NofCards: '+str(myHandler.numberOfCards))
                if myHandler.numberOfCards == 0:
                        myHandler.calcolaPunteggio(myHandler)
                        if myHandler.currentState == 99:
                                return
                        myHandler.puntate = [-1] * myHandler.n #4. Reset puntate
                        myHandler.mani = [0] * myHandler.n #5. Reset number of hands already won
                        myHandler.giocate = [-1] * myHandler.n #6. Reset giocate
                        myHandler.currentState = 3

                        myHandler.lastNofCards -= 1
                        if myHandler.lastNofCards == 0:
                                myHandler.lastNofCards = 5
                        myHandler.numberOfCards = myHandler.lastNofCards #3. Reset NofCards
                        myHandler.laststarter = (myHandler.laststarter+1) % myHandler.n
                        myHandler.current = myHandler.laststarter

                        myHandler.giveCards(myHandler)


        def generateDict(myHandler,User=None):
                if not User in myHandler.users:
                        User = None

                if myHandler.lastNofCards == 1:
                        print('Carta in testa')
                        i = myHandler.users.index(User)
                        tmp = copy.deepcopy(myHandler.giocate)
                        tmp[i] = -1
                else:
                        tmp = myHandler.giocate

                myHandler.gameState = {
                        'State': str(myHandler.currentState),
                        'Users': myHandler.users, #1
                        'Lives': myHandler.playersLives, #2
                        'Ncards': myHandler.numberOfCards, #3
                        'Puntate': myHandler.puntate, #4
                        'Mani': myHandler.mani, #5
                        'Giocate': tmp, #6
                        'Current': myHandler.current #7
                }

                temp = copy.deepcopy(myHandler.gameState)
                if not User == None:
                        i = myHandler.users.index(User)
                        temp['Usercards'] = myHandler.cardsToEachPlayer[i][:-1]
                else:
                        print('genero dict senza user')
                #if len(myHandler.stringWhoWin) > 0:
                temp['WhoWin'] = myHandler.stringWhoWin
                #if len(myHandler.stringWhoLoseLives) > 0:
                temp['WhoLoseLives'] = myHandler.stringWhoLoseLives
                #if len(myHandler.stringWhoKilled) > 0:
                temp['WhoKilled'] = myHandler.stringWhoKilled
                if len(myHandler.lastHand) > 0:
                        print('Set myHandler.lastHand')
                        temp['LastHand'] = myHandler.lastHand

                if not myHandler.winner == None:
                        temp['Winner'] = myHandler.winner

                return temp


	#Handler for the GET requests
        def do_GET(myHandler, msg):
                if not hasattr(myHandler, 'users'):
                        myHandler.users = []
                if not hasattr(myHandler, 'currentState'):
                        myHandler.currentState = 2


                #print dict request
                #query = urlparse(self.path).query
                #msg = dict(qc.split("=") for qc in query.split("&"))
                print('Dict reveived: ' + str(msg))

                if not 'state' in msg.keys():
                        print('ERROR - State non present in GET request')
                        return

                #Handle username selection
                if msg['state'] == '1':
                    if not myHandler.currentState == 2:
                        return
                        if 'name' in msg.keys():
                                if not (msg['name'] in myHandler.users or len(myHandler.users)>=8):
                                        myHandler.users.append(msg['name'])
                                dictBack = {'State': '2',
                                        'Users': ','.join(myHandler.users)}

                #Handle waiting list
                elif msg['state'] == '2':
                        if myHandler.currentState == 2:
                                dictBack = {'State': '2',
                                'Users': ','.join(myHandler.users)}
                        elif myHandler.currentState == 3:
                                dictBack = myHandler.generateDict(myHandler,msg['user'])

                #Handle Start game
                elif msg['state'] == 'START':
                        myHandler.currentState = 3
                        myHandler.startGame(myHandler)
                        dictBack = myHandler.generateDict(myHandler,msg['user'])
                        print('\n\nTHE GAME IS STARTING\n\n')

                #Handle puntate
                elif msg['state'] == '3':
                        user = msg['user']
                        if user in myHandler.users:
                            if myHandler.puntate[myHandler.users.index(user)] == -1:
                                    if 'puntata' in msg.keys() and myHandler.current == myHandler.users.index(user):
                                        myHandler.puntate[myHandler.users.index(user)] = int(msg['puntata'])
                                        myHandler.alreadyPlayed += 1
                                        if myHandler.alreadyPlayed == myHandler.n:
                                                #Una carta
                                                if myHandler.lastNofCards == 1:
                                                        myHandler.handleGame(myHandler)
                                                else:
                                                # start game
                                                        myHandler.alreadyPlayed = 0
                                                        myHandler.currentState = 4
                                                        myHandler.current = myHandler.laststarter
                                        else:
                                                myHandler.current = (myHandler.current+1) % myHandler.n
                            dictBack = myHandler.generateDict(myHandler, user)
                        else:
                            dictBack = myHandler.generateDict(myHandler)

                #Handle game
                elif msg['state'] == '4':
                        user = msg['user']
                        if user in myHandler.users:
                                i = myHandler.users.index(user)

                                if myHandler.giocate[i] == -1:
                                        if 'carta' in msg.keys() and myHandler.current == i:
                                                carta = myHandler.cardsToEachPlayer[i][int(msg['carta'])]
                                                myHandler.giocate[i] = carta
                                                del myHandler.cardsToEachPlayer[i][int(msg['carta'])]
                                                myHandler.alreadyPlayed += 1
                                                #Handle asso
                                                if 'asso' in msg.keys():
                                                        if msg['asso'] == 'vincere':
                                                                myHandler.giocate[i] = ['DENARI','ASSO','VINCERE']
                                                        elif msg['asso'] == 'perdere':
                                                                myHandler.giocate[i] = ['DENARI','ASSO','PERDERE']
                                                if myHandler.alreadyPlayed == myHandler.n:
                                                        #WHO WIN
                                                        myHandler.handleGame(myHandler)
                                                else:
                                                        myHandler.current = (myHandler.current+1) % myHandler.n
                                dictBack = myHandler.generateDict(myHandler,user)
                        else:
                                dictBack = myHandler.generateDict(myHandler)

                else:
                        dictBack = myHandler.generateDict(myHandler)


                #Send message back
                print('Dict to send back: ', dictBack)
                return dictBack

