from tkinter import *
from random import *
from tkinter import messagebox




### INITIALISATION ###

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
    #création d'une fenetre
    window = Tk()
    #screenHeight = window.winfo_screenheight()
    window.title("Othello")
    window.update_idletasks()
    window.resizable(width=False, height=False) #emepche resize de la fenetre

    #création d'un canvas ans la fenetre
    global can
    can = Canvas(window, width=400, height=400, bg='black')
    can.pack()

    displayGrid(can)

    window.bind("<Button-1>", onClick)
    window.mainloop()



# création des cases du plateau 
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


### JEU ###    

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
def searchColor(abs, ordo):
        color = board[abs][ordo]["value"]
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



# regarde les coups possible
def checkPlayable():
    playable = FALSE
    shot = {}
    for key, value in board.items():
        k = 1
        while k <= 8:
            if(value[k]["value"] == "green"):

                ### COUP DROIT ###

                #DROITE
                if key != 'H': 
                    right = searchColor(chr(ord(key) + 1), k) 

                    # si case de droite est un pion ennemi
                    if(right != player and right != "green"):
                        nx = chr(ord(key) + 1)
                        nbcase = 0

                        # cherche une case allié a droite sans case verte intermédiaire
                        while(searchColor(nx, k) != player and searchColor(nx, k) != "green" and ord(nx) < ord("H")):
                            nx = chr(ord(nx) + 1)
                            nbcase += 1

                            # repère si la case est allié
                            if searchColor(nx, k) == player:
                                playable = TRUE
                                case = key + str(k)
                                if case in shot:
                                    shot[case] += nbcase
                                else:
                                    shot[case] = nbcase
                                
                                

                #GAUCHE
                if key != 'A': 
                    left = searchColor(chr(ord(key) - 1), k) 
                    if(left != player and left != "green"):
                        nx = chr(ord(key) - 1)
                        nbcase = 0
                        while(searchColor(nx, k) != player and searchColor(nx, k) != "green" and ord(nx) > ord("A")):
                            nx = chr(ord(nx) - 1)
                            nbcase += 1
                            if searchColor(nx, k) == player:
                                playable = TRUE
                                case = key + str(k)
                                if case in shot:
                                    shot[case] += nbcase
                                else:
                                    shot[case] = nbcase                                                           


                #TOP
                if k != 1: 
                    top = searchColor(key, k - 1) 
                    if(top != player and top != "green"):
                        ny = k - 1
                        nbcase = 0
                        while(searchColor(key, ny) != player and searchColor(key, ny) != "green" and ny > 1):
                            ny -= 1
                            nbcase += 1
                            if searchColor(key, ny) == player:
                                playable = TRUE
                                case = key + str(k)
                                if case in shot:
                                    shot[case] += nbcase
                                else:
                                    shot[case] = nbcase
                                

                #BOT
                if k != 8: 
                    bot = searchColor(key, k + 1) 
                    if(bot != player and bot != "green"):
                        ny = k + 1
                        nbcase = 0
                        while(searchColor(key, ny) != player and searchColor(key, ny) != "green" and ny < 8):
                            ny += 1
                            nbcase += 1
                            if searchColor(key, ny) == player:
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
                    botRight = searchColor(chr(ord(key) + 1), k + 1) 

                    # si case en bas a droite est un pion ennemi 
                    if(botRight != player and botRight != "green"):
                        nx = chr(ord(key) + 1)
                        ny = k + 1
                        nbcase = 0


                        # cherche une case allié en diagonale (bas, droite) sans case verte intermédiaire et sans sortir d plateau
                        while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) < ord("H") and ny < 8):
                            nx = chr(ord(nx) + 1)
                            ny += 1
                            nbcase += 1

                            # repère si la case est allié
                            if searchColor(nx, ny) == player:
                                playable = TRUE
                                case = key + str(k)
                                if case in shot:
                                    shot[case] += nbcase
                                else:
                                    shot[case] = nbcase
                                
                
                # BAS GAUACHE
                if key != "A" and k != 8:
                    botLeft = searchColor(chr(ord(key) - 1), k + 1) 
                    if(botLeft != player and botLeft != "green"):
                        nx = chr(ord(key) - 1)
                        ny = k + 1
                        nbcase = 0
                        while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) > ord("A") and ny < 8):
                            nx = chr(ord(nx) - 1)
                            ny += 1
                            nbcase += 1
                            if searchColor(nx, ny) == player:
                                playable = TRUE
                                case = key + str(k)
                                if case in shot:
                                    shot[case] += nbcase
                                else:
                                    shot[case] = nbcase
                                

                # HAUT GAUCHE
                if key != "A" and k != 1:
                    topLeft = searchColor(chr(ord(key) - 1), k - 1) 
                    if(topLeft != player and topLeft != "green"):
                        nx = chr(ord(key) - 1)
                        ny = k - 1
                        nbcase = 0
                        while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) > ord("A") and ny > 1):
                            nx = chr(ord(nx) - 1)
                            ny -= 1
                            nbcase += 1
                            if searchColor(nx, ny) == player:
                                playable = TRUE
                                case = key + str(k)
                                if case in shot:
                                    shot[case] += nbcase
                                else:
                                    shot[case] = nbcase
                                

                # HAUT DROIT
                if key != "H" and k != 1:
                    topRight = searchColor(chr(ord(key) + 1), k - 1) 
                    if(topRight != player and topRight != "green"):
                        nx = chr(ord(key) + 1)
                        ny = k - 1
                        nbcase = 0
                        while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) < ord("H") and ny > 1):
                            nx = chr(ord(nx) + 1)
                            ny -= 1
                            nbcase += 1
                            if searchColor(nx, ny) == player:
                                playable = TRUE
                                case = key + str(k)
                                if case in shot:
                                    shot[case] += nbcase
                                else:
                                    shot[case] = nbcase            
                            
                            
            k += 1


    # si aucun coup possible change de joueur
    if(playable == FALSE):
            switchPlayer()

    return shot


