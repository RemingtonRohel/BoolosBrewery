"""
Solver for default game.
"""

from strats import *

class Strategy(Default):
    question_limit = 3

    def solve(game):
        """
        Will solve in exactly three attempts every time.
        """
        
        # .iff(Foo.equals(True)) maps a Foo response to True (if you are asking someone who isn't the engineer).
        control = Foo.equals(True).iff

        # First, ask Bob is Alice studies non-engineering. 
        # If Bob is the engineer, the response is meaningless.
        # If Bob isn't the engineer, then a Foo response means that Charlie is the engineer.
        #   A Bar response means that Alice is the engineer.
        # So, a Foo response only happens if either Bob or Charlie is the engineer, meaning Alice will give reliable responses.
        # A Bar response only happens if Alice or Bob is the engineer, meaning Charlie will give reliable responses.
        response = game.get_response(Bob.ask(control(Alice.studies(Math).or_(Alice.studies(Phys)))))

        if response == Foo:
            asker = Alice
            other = Charlie
        else:
            asker = Charlie
            other = Alice

        # Ask the reliable responder if they study math. Foo means yes, Bar means no, implying they study Physics.
        # Whichever they don't study is studied by the other non-engineer.
        second_response = game.get_response(asker.ask(control(asker.studies(Math))))

        if second_response == Foo:
            game.guess[asker] = Math
            leftover = Phys
        else:
            game.guess[asker] = Phys
            leftover = Math

        # Now, ask them if Bob studies Engineering. Foo means yes, Bar means no.
        # Either Bob or the remaining non-asker studies Engineering, and the final person studies the left over subject.
        third_response = game.get_response(asker.ask(control(Bob.studies(Engg))))

        if third_response == Foo:
            game.guess[Bob] = Engg
            game.guess[other] = leftover
        else:
            game.guess[Bob] = leftover
            game.guess[other] = Engg

