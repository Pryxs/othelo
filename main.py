from tkinter import *
from random import *
from tkinter import messagebox
import time
import copy


####################################### 
# 
# INITIALISATION 
#
####################################### 


# initialise les variables du jeu
def initVariable():
    global player 
    global score
    score = {"white" : 2, "black" : 2}
    player = "black"
    createBoard()
    

# création d'un dictionnaire réprésentant le plateau de jeu
def createBoard():
    global board
    board = {}
    i = 65 # A = chr(65) et H = chr(72)
    while i <= 72:
        keyX = chr(i)
        board[keyX] = {}
        i += 1
        k = 1

        while k <= 8:
            board[keyX][k] = {}
            board[keyX][k]["coord"] = createCoord(keyX, k)
            board[keyX][k]["value"] = initColor(keyX, k)
            k += 1


# affecte les bonnes coordonnées (abscisse : x) dans le dictionnaire
def createCoord(keyX, k):
    if(keyX == "A"):
        ordo = createOrdo(k)
        return {"x0" : 0, "x1" : 50, "y0" : ordo["y0"], "y1" : ordo["y1"]}
    elif(keyX == "B"):
        ordo = createOrdo(k)
        return {"x0" : 50, "x1" : 100, "y0" : ordo["y0"], "y1" : ordo["y1"]}
    elif(keyX == "C"):
        ordo = createOrdo(k)
        return {"x0" : 100, "x1" : 150, "y0" : ordo["y0"], "y1" : ordo["y1"]}
    elif(keyX == "D"):
        ordo = createOrdo(k)
        return {"x0" : 150, "x1" : 200, "y0" : ordo["y0"], "y1" : ordo["y1"]}
    elif(keyX == "E"):
        ordo = createOrdo(k)
        return {"x0" : 200, "x1" : 250, "y0" : ordo["y0"], "y1" : ordo["y1"]}
    elif(keyX == "F"):
        ordo = createOrdo(k)
        return {"x0" : 250, "x1" : 300, "y0" : ordo["y0"], "y1" : ordo["y1"]}
    elif(keyX == "G"):
        ordo = createOrdo(k)
        return {"x0" : 300, "x1" : 350, "y0" : ordo["y0"], "y1" : ordo["y1"]}
    elif(keyX == "H"):
        ordo = createOrdo(k)
        return {"x0" : 350, "x1" : 400, "y0" : ordo["y0"], "y1" : ordo["y1"]}


# affecte les bonnes coordonnées (ordonné : y) dans le dictionnaire
def createOrdo(k):
    if(k == 1):
        return {"y0" : 0, "y1" : 50}
    elif(k == 2):
        return {"y0" : 50, "y1" : 100}
    elif(k == 3):
        return {"y0" : 100, "y1" : 150}
    elif(k == 4):
        return {"y0" : 150, "y1" : 200}
    elif(k == 5):
        return {"y0" : 200, "y1" : 250}
    elif(k == 6):
        return {"y0" : 250, "y1" : 300}
    elif(k == 7):
        return {"y0" : 300, "y1" : 350}
    elif(k == 8):
        return {"y0" : 350, "y1" : 400}


# initialise les 4 pions au milieu du plateau 
def initColor(keyX, k):
    if(keyX == "D" and k == 4 or keyX == "E" and k == 5):
        return "white"
    elif(keyX == "D" and k == 5 or keyX == "E" and k == 4):
        return "black"   
    else:
        return "green"


# création du plateau de jeu à l'aide de notre tableau
def createWindow():
    # création d'une fenetre
    window = Tk()
    #screenHeight = window.winfo_screenheight()
    window.title("Othello")
    window.update_idletasks()
    window.resizable(width=False, height=False) #emepche resize de la fenetre

    # création d'un canvas ans la fenetre
    global can
    can = Canvas(window, width=400, height=400, bg='black')
    can.pack()

    # affichage du plateau de jeu
    displayGrid(can)

    # attache un evenement au click
    window.bind("<Button-1>", onClick)
    window.mainloop()


