import random
import copy

def listValidMoves(board,player):
    possibleMoves=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        moveRowInc=-1
    else:
        playerTokens=["r","R"]
        moveRowInc=1
    kingTokens=["B","R"]
    for row in range(8): #For every row
        for col in range(8):  #For every square in a row
            if board[row][col] in playerTokens: #If the board contains either a regular or king checker of the given player
                if board[row][col] not in kingTokens: #if checker is NOT a king
                    for colInc in [-1,1]: #for each diagonal square in the correct row direction
                        if row+moveRowInc in validRange and col+colInc in validRange and board[row+moveRowInc][col+colInc] =='e':
                            possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+moveRowInc)+str(col+colInc))
                else:  #checker is a king
                    for rowInc in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]: #for each diagonal square in each row direction
                            if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] =='e':
                                possibleMoves.append(chr(row+65)+str(col)+":"+chr(row+65+rowInc)+str(col+colInc))              
    return possibleMoves



def listSingleJumps(board,player):
    possibleSingleJumps=[]
    validRange=[0,1,2,3,4,5,6,7] #list(range(8))
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        enemyTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        enemyTokens=["b","B"]
    kingTokens=["B","R"]
    for row in range(8):
        for col in range(8):
            if board[row][col] in playerTokens:
                if board[row][col] not in kingTokens:  #if checker is NOT a king
                    for colInc in [-1,1]:
                        if row+rowInc in validRange and col+colInc in validRange and board[row+rowInc][col+colInc] in enemyTokens:                        
                            colJumpInc=2 * colInc
                            rowJumpInc=2 * rowInc
                            if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
                else: #checker is a king
                    for rowIncs in [-1,1]: #for each row direction (forward and backward)
                        for colInc in [-1,1]:
                            if row+rowIncs in validRange and col+colInc in validRange and board[row+rowIncs][col+colInc] in enemyTokens:                        
                                colJumpInc=2 * colInc
                                rowJumpInc=2 * rowIncs
                                if row+rowJumpInc in validRange and col + colJumpInc in validRange and board[row+rowJumpInc][col+colJumpInc]=="e":
                                    possibleSingleJumps.append(chr(row+65)+str(col)+":"+chr(row+65+rowJumpInc)+str(col+colJumpInc))
    return possibleSingleJumps

def listMultipleJumps(board,player,jumpsList):
    newJumps=expandJumps(board,player,jumpsList)
    while newJumps != jumpsList:
        jumpsList=newJumps[:]
        newJumps=expandJumps(board,player,jumpsList)
    return newJumps


def expandJumps(board,player,oldJumps):
    INCs=[1,-1]
    VALID_RANGE=[0,1,2,3,4,5,6,7]
    if player=="b":
        playerTokens=["b","B"]
        rowInc=-1
        opponentTokens=["r","R"]
    else:
        playerTokens=["r","R"]
        rowInc=1
        opponentTokens=["b","B"]
    newJumps=[]
    for oldJump in oldJumps:
        row=ord(oldJump[-2])-65
        col=int(oldJump[-1])
        newJumps.append(oldJump)
        startRow=ord(oldJump[0])-65
        startCol=int(oldJump[1])
        if board[startRow][startCol] not in ["R","B"]: #not a king
            for colInc in INCs:
                jumprow=row+rowInc
                jumpcol=col+colInc
                torow=row+2*rowInc
                tocol=col+2*colInc
                if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                and board[jumprow][jumpcol] in opponentTokens and board[torow][tocol]=='e':
                    newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                    if oldJump in newJumps:
                        newJumps.remove(oldJump)
        else: #is a king
            for colInc in INCs:
                for newRowInc in INCs:
                    jumprow=row+newRowInc
                    jumpcol=col+colInc
                    torow=row+2*newRowInc
                    tocol=col+2*colInc
                    if jumprow in VALID_RANGE and jumpcol in VALID_RANGE and torow in VALID_RANGE and tocol in VALID_RANGE \
                    and board[jumprow][jumpcol] in opponentTokens and (board[torow][tocol]=='e' or oldJump[0:2]==chr(torow+65)+str(tocol)) \
                    and ((oldJump[-2:]+":"+chr(torow+65)+str(tocol)) not in oldJump) and ((chr(torow+65)+str(tocol)+':'+oldJump[-2:] not in oldJump)) and (chr(torow+65)+str(tocol)!=oldJump[-5:-3]):
                        newJumps.append(oldJump+":"+chr(torow+65)+str(tocol))
                        if oldJump in newJumps:
                            newJumps.remove(oldJump)
    return newJumps          