def checkMove(square, actor):
    shot = checkPlayable()
    print("case pour" , player , "=" , shot)
    valid = FALSE
    # vérifie si case pointé est libre
    if(board[square[0]][square[1]]["value"] == "green"):

        ### COUP LIGNE ###

        #ne vérifie pas si case collé au bord droit
        if(ord(square[0]) < ord("H")):
            # couleur de la case de droite
            right = searchColor(chr(ord(square[0]) + 1), square[1]) 

            # si case de droite est un pion ennemi
            if(right != player and right != "green"):
                nx = chr(ord(square[0]) + 1)

                # cherche une case allié a droite sans case verte intermédiaire
                while(searchColor(nx, square[1]) != player and searchColor(nx, square[1]) != "green" and ord(nx) < ord("H")):
                    nx = chr(ord(nx) + 1)

                    # repère si la case est allié
                    if searchColor(nx, square[1]) == player:
                        nnx = chr(ord(square[0]) + 1)
                        valid = TRUE


                        # change la couleur de la case de départ jusqu'a la case allié
                        while searchColor(nnx, square[1]) != player:
                            board[nnx][square[1]]["value"] = player
                            nnx = chr(ord(nnx) + 1)
            
        #GAUCHE
        if(ord(square[0]) > ord("A")):
            left = searchColor(chr(ord(square[0]) - 1), square[1]) 
            if(left != player and left != "green"):
                nx = chr(ord(square[0]) - 1)
                while(searchColor(nx, square[1]) != player and searchColor(nx, square[1]) != "green" and ord(nx) > ord("A")):
                    nx = chr(ord(nx) - 1)
                    if searchColor(nx, square[1]) == player:
                        nnx = chr(ord(square[0]) - 1)
                        valid = TRUE

                        while searchColor(nnx, square[1]) != player:
                            board[nnx][square[1]]["value"] = player
                            nnx = chr(ord(nnx) - 1)

        #HAUT
        if(square[1] > 1):
            top = searchColor(square[0], square[1] - 1) 
            if(top != player and top != "green"):
                ny = square[1] - 1
                while(searchColor(square[0], ny) != player and searchColor(square[0], ny)  != "green" and ny > 1):
                    ny -= 1
                    if searchColor(square[0], ny) == player:
                        nny = square[1]  - 1
                        valid = TRUE
                        while searchColor(square[0], nny) != player:
                            board[square[0]][nny]["value"] = player
                            nny -= 1

        #BAS
        if(square[1] < 8):
            bot = searchColor(square[0], square[1] + 1) 
            if(bot != player and bot != "green"):
                ny = square[1] + 1
                while(searchColor(square[0], ny) != player and searchColor(square[0], ny) != "green" and ny < 8):
                    ny += 1
                    if searchColor(square[0], ny) == player:
                        nny = square[1] + 1
                        valid = TRUE

                        while searchColor(square[0], nny) != player:
                            board[square[0]][nny]["value"] = player
                            nny += 1

        ### COUP DIAGONALE ###

        # BAS DROITE
        if(ord(square[0]) < ord("H") and square[1] < 8):
            # couleur de la case en bas a droite de celle cliqué
            botRight = searchColor(chr(ord(square[0]) + 1), square[1] + 1) 

            # si case en bas a droite est un pion ennemi 
            if(botRight != player and botRight != "green"):
                nx = chr(ord(square[0]) + 1)
                ny = square[1] + 1

                # cherche une case allié en diagonale (bas, droite) sans case verte intermédiaire et sans sortir d plateau
                while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) < ord("H") and ny < 8):
                    nx = chr(ord(nx) + 1)
                    ny += 1

                    # repère si la case est allié
                    if searchColor(nx, ny) == player:
                        nnx = chr(ord(square[0]) + 1)
                        nny = square[1] + 1
                        valid = TRUE

                        # change la couleur de la case de départ jusqu'a la case allié
                        while searchColor(nnx, nny) != player:
                            board[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) + 1)
                            nny += 1

        # BAS GAUCHE
        if(ord(square[0]) > ord("A") and square[1] < 8):
            botLeft = searchColor(chr(ord(square[0]) - 1), square[1] + 1) 
            if(botLeft != player and botLeft != "green"):
                nx = chr(ord(square[0]) - 1)
                ny = square[1] + 1
                while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) > ord("A") and ny < 8):
                    nx = chr(ord(nx) - 1)
                    ny += 1
                    if searchColor(nx, ny) == player:
                        nnx = chr(ord(square[0]) - 1)
                        nny = square[1] + 1
                        valid = TRUE
                        while searchColor(nnx, nny) != player:
                            board[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) - 1)
                            nny += 1

            
        # HAUT GAUCHE
        if(ord(square[0]) > ord("A") and square[1] > 1):
            topLeft = searchColor(chr(ord(square[0]) - 1), square[1] - 1) 
            if(topLeft != player and topLeft != "green"):
                nx = chr(ord(square[0]) - 1)
                ny = square[1] - 1
                while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) > ord("A") and ny > 1):
                    nx = chr(ord(nx) - 1)
                    ny -= 1
                    if searchColor(nx, ny) == player:
                        nnx = chr(ord(square[0]) - 1)
                        nny = square[1] - 1
                        valid = TRUE
                        while searchColor(nnx, nny) != player:
                            board[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) - 1)
                            nny -= 1

        # HAUT DROITE
        if(ord(square[0]) < ord("H") and square[1] > 1):
            topRight = searchColor(chr(ord(square[0]) + 1), square[1] - 1) 
            if(topRight != player and topRight != "green"):
                nx = chr(ord(square[0]) + 1)
                ny = square[1] - 1
                while(searchColor(nx, ny) != player and searchColor(nx, ny) != "green" and ord(nx) < ord("H") and ny > 1):
                    nx = chr(ord(nx) + 1)
                    ny -= 1
                    if searchColor(nx, ny) == player:
                        nnx = chr(ord(square[0]) + 1)
                        nny = square[1] - 1
                        valid = TRUE
                        while searchColor(nnx, nny) != player:
                            board[nnx][nny]["value"] = player
                            nnx = chr(ord(nnx) + 1)
                            nny -= 1



        if(valid):
            board[square[0]][square[1]]["value"] = player
            switchPlayer()
            displayGrid(can)
            checkEnd()
            if(actor == "player"):
                bestMove()
            

            checkPlayable()
    
