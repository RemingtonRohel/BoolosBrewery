"""
Solver for hard game.
"""

from strats import *

class Strategy(Hard):
    question_limit = 7

    def solve(game):
        # Start with gathering some information about Alice and Bob.
        truth_dict = {
            Alice: {},
            Bob: {},
            Charlie: {},
            Dan: {},
        }
        results = []
        results.append(game.get_response(Alice.ask(True)))
        results.append(game.get_response(Alice.ask(False)))
        results.append(game.get_response(Bob.ask(True)))
        results.append(game.get_response(Bob.ask(False)))

        truth_dict[Alice] = {True: results[0], False: results[1]}
        truth_dict[Bob] = {True: results[2], False: results[3]}

        # Someone answering the same response twice indicates they are a Philosopher or Engineer
        if results[0] == results[1] and results[2] == results[3]:
            # Alice and Bob must be the engineer and philosopher (not necessarily respectively)
            
            remaining_responses = {Foo, Bar, Baz} - set(results)
            control_word = list(remaining_responses)[0]
            control_question = control_word.equals(True).iff

            if len(remaining_responses) == 2:
                # the remaining responses are the Mathematician/Physicist response set
                
                # We don't need to know whether the control_word means True or False to Charlie, 
                # we only care if their response matches the control_word.
                # If so, the other half of the question is True.
                if game.get_response(control_question(Charlie.studies(Math))) == control_word:
                    game.guess[Charlie] = Math
                    game.guess[Dan] = Phys
                else:
                    game.guess[Charlie] = Phys
                    game.guess[Dan] = Math

                # Now figure out who is what between Alice and Bob
                if game.get_response(control_question(Alice.studies(Phil))) == control_word:
                    game.guess[Alice] = Phil
                    game.guess[Bob] = Engg
                else:
                    game.guess[Alice] = Engg
                    game.guess[Bob] = Phil

            if len(remaining_responses) == 2:
                # the remaining response is part of the set of Mathematician/Physicist responses
                
                reply = game.get_response(control_question(Charlie.studies(Math)))
                if reply == control_word:
                    # Only happens if control_word means True, and the question is True
                    game.guess[Charlie] = Math
                    game.guess[Dan] = Phys
                    # Still need to determine between Alice and Bob who is the Engineer/Philosopher
                    if game.get_response(control_question(Alice.studies(Engg))) == control_word:
                        game.guess[Alice] = Engg
                        game.guess[Bob] = Phil
                    else:
                        game.guess[Alice] = Phil
                        game.guess[Bob] = Engg
                else:
                    # The reply did not match control_word, Charlie does not study Math
                    game.guess[Charlie] = Phys
                    game.guess[Dan] = Math

            return  # All done here

        elif results[0] == results[1]:
            # Alice gave identical answers, she is either the Engineer or Philosopher
            pass

        elif results[2] == results[3]:
            # Bob gave identical answers, he is either the Engineer or Philosopher
            pass

        elif results[0] == results[3] and results[1] == results[2]:
            # Alice and Bob may be the Mathematician and Physicist
            pass

        else:
            # Two different response sets, one of Alice and Bob is the Engineer
            reply = game.get_response(Charlie.ask(True))
            results.append(reply)

            if reply == results[1]:
                # Charlie's True is Alice's False, they are likely the Math/Physics pair with Bob/Dan Engg/Phil
                # The other possibility is Alice Engg, Bob Math/Phys, Charlie Phil, Dan Math/Phys
                if game.get_response(Charlie.ask(False)) == reply:
                    # Charlie replies the same no matter what, he is Phil and thus Alice Engg
                    game.guess[Charlie] = Phil
                    game.guess[Alice] = Engg
                    control_word = truth_dict[Bob][True]
                    if game.person_is_mathematician(Bob, control_word):
                        game.guess[Bob] = Math
                        game.guess[Dan] = Phys
                    else:
                        game.guess[Bob] = Phys
                        game.guess[Dan] = Math
                else:
                    # Charlie is not Phil, therefore Bob/Dan and Engg/Phil and Alice/Charlie are Math/Phys
                    game.guess[Dan] = Phil
                    game.guess[Bob] = Engg
                    control_word = truth_dict[Alice][True]
                    if game.person_is_mathematician(Alice, control_word):
                        game.guess[Alice] = Math
                        game.guess[Charlie] = Phys
                    else:
                        game.guess[Alice] = Phys
                        game.guess[Charlie] = Math
                    
            elif reply == results[3]:
                # Charlie's True is Bob's False, possibly Bob/Charlie are Math/Phys, Alice/Dan Engg/Phil
                # The other possibility is Bob Engg, Alice Math/Phys, Charlie Phil, Dan Math/Phys
                if game.get_response(Charlie.ask(False)) == reply:
                    # Charlie replies the same no matter what, he is Phil and thus Bob Engg
                    game.guess[Charlie] = Phil
                    game.guess[Bob] = Engg
                    control_word = truth_dict[Alice][True]
                    if game.person_is_mathematician(Alice, control_word):
                        game.guess[Alice] = Math
                        game.guess[Dan] = Phys
                    else:
                        game.guess[Alice] = Phys
                        game.guess[Dan] = Math
                else:
                    # Charlie is not Phil, therefore Alice/Dan and Engg/Phil and Bob/Charlie are Math/Phys
                    game.guess[Dan] = Phil
                    game.guess[Alice] = Engg
                    control_word = truth_dict[Bob][True]
                    if game.person_is_mathematician(Bob, control_word):
                        game.guess[Bob] = Math
                        game.guess[Charlie] = Phys
                    else:
                        game.guess[Bob] = Phys
                        game.guess[Charlie] = Math
            elif reply == results[0]:
                # Charlie's True matches Alice's True, these two must be the Engineer/Philosopher
                control_word = truth_dict[Bob][True]
                if game.get_response(Bob.ask(control_word.equals(True).iff(Bob.studies(Math)))) == control_word:
                    game.guess[Bob] = Math
                    game.guess[Dan] = Phys
                else:
                    game.guess[Bob] = Phys
                    game.guess[Dan] = Math
                if game.get_response(Bob.ask(control_word.equals(True).iff(Alice.studies(Engg)))) == control_word:
                    game.guess[Alice] = Engg
                    game.guess[Charlie] = Phil
                else:
                    game.guess[Alice] = Phil
                    game.guess[Charlie] = Engg
            elif reply == results[2]:
                # Charlie's True matches Bob's True, these two must be the Engineer/Philosopher
                control_word = truth_dict[Alice][True]
                if game.get_response(Alice.ask(control_word.equals(True).iff(Alice.studies(Math)))) == control_word:
                    game.guess[Alice] = Math
                    game.guess[Dan] = Phys
                else:
                    game.guess[Alice] = Phys
                    game.guess[Dan] = Math
                if game.get_response(Alice.ask(control_word.equals(True).iff(Bob.studies(Engg)))) == control_word:
                    game.guess[Bob] = Engg
                    game.guess[Charlie] = Phil
                else:
                    game.guess[Bob] = Phil
                    game.guess[Charlie] = Engg


    @staticmethod
    def person_is_mathematician(name, control_word):
        """
        Will determine if a person (that we must know beforehand is a Math/Phys person) is the mathematician
        """
        return game.get_response(name.ask(control_word.equals(True).iff(name.studies(Math)))) == control_word