# création des cases du plateau (graphiquement)
def displayGrid(can):
    for key, value in board.items():
        k = 1
        while k <= 8:
            coord = value[k]["coord"]
            color = value[k]["value"]
            x0 = coord["x0"]
            x1 = coord["x1"]
            y0 = coord["y0"]
            y1 = coord["y1"]

            can.create_rectangle(x0, y0, x1, y1, fill=color)
            k += 1


####################################### 
# 
# JEU 
#
#######################################    


# change de joueur
def switchPlayer():
    global player
    if(player == "black"):
        player = "white"
    else:
        player = "black"


# renvoie la case en fonction des coordonnées 
def searchIndex(x, y):
    for key, value in board.items():
        k = 1
        while k <= 8:
            coord = value[k]["coord"]
            if(coord["x0"] <= x <= coord["x1"] and coord["y0"] <= y <= coord["y1"]):
                return(key , k)


            k += 1


# renvoie la couleur de la case demandé
def searchColor(abs, ordo, middleBoard):
        color = middleBoard[abs][ordo]["value"]
        return color


# vérifie quand le jeu prend fin
def checkEnd():
    global score
    w = 0
    b = 0
    for key, value in board.items():
        k = 1
        while k <= 8:
            val = value[k]["value"]
            if(val == "white"):
                w += 1
            elif(val == "black"):
                b += 1          
            k += 1

    score["white"] = w
    score["black"] = b

    if(w + b == 64):
        if(w == b):
            message = "égalité !"
        elif(w > b):
            message = "blanc gagne avec", w ,"points contre" , b
        else:
            message = "noir gagne avec", b ,"points contre" , w

        messagebox.showinfo("Fin du jeu", message)
        initVariable()
        displayGrid(can)