# event tkinter qui récupère le click de la souris dans la fenêtre
def onClick(event):
    square = searchIndex(event.x, event.y)
    checkMove(square, "player")
    #searchColor(square[0], square[1])


# retourne la clef du dictionnaire en fonction de son index
def getKey(dictionary, n):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 

### HEURISTIQUE ###

# random 
def randomIA():
    shot = checkPlayable()
    print("case pour" , player , "=" , shot)
    shotLen = len(shot)
    if(shotLen >= 0):
        rand = randint(0, shotLen - 1)
        key = getKey(shot, rand)
        x = key[0]
        y = int(key[1])
        square = (x, y)
        print("je vais jouer en", key)
        checkMove(square, "computer")


# meilleur coup 
def bestMove():
    shot = checkPlayable()
    key = max(shot, key=shot.get)
    x = key[0]
    y = int(key[1])
    square = (x, y)
    print("je vais jouer en", key)
    checkMove(square, "computer")


# meilleur coup en fonction du meilleur coup adverse
def bestMoveUp():
    shot = checkPlayable()
    key = max(shot, key=shot.get)
    x = key[0]
    y = int(key[1])
    square = (x, y)
    print("je vais jouer en", key)
    checkMove(square, "computer")


### LANCEMENT ###

def othello():
    initVariable()
    createWindow()
    

othello()
# initVariable()
# checkPlayable()




