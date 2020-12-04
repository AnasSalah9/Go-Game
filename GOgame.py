import Board

class GOgame:

    board = Board.Board(None, (-1,-1), 9)
    board.turn()
    AgentTertoiry, OpponentTertoiry = board.countLiberty()
    OpponentTertoiry += 6.5
    print("the Agent Teritory is : "+str(AgentTertoiry))
    print("the Opponent Teritory is : "+str(OpponentTertoiry))
    if(AgentTertoiry > OpponentTertoiry):
        print("Our Agent won the game")
    elif(AgentTertoiry < OpponentTertoiry):
        print("The game is end and the loser is our Agent, let us try to grow up it level")
    else:
        print("_____DRAW_____")

    exit()