# regarde les coups possible selon un tableau de jeu et un joueur hypothetique
def checkPlayable(middleBoard, middlePlayer):
    playable = FALSE
    shot = {}
    if(middleBoard):
        for key, value in middleBoard.items():
            k = 1
            while k <= 8:
                if(value[k]["value"] == "green"):

                    ### COUP DROIT ###

                    #DROITE
                    if key != 'H': 
                        right = searchColor(chr(ord(key) + 1), k, middleBoard) 

                        # si case de droite est un pion ennemi
                        if(right != middlePlayer and right != "green"):
                            nx = chr(ord(key) + 1)
                            nbcase = 0

                            # cherche une case allié a droite sans case verte intermédiaire
                            while(searchColor(nx, k, middleBoard) != middlePlayer and searchColor(nx, k, middleBoard) != "green" and ord(nx) < ord("H")):
                                nx = chr(ord(nx) + 1)
                                nbcase += 1

                                # repère si la case est allié
                                if searchColor(nx, k, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase
                                    
                                    

                    #GAUCHE
                    if key != 'A': 
                        left = searchColor(chr(ord(key) - 1), k, middleBoard) 
                        if(left != middlePlayer and left != "green"):
                            nx = chr(ord(key) - 1)
                            nbcase = 0
                            while(searchColor(nx, k, middleBoard) != middlePlayer and searchColor(nx, k, middleBoard) != "green" and ord(nx) > ord("A")):
                                nx = chr(ord(nx) - 1)
                                nbcase += 1
                                if searchColor(nx, k, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase                                                           


                    #TOP
                    if k != 1: 
                        top = searchColor(key, k - 1, middleBoard) 
                        if(top != middlePlayer and top != "green"):
                            ny = k - 1
                            nbcase = 0
                            while(searchColor(key, ny, middleBoard) != middlePlayer and searchColor(key, ny, middleBoard) != "green" and ny > 1):
                                ny -= 1
                                nbcase += 1
                                if searchColor(key, ny, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase
                                    

                    #BOT
                    if k != 8: 
                        bot = searchColor(key, k + 1, middleBoard) 
                        if(bot != middlePlayer and bot != "green"):
                            ny = k + 1
                            nbcase = 0
                            while(searchColor(key, ny, middleBoard) != middlePlayer and searchColor(key, ny, middleBoard) != "green" and ny < 8):
                                ny += 1
                                nbcase += 1
                                if searchColor(key, ny, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase
                                    

                    ### COUP DIAGONALE ###

                    # BAS DROITE
                    if key != "H" and k != 8:
                        # couleur de la case en bas a droite de celle cliqué
                        botRight = searchColor(chr(ord(key) + 1), k + 1, middleBoard) 

                        # si case en bas a droite est un pion ennemi 
                        if(botRight != middlePlayer and botRight != "green"):
                            nx = chr(ord(key) + 1)
                            ny = k + 1
                            nbcase = 0


                            # cherche une case allié en diagonale (bas, droite) sans case verte intermédiaire et sans sortir d plateau
                            while(searchColor(nx, ny, middleBoard) != middlePlayer and searchColor(nx, ny, middleBoard) != "green" and ord(nx) < ord("H") and ny < 8):
                                nx = chr(ord(nx) + 1)
                                ny += 1
                                nbcase += 1

                                # repère si la case est allié
                                if searchColor(nx, ny, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase
                                    
                    
                    # BAS GAUACHE
                    if key != "A" and k != 8:
                        botLeft = searchColor(chr(ord(key) - 1), k + 1, middleBoard) 
                        if(botLeft != middlePlayer and botLeft != "green"):
                            nx = chr(ord(key) - 1)
                            ny = k + 1
                            nbcase = 0
                            while(searchColor(nx, ny, middleBoard) != middlePlayer and searchColor(nx, ny, middleBoard) != "green" and ord(nx) > ord("A") and ny < 8):
                                nx = chr(ord(nx) - 1)
                                ny += 1
                                nbcase += 1
                                if searchColor(nx, ny, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase
                                    

                    # HAUT GAUCHE
                    if key != "A" and k != 1:
                        topLeft = searchColor(chr(ord(key) - 1), k - 1, middleBoard) 
                        if(topLeft != middlePlayer and topLeft != "green"):
                            nx = chr(ord(key) - 1)
                            ny = k - 1
                            nbcase = 0
                            while(searchColor(nx, ny, middleBoard) != middlePlayer and searchColor(nx, ny, middleBoard) != "green" and ord(nx) > ord("A") and ny > 1):
                                nx = chr(ord(nx) - 1)
                                ny -= 1
                                nbcase += 1
                                if searchColor(nx, ny, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase
                                    

                    # HAUT DROIT
                    if key != "H" and k != 1:
                        topRight = searchColor(chr(ord(key) + 1), k - 1, middleBoard) 
                        if(topRight != middlePlayer and topRight != "green"):
                            nx = chr(ord(key) + 1)
                            ny = k - 1
                            nbcase = 0
                            while(searchColor(nx, ny, middleBoard) != middlePlayer and searchColor(nx, ny, middleBoard) != "green" and ord(nx) < ord("H") and ny > 1):
                                nx = chr(ord(nx) + 1)
                                ny -= 1
                                nbcase += 1
                                if searchColor(nx, ny, middleBoard) == middlePlayer:
                                    playable = TRUE
                                    case = key + str(k)
                                    if case in shot:
                                        shot[case] += nbcase
                                    else:
                                        shot[case] = nbcase            
                                
                                
                k += 1

    # si aucun coup possible change de joueur
    #if(playable == FALSE):
        # switchPlayer()

    return shot


# regarde si le coup envisagé est possible et retourne le plateau de jeu modifié
def checkMove(square):

    ### ATTENTION ###

    #middleBoard = board    LIE LES DEUX PAS DIFFERENTE INSTANCE, IL NE SONT PAS INDEPENDANT

    ### ATTENTION ###

    middleBoard = copy.deepcopy(board)
    # print("case pour" , player , "=" , shot)
    valid = FALSE

    # vérifie si case pointé est libre
    if(middleBoard[square[0]][square[1]]["value"] == "green"):

        ### COUP LIGNE ###

        # ne vérifie pas si case collé au bord droit
        if(ord(square[0]) < ord("H")):
            # couleur de la case de droite
            right = searchColor(chr(ord(square[0]) + 1), square[1], middleBoard) 

            # si case de droite est un pion ennemi
            if(right != player and right != "green"):
                nx = chr(ord(square[0]) + 1)

                # cherche une case allié a droite sans case verte intermédiaire
                while(searchColor(nx, square[1], middleBoard) != player and searchColor(nx, square[1], middleBoard) != "green" and ord(nx) < ord("H")):
                    nx = chr(ord(nx) + 1)

                    # repère si la case est allié
                    if searchColor(nx, square[1], middleBoard) == player:
                        nnx = chr(ord(square[0]) + 1)
                        valid = TRUE


                        # change la couleur de la case de départ jusqu'a la case allié
                        while searchColor(nnx, square[1], middleBoard) != player:
                            middleBoard[nnx][square[1]]["value"] = player
                            nnx = chr(ord(nnx) + 1)
            
        #GAUCHE
        if(ord(square[0]) > ord("A")):
            left = searchColor(chr(ord(square[0]) - 1), square[1], middleBoard) 
            if(left != player and left != "green"):
                nx = chr(ord(square[0]) - 1)
                while(searchColor(nx, square[1], middleBoard) != player and searchColor(nx, square[1], middleBoard) != "green" and ord(nx) > ord("A")):
                    nx = chr(ord(nx) - 1)
                    if searchColor(nx, square[1], middleBoard) == player:
                        nnx = chr(ord(square[0]) - 1)
                        valid = TRUE

                        while searchColor(nnx, square[1], middleBoard) != player:
                            middleBoard[nnx][square[1]]["value"] = player
                            nnx = chr(ord(nnx) - 1)

        #HAUT
        if(square[1] > 1):
            top = searchColor(square[0], square[1] - 1, middleBoard) 
            if(top != player and top != "green"):
                ny = square[1] - 1
                while(searchColor(square[0], ny, middleBoard) != player and searchColor(square[0], ny, middleBoard)  != "green" and ny > 1):
                    ny -= 1
                    if searchColor(square[0], ny, middleBoard) == player:
                        nny = square[1]  - 1
                        valid = TRUE
                        while searchColor(square[0], nny, middleBoard) != player:
                            middleBoard[square[0]][nny]["value"] = player
                            nny -= 1

        #BAS
        if(square[1] < 8):
            bot = searchColor(square[0], square[1] + 1, middleBoard) 
            if(bot != player and bot != "green"):
                ny = square[1] + 1
                while(searchColor(square[0], ny, middleBoard) != player and searchColor(square[0], ny, middleBoard) != "green" and ny < 8):
                    ny += 1
                    if searchColor(square[0], ny, middleBoard) == player:
                        nny = square[1] + 1
                        valid = TRUE

                        while searchColor(square[0], nny, middleBoard) != player:
                            middleBoard[square[0]][nny]["value"] = player
                            nny += 1

        ### COUP DIAGONALE ###

        # BAS DROITE
        if(ord(square[0]) < ord("H") and square[1] < 8):
            # couleur de la case en bas a droite de celle cliqué
            botRight = searchColor(chr(ord(square[0]) + 1), square[1] + 1, middleBoard) 

            # si case en bas a droite est un pion ennemi 
            if(botRight != player and botRight != "green"):
                nx = chr(ord(square[0]) + 1)
                ny = square[1] + 1

                # cherche une case allié en diagonale (bas, droite) sans case verte intermédiaire et sans sortir d plateau
                while(searchColor(nx, ny, middleBoard) != player and searchColor(nx, ny, middleBoard) != "green" and ord(nx) < ord("H") and ny < 8):
                    nx = chr(ord(nx) + 1)
                    ny += 1

                    # repère si la case est allié
                    if searchColor(nx, ny, middleBoard) == player:
                        nnx = chr(ord(square[0]) + 1)
                        nny = square[1] + 1
                        valid = TRUE

                        # change la couleur de la case de départ jusqu'a la case allié
                        while searchColor(nnx, nny, middleBoard) != player:
                            middleBoard[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) + 1)
                            nny += 1

        # BAS GAUCHE
        if(ord(square[0]) > ord("A") and square[1] < 8):
            botLeft = searchColor(chr(ord(square[0]) - 1), square[1] + 1, middleBoard) 
            if(botLeft != player and botLeft != "green"):
                nx = chr(ord(square[0]) - 1)
                ny = square[1] + 1
                while(searchColor(nx, ny, middleBoard) != player and searchColor(nx, ny, middleBoard) != "green" and ord(nx) > ord("A") and ny < 8):
                    nx = chr(ord(nx) - 1)
                    ny += 1
                    if searchColor(nx, ny, middleBoard) == player:
                        nnx = chr(ord(square[0]) - 1)
                        nny = square[1] + 1
                        valid = TRUE
                        while searchColor(nnx, nny, middleBoard) != player:
                            middleBoard[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) - 1)
                            nny += 1

            
        # HAUT GAUCHE
        if(ord(square[0]) > ord("A") and square[1] > 1):
            topLeft = searchColor(chr(ord(square[0]) - 1), square[1] - 1, middleBoard) 
            if(topLeft != player and topLeft != "green"):
                nx = chr(ord(square[0]) - 1)
                ny = square[1] - 1
                while(searchColor(nx, ny, middleBoard) != player and searchColor(nx, ny, middleBoard) != "green" and ord(nx) > ord("A") and ny > 1):
                    nx = chr(ord(nx) - 1)
                    ny -= 1
                    if searchColor(nx, ny, middleBoard) == player:
                        nnx = chr(ord(square[0]) - 1)
                        nny = square[1] - 1
                        valid = TRUE
                        while searchColor(nnx, nny, middleBoard) != player:
                            middleBoard[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) - 1)
                            nny -= 1

        # HAUT DROITE
        if(ord(square[0]) < ord("H") and square[1] > 1):
            topRight = searchColor(chr(ord(square[0]) + 1), square[1] - 1, middleBoard) 
            if(topRight != player and topRight != "green"):
                nx = chr(ord(square[0]) + 1)
                ny = square[1] - 1
                while(searchColor(nx, ny, middleBoard) != player and searchColor(nx, ny, middleBoard) != "green" and ord(nx) < ord("H") and ny > 1):
                    nx = chr(ord(nx) + 1)
                    ny -= 1
                    if searchColor(nx, ny, middleBoard) == player:
                        nnx = chr(ord(square[0]) + 1)
                        nny = square[1] - 1
                        valid = TRUE
                        while searchColor(nnx, nny, middleBoard) != player:
                            middleBoard[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) + 1)
                            nny -= 1



        if(valid):
            middleBoard[square[0]][square[1]]["value"] = player
            return middleBoard

    

# concretise le coup et prend en paramètre un tableau de jeu ainsi qu'un acteuer (joueur)
def activeBoard(middleBoard, actor):

    # modifie le tableau de jeu
    if(middleBoard):
        global board
        board = middleBoard

    # affiche la grille selon le nouveau tableau de jeu
    displayGrid(can)

    # change de joueur
    switchPlayer()

    # on regarde si le jeu prend fin
    checkEnd()

    # pour versus humain/machine on donne le jeu a l'ordinateur
    if(actor == "player"):
        bestMove(False)

    
    # checkPlayable(board, player)


# event tkinter qui récupère le click de la souris dans la fenêtre
def onClick(event):
    # human(event.x, event.y)
    # vs()
    stats()

# retourne la clef du dictionnaire en fonction de son index
def getKey(dictionary, n):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 


####################################### 
# 
# HEURISTIQUE 
#
####################################### 


# random heuristique (génère un index du tableau des coups possible) 
def randomIA():
    print("---------------------")
    print("Random")
    print("---------------------")
    shot = checkPlayable(board, player)
    print("case pour" , player , "=" , shot)

    if(len(shot) > 0):
        shotLen = len(shot)
        rand = randint(0, shotLen - 1)
        key = getKey(shot, rand)
        x = key[0]
        y = int(key[1])
        square = (x, y)
        print("je vais jouer en", key)
        middleBoard = checkMove(square)   
        activeBoard(middleBoard, "player")
    else:
        activeBoard(board, "player")


# heuristique du meilleur coup (joue la case retournant le plus de pions)
# paramètre => boolean qui définit si meilleur coup aléatoire ou toujours le premier 
def bestMove(random):
    print("---------------------")
    print("BestMove")
    print("---------------------")
    shot = checkPlayable(board, player)
    print("case pour" , player , "=" , shot)

    # si coup possible
    if(shot):
        # si on active effet aléatoire, on choisit un coup random parmis les meilleurs coups
        if(random == True):
            key = getKey(shot, 0)
            current = (key, shot[key])

            for key, value in shot.items():
                if value > current[1]:
                    current = (key, value)

                # random si meme coup
                elif value == current[1]:
                    rand = randint(0, 1)
                    if(rand == 1):
                        current = (key, value)

            key = current[0]

        else:
            key = max(shot, key=shot.get)


        x = key[0]
        y = int(key[1])
        square = (x, y)
        print("je suis", player, " et je vais jouer en", key)
        middleBoard = checkMove(square)
        activeBoard(middleBoard, "computer")

    # si pas de coup possible on passe tour
    else:
        activeBoard(board, "computer")


# meilleur coup en fonction du meilleur coup adverse
# paramètre => boolean qui définit si meilleur coup aléatoire ou toujours le premier 
def bestMoveUp(random):
    print("---------------------")
    print("BestMoveUp")
    print("---------------------")
    shot = checkPlayable(board, player)
    bestValue = -100 # initialise très basse valeur car des coups peuvent avoir un impacte négatif
    bestShot = tuple()
    print("case pour" , player , "=" , shot)

    # si je peux jouer, pour tout les coups possible on génère un tableau de jeu 
    if(shot):
        for key, value in shot.items():
            square = (key[0], int(key[1]))
            middleBoard = checkMove(square)
            if(player == "white"):
                middleShot = checkPlayable(middleBoard, "black")
            else:
                middleShot = checkPlayable(middleBoard, "white")


            # pour tout les coups possible ennemi de notre tableau de jeu hypothètique on fait le poids des pions 
            # pions que je gagne - pions que je perds 
            if(middleShot):
                print(middleShot)
                for middleKey, middleValue in middleShot.items():
                    maxMiddleValueKey = max(middleShot, key=middleShot.get)
                    maxMiddleValue = middleShot[maxMiddleValueKey]
                    interValue = value - maxMiddleValue
                    if(interValue > bestValue):
                        bestValue = interValue
                        bestShot = square
                    if(random == True):
                        if(interValue == bestValue):
                            rand = randint(0, 1)
                            if(rand == 1):
                                bestValue = interValue
                                bestShot = square

            else:
                bestShot = square
    

        print("je suis", player, " et je vais jouer en", bestShot)
        middleBoard = checkMove(bestShot)
        activeBoard(middleBoard, "computer")

    # si je peux pas jouer je apsse tour
    else:
        activeBoard(board, "computer")


####################################### 
# 
# DEMO  
#
####################################### 


# joue un humain vs machine (nécessite modification activeBoard())
def human(x, y):
    square = searchIndex(x, y)
    middleBoard = checkMove(square)
    if(middleBoard):
        activeBoard(middleBoard, "player")


# joue deux heuristique
def vs():
    while score["black"] + score["white"] != 64:
        bestMoveUp(True)
        bestMove(True)


# joue un certain nombre de partie et regarde les resultats
def stats():
    k = 0
    white = 0
    black = 0
    equal = 0
    while k < 10:
        equality = checkEqual()
        if score["black"] + score["white"] != 64 and equality:
            bestMoveUp(True)
            bestMove(True)
            print(score)
        else:
            if score["black"] == score["white"]:
                equal += 1
            elif score["black"] > score["white"]:
                black += 1
            else:
                white += 1

            k += 1
            initVariable()
            displayGrid(can)
        
    print("white : ", white)
    print("black : ", black)
    print("egalite :", equal)


# regarde si aucun joueur ne peux joeur
def checkEqual():
    if(checkPlayable(board, "white") and (checkPlayable(board, "black"))):
        return True
    else:
        return False
    

####################################### 
# 
# DEBUG 
#
####################################### 


# affiche toutes les cases du jeu et leur valeur 
def debugBord(board):
    for key, value in board.items():
        k = 1
        while k <= 8:
            case = (key, k)
            if(value[k]["value"] != "green"):
                print(case, value[k]["value"])
            k += 1


####################################### 
# 
# LANCEMENT 
#
####################################### 


# initialise le jeu (jeu se lance au clique)
def othello():
    initVariable()
    createWindow()
    

othello()