def findCrownRowMovesOrJumps(board,player,movesList):
    kingingList=[]
    for move in movesList:
        FROM=move[0:2]
        FROMRow=ord(FROM[0])-65
        FROMCol=int(FROM[1])
        TO=move[-2:]
        TORow=TO[0]
        if player=="r":
            kingRow="H"
        else:
            kingRow="A"
        if board[FROMRow][FROMCol]==player and TORow==kingRow:
            kingingList.append(move)
            movesList=movesList[:movesList.index(move)]+movesList[movesList.index(move)+1:]
    return kingingList
    
def findBlockingMoves(playerBlockingMove, enemyMoveBlocked):
    # works for both moves and jumps
    blockMovesList = []
    for jump in playerBlockingMove:
        for move in enemyMoveBlocked:
            if jump[-2:] in move:
                blockMovesList.append(jump)
    return blockMovesList

def placeCheckerLogical(TORow,TOCol,board,playerToken):
    #Logical board update first
    if playerToken == "r" and TORow==7:  #if a kinging move for red
        board[TORow][TOCol]=playerToken.upper()
    elif playerToken == "b" and TORow==0: #if a kinging move for black
        board[TORow][TOCol]=playerToken.upper()
    else: #all non-kinging moves place checker in logical board
        board[TORow][TOCol]=playerToken

def findLongestJump(jumpsList): # Function designed to opt for multiple jumps first
    countIndexes = []
    for jump in jumpsList:
        countIndexes.append(jump.count(':'))
    maxIndex = index(max(countIndexes))
    return jumpsList[maxIndex]

def parseMove(move):
    FROM=move[0:2]
    FROMRow=ord(FROM[0])-65
    FROMCol=int(FROM[1])
    TO=move[3:5]
    TORow=ord(TO[0])-65
    TOCol=int(TO[1])
    return FROMRow,FROMCol,TORow,TOCol

