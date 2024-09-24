import board
import game
import player
import randomPlayer
# Note that you can comment out the following if you don't want to seed the random player differently each run
from datetime import datetime
import time

start=time.time()
# This script allows you to test your solution.
# Your coursework implementation must always be player 1.
# You should consider changing player 2 to use a minimax approach for evaluation.
# It is recommended that you also consider other game board sizes, and vary the number of pieces 
# that are required in a line to win. There are examples of the method calls to create such games
# commented out below.
p1 = player.Player("X")

# Player 2 currently picks random moves and so, while player 2 is not very good, it does allow you to
# start testing your solution. Once you have something sensible, you should change player 2 to be more 
# intelligent. Note that you can specify a seed for the random player (currently the seed is '42'),
# which allows for testing in a consistent environment.
# Note that the following two lines seed the random player differently each run
games=10
c=0
wins=0
losses=0
draws=0
while c<games:
    print(f"\n----GAME {c+1} ----")
    c+=1    
    seed = datetime.now().timestamp()
    p2 = randomPlayer.RandomPlayer("O", seed)
    # Instead of randomly seeding, you can comment out the following line to seed the random player and
    # test with a consistent opponent
    #p2 = randomPlayer.RandomPlayer("O", seed=42)

    # The arguments to game.Game specify the two players, the number of rows, the number of columns
    # and the number of pieces that need to be placed in a line in order to win.
    #g=game.Game(p1,p2,7,3,3)
    #g=game.Game(p1,p2,10,9,8)
    #g = game.Game(p1, p2, 5, 6, 2)
    #g= game.Game(p1, p2, 5, 5, 2)
    #g = game.Game(p1, p2, 4, 5, 3)
    #g = game.Game(p1, p2, 4, 4, 4)
    #g=game.Game(p1,p2,5,5,2)
    #g=game.Game(p1,p2,6,6,2)
    g=game.Game(p1,p2,7,7,2)
    #g = game.Game(p1, p2, 4, 4, 2)
    #g = game.Game(p1, p2, 3, 3, 2)

    # You can pass 'True' to the playGame() method to test your alpha-beta pruning approach, i.e., to make
    # player 1 use alpha-beta. If you want player 2 to use alpha-beta you will need to ensure 
    # that you create player 2 accordingly. 
    res=g.playGame(True)
    if(res==1):
       wins+=1
    elif(res==-1):
       losses+=1
    else:
       draws+=1
end=time.time()
print(f"\n\nRuntime: {(end-start)*(10**3):.02f}ms")
print(f"Games: {games}\nWins: {wins}\nLosses: {losses}\nDraws: {draws}\nWin Rate: {(wins/games):.02f}")