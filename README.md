# Game of UR: The earliest game known

The objective of this repository is to develop an understanding for AI. Here the ancient Game of UR is provided in python implementation in 3 modes
1. Player vs Player
2. Player vs AI
3. AI vs AI

Here you need to develop an AI module which can play the game and ofcourse, with an objective to win. This module has to be written in AI.py.
You can also record the moves of players during the game by choosing "y" in the game options. It saves each move in a csv file in the data folder. The name of the file is epoch in seconds.

To play this game
```
$ python3
>>> import play
>>> play.Ur().start()
```

To skip introduction and setup, initialize with options
```
$ python3
>>> import play
>>> play.Ur().start({"gameType":"1", "autosaveMoves":"y"})
```

gameType: "1"/"2"/"3"
autosaveMoves: "y/n"

Happy Coding!!
