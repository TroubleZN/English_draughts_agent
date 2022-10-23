# English draughts game playing agent
## Rules
The detailed rule can be found in https://en.wikipedia.org/wiki/English_draughts

## Program information
Language: python 3.8

Modules: numpy, copy

## Discription
Two heuristic functions are applied in the function.

- H1: this heuristic function is based on the piece counts. The player with more pieces will be more likely to win and pieces as kings will provide more chances. Thus, each piece in our team will get us one credit and one king will come with half more credit. Each piece in the enemy team will remove one credit and one king will remove half more credit.

- H2: this heuristic function is a complex version, which is a linear combination of some features. For the H1, there is a big chance to avoid battle near the end of the game, which will bring a tie. This one will consider some more features, containing the chances to jump at current status, the smallest distance for a man to be a king.

## Running instruction
1) 'cd' into to directory where 'checkers.py' is located
2) Run 'python3 checkers.py' to run a "user VS computer" game.
3) Run 'python3 checkers.py --compare_depth' to run an automatic comparison program to compare the performance of different depths.
4) Run 'python3 checkers.py --compare_evaluation' to run an automatic comparison program to compare the performance of different evaluation functions.

## Reference
I referenced the alpha-beta function from 'https://github.com/aimacode/aima-python'