def findSuicideMoves(board, movesList, player, enemyPlayer):
    suicideMoves = []
    newBoard = copy.deepcopy(board)
    for move in movesList:
        moveCopy = move[:]
        moveFROMRow, moveFROMCol, moveTORow, moveTOCol = parseMove(move)
        isMove = abs(moveFROMCol - moveTOCol) > 1
        if isMove: # process the move and check for enemy jumps resulting from said move
            newBoard[moveFROMRow][moveFROMCol] = 'e'
            placeCheckerLogical(moveTORow, moveTOCol, newBoard, player)
        else:
            reps = moveCopy.count(':')
            for i in range(reps):
                moveFROMRow, moveFROMCol, moveTORow, moveTOCol = parseMove(moveCopy)
                newBoard[moveTORow][moveTOCol] = 'e'
                placeCheckerLogical(moveTORow, moveTOCol, newBoard, player)
                newBoard[(moveFROMRow+moveTORow)//2][(moveFROMCol+moveTOCol)//2] = 'e'
                moveCopy = move[3:]
        enemyJumpsList = listSingleJumps(newBoard, enemyPlayer)
        enemyJumpsList = listMultipleJumps(newBoard, enemyPlayer, enemyJumpsList)
        moveFROMRow, moveFROMCol, moveTORow, moveTOCol = parseMove(move)
        for enemyJump in enemyJumpsList:
            numPairs = enemyJump.count(':')
            for i in range(0, numPairs*3, 3):
                FROMRow = enemyJump[i]
                FROMCol = enemyJump[i+1]
                TORow = enemyJump[i+3]
                TOCol = enemyJump[i+4]
                if ((ord(FROMRow)-65+1 == moveTORow) or (ord(FROMRow)-65-1 == moveTORow)) and \
                   ((ord(TORow)-65+1 == moveTORow) or (ord(TORow)-65-1 == moveTORow)) and \
                   ((int(FROMCol) + 1 == moveTOCol) or (int(FROMCol) - 1 == moveTOCol)) and \
                    ((int(TOCol) + 1 == moveTOCol) or (int(TOCol) - 1 == moveTOCol)):
                    suicideMoves.append(move)
    return suicideMoves

def getValidMove(board,player):
    if player=="b":
        playerName="black"
        enemyPlayer = 'r'
    else:
        playerName="red"
        enemyPlayer = 'b'

    # Player moves, jumps and crowns
    movesList=listValidMoves(board,player)
    jumpsList=listSingleJumps(board,player)
    jumpsList=listMultipleJumps(board,player,jumpsList)

    crowningMoves = findCrownRowMovesOrJumps(board, player, movesList)
    crowningJumps = findCrownRowMovesOrJumps(board, player, jumpsList)

    # Opponent moves, jumps and crowns
    enemyMovesList = listValidMoves(board, enemyPlayer)
    enemyJumpsList = listSingleJumps(board, enemyPlayer)
    enemyJumpsList = listMultipleJumps(board, enemyPlayer, enemyJumpsList)

    enemyCrowningMoves = findCrownRowMovesOrJumps(board, enemyPlayer, enemyMovesList)
    enemyCrowningJumps = findCrownRowMovesOrJumps(board, enemyPlayer, enemyJumpsList)
    
    while True:
        if crowningJumps != []: # Heuristic 1 (crowning jumps)
            return crowningJumps[random.randrange(len(crowningJumps))]
        if jumpsList != []: # Heuristic 2 (jumps)
            suicideJumps = findSuicideMoves(board, jumpsList, player, enemyPlayer)
            safeJumps = []
            for jump in jumpsList:
                if jump not in suicideJumps:
                    safeJumps.append(jump)
            if safeJumps != []: # Heuristic 9 (look for safe jumps first)
                if enemyCrowningJumps != []: # Heuristic 3 (safe jumps that block opponent crowning jumps)
                    blockingJumps = findBlockingMoves(safeJumps, enemyCrowningJumps)
                    if blockingJumps != []:
                        return blockingJumps[random.randrange(0, len(blockingJumps))]
                if enemyCrowningMoves != []: # Heuristic 4 (safe jumps that block opponent crowning moves)
                    blockingJumps = findBlockingMoves(safeJumps, enemyCrowningMoves)
                    if blockingJumps != []:
                        return blockingJumps[random.randrange(0, len(blockingJumps))]
                if enemyJumpsList != []: # Heuristic 5 (safe jumps that block opponent jumps)
                    blockingJumps = findBlockingMoves(safeJumps, enemyJumpsList)
                    if blockingJumps != []:
                        return blockingJumps[random.randrange(0, len(blockingJumps))]
            else: # Heuristic 10 (if no safe jumps, search all jumps)
                if enemyCrowningJumps != []: # Heuristic 11 (all jumps that block opponent crowning jumps)
                    blockingJumps = findBlockingMoves(jumpsList, enemyCrowningJumps)
                    if blockingJumps != []:
                        return blockingJumps[random.randrange(0, len(blockingJumps))]
                if enemyCrowningMoves != []: # Heuristic 12 (all jumps that block opponent crowning moves)
                    blockingJumps = findBlockingMoves(jumpsList, enemyCrowningMoves)
                    if blockingJumps != []:
                        return blockingJumps[random.randrange(0, len(blockingJumps))]
                if enemyJumpsList != []: # Heuristic 13 (all jumps that block opponent jumps)
                    blockingJumps = findBlockingMoves(jumpsList, enemyJumpsList)
                    if blockingJumps != []:
                        return blockingJumps[random.randrange(0, len(blockingJumps))]
            if safeJumps != []: # Heuristic 14 (if no blocking jumps, opt for safe jumps)
                return safeJumps[random.randrange(0, len(safeJumps))]
            else: # Heuristic 15 (no safe or blocking jumps)
                return jumpsList[random.randrange(0, len(jumpsList))]
        elif crowningMoves != []: # Heuristic 6 (crowning moves)
            return crowningMoves[random.randrange(0, len(crowningMoves))]
        else: # Heuristic 7 (regular move)
            suicideMoves = findSuicideMoves(board, movesList, player, enemyPlayer)
            safeMoves = []
            for move in movesList:
                if move not in suicideMoves:
                    safeMoves.append(move)
            if safeMoves != []: # Heuristic 8 (regular safe moves)
                return safeMoves[random.randrange(0, len(safeMoves))]
            else:
                return movesList[random.randrange(0, len(movesList))]
