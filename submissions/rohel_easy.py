"""
Solver for easy game.
"""

from strats import *

class Strategy(Easy):
    question_limit = 1

    def solve(game):
        """
        .iff(Foo.equals(True)) essentially maps a Foo response to True, and a Bar response to False.
        So, if the question on the other side of the iff is True, then you get Foo as a response.
        """

        response = game.get_response(Alice.ask(Alice.studies(Math).iff(Foo.equals(True))))

        if response == Foo:
            game.guess[Alice] = Math
            game.guess[Bob] = Phys
        else:
            game.guess[Bob] = Math
            game.guess[Alice] = Phys

