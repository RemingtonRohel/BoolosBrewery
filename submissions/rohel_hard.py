"""
Solver for hard game.
"""

from strats import *

class Strategy(Hard):
    question_limit = 7

    def solve(game):
        # Start with gathering some information about Alice and Bob.
        bool_map = {}
        game.guess[Alice] = Engg
        game.guess[Bob] = Phil
        game.guess[Charlie] = Math
        game.guess[Dan] = Phys

        def assign_math_phys_pair(person_x, person_y, truth_word=None):
            if truth_word is None:
                truth_word = bool_map[person_x]
            if game.person_is_mathematician(person_x, truth_word):
                game.guess[person_x] = Math
                game.guess[person_y] = Phys
            else:
                game.guess[person_x] = Phys
                game.guess[person_y] = Math

        results = [
            game.get_response(Alice.ask(True)),
            game.get_response(Alice.ask(False)),
            game.get_response(Bob.ask(True)),
            game.get_response(Bob.ask(False))
        ]

        bool_map[Alice] = results[0]
        bool_map[Bob] = results[2]

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
                assign_math_phys_pair(Charlie, Dan, truth_word=control_word)

                # Now figure out who is what between Alice and Bob
                if game.get_response(Charlie.ask(control_question(Alice.studies(Phil)))) == control_word:
                    game.guess[Alice] = Phil
                    game.guess[Bob] = Engg
                else:
                    game.guess[Alice] = Engg
                    game.guess[Bob] = Phil

            if len(remaining_responses) == 2:
                # the remaining response is part of the set of Mathematician/Physicist responses
                
                reply = game.get_response(Charlie.ask(control_question(Charlie.studies(Math))))
                if reply == control_word:
                    # Only happens if control_word means True, and the question is True
                    game.guess[Charlie] = Math
                    game.guess[Dan] = Phys
                    # Still need to determine between Alice and Bob who is the Engineer/Philosopher
                    if game.get_response(Charlie.ask(control_question(Alice.studies(Engg)))) == control_word:
                        game.guess[Alice] = Engg
                        game.guess[Bob] = Phil
                    else:
                        game.guess[Alice] = Phil
                        game.guess[Bob] = Engg
                else:
                    # The reply did not match control_word, Charlie does not study Math
                    game.guess[Charlie] = Phys
                    game.guess[Dan] = Math
                    # todo: What do Alice and Bob study?

            return  # All done here

        elif results[0] == results[1]:
            # Alice gave identical answers, she is either the Engineer or Philosopher
            pass

        elif results[2] == results[3]:
            # Bob gave identical answers, he is either the Engineer or Philosopher
            bool_map[Charlie] = game.get_response(Charlie.ask(True))
            if bool_map[Charlie] in results and len(set(results)) == 2:
                # Either Alice/Bob are Engg/Phil, or Alice is Math/Phys.
                # Alice:   [Engg,      Math/Phys]
                # Bob:     [Phil,      Engg/Phil]
                # Charlie: [Math/Phys, Math/Phys/Phil]
                # Dan:     [Math/Phys, Math/Phys/Phil]
                not_bob = {Foo, Bar, Baz} - set(bool_map[Bob])
                dan_false = game.get_response(Dan.ask(False))
                if dan_false in not_bob:
                    # Can only happen if in right column scenario
                    game.guess[Bob] = Engg
                    game.guess[Dan] = Phil
                    assign_math_phys_pair(Alice, Charlie)
                else:
                    game.guess[Alice] = Engg
                    game.guess[Bob] = Phil
                    assign_math_phys_pair(Charlie, Dan)
            elif bool_map[Charlie] in results:
                # Alice:   [Engg,      Math/Phys]
                # Bob:     [Phil,      Engg]
                # Charlie: [Math/Phys, Math/Phys/Phil]
                # Dan:     [Math/Phys, Math/Phys/Phil]
                if bool_map[Charlie] == bool_map[Bob]:
                    # Right column scenario
                    game.guess[Bob] = Engg
                    if game.get_response(Alice.ask(Charlie.studies(Phil))) == bool_map[Alice]:
                        game.guess[Charlie] = Phil
                        assign_math_phys_pair(Alice, Dan)
                    else:
                        game.guess[Dan] = Phil
                        assign_math_phys_pair(Alice, Charlie)
            else:
                # Charlie said something new, so either Alice/Bob and Engg/Phil, or Charlie is Phil
                # In other words, Dan cannot be Phil
                # If Alice/Bob are Engg/Phil, then whoever said the same thing twice is Phil (in this case, Bob)
                # If Charlie is Phil, then Bob must be Engg since he repeated a response, so Alice is Math/Phys
                # Either way, Dan is Math/Phys
                # So, Alice is [Engg, Math/Phys], Bob is [Phil, Engg], Charlie is [Math/Phys, Phil], Dan is [Math/Phys]
                if game.get_response(Dan.ask(False)) == bool_map[Charlie]:
                    # Charlie and Dan are the Math/Physics pair
                    assign_math_phys_pair(Charlie, Dan)
                    game.guess[Alice] = Engg
                    game.guess[Bob] = Phil
                else:
                    game.guess[Bob] = Engg
                    game.guess[Charlie] = Phil
                    assign_math_phys_pair(Alice, Dan)

        elif results[0] == results[3] and results[1] == results[2]:
            # The philosopher is either Charlie or Dan
            bool_map[Charlie] = game.get_response(Charlie.ask(True))
            if bool_map[Charlie] not in results[:2]:
                # Charlie is either the Engineer or the Philosopher
                bool_map[Dan] = game.get_response(Dan.ask(True))
                if bool_map[Dan] in results[:2]:
                    game.guess[Charlie] = Phil
                    if bool_map[Dan] == bool_map[Alice]:
                        # Either Dan or Alice is the engineer
                        if game.person_is_mathematician(Bob, bool_map[Bob]):
                            game.guess[Bob] = Math
                        else:
                            game.guess[Bob] = Phys
                        # todo: How can we figure the rest out in less turns?
                    else:
                        # Either Dan or Bob is the engineer
                        if game.person_is_mathematician(Alice, bool_map[Alice]):
                            game.guess[Alice] = Math
                        else:
                            game.guess[Alice] = Phys
                        # todo: How can we figure the rest out in less turns?
            else:
                # The philosopher must be Dan
                game.guess[Dan] = Phil
                if bool_map[Charlie] == bool_map[Alice]:
                    # Alice or Charlie is the Engineer
                    if game.get_response(Bob.ask(Alice.studies(Engg))) == bool_map[Bob]:
                        game.guess[Alice] = Engg
                        other = Charlie
                    else:
                        game.guess[Charlie] = Engg
                        other = Alice
                    assign_math_phys_pair(Bob, other)

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
                    assign_math_phys_pair(Bob, Dan)
                else:
                    # Charlie is not Phil, therefore Bob/Dan and Engg/Phil and Alice/Charlie are Math/Phys
                    game.guess[Dan] = Phil
                    game.guess[Bob] = Engg
                    assign_math_phys_pair(Alice, Charlie)
                    
            elif reply == results[3]:
                # Charlie's True is Bob's False, possibly Bob/Charlie are Math/Phys, Alice/Dan Engg/Phil
                # The other possibility is Bob Engg, Alice Math/Phys, Charlie Phil, Dan Math/Phys
                if game.get_response(Charlie.ask(False)) == reply:
                    # Charlie replies the same no matter what, he is Phil and thus Bob Engg
                    game.guess[Charlie] = Phil
                    game.guess[Bob] = Engg
                    assign_math_phys_pair(Alice, Dan)
                else:
                    # Charlie is not Phil, therefore Alice/Dan and Engg/Phil and Bob/Charlie are Math/Phys
                    game.guess[Dan] = Phil
                    game.guess[Alice] = Engg
                    assign_math_phys_pair(Bob, Charlie)

            elif reply == results[0]:
                # Charlie's True matches Alice's True, these two must be the Engineer/Philosopher
                assign_math_phys_pair(Bob, Dan)
                control_word = bool_map[Bob]
                if game.get_response(Bob.ask(control_word.equals(True).iff(Alice.studies(Engg)))) == control_word:
                    game.guess[Alice] = Engg
                    game.guess[Charlie] = Phil
                else:
                    game.guess[Alice] = Phil
                    game.guess[Charlie] = Engg
            elif reply == results[2]:
                # Charlie's True matches Bob's True, these two must be the Engineer/Philosopher
                assign_math_phys_pair(Alice, Dan)
                control_word = bool_map[Alice]
                if game.get_response(Alice.ask(control_word.equals(True).iff(Bob.studies(Engg)))) == control_word:
                    game.guess[Bob] = Engg
                    game.guess[Charlie] = Phil
                else:
                    game.guess[Bob] = Phil
                    game.guess[Charlie] = Engg

    def person_is_mathematician(game, name, control_word):
        """
        Will determine if a person (that we must know beforehand is a Math/Phys person) is the mathematician
        """
        return game.get_response(name.ask(control_word.equals(True).iff(name.studies(Math)))) == control_word

