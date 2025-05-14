from Player import *

class Game:

    def __init__(
            game,
            players: List[Player],
            n_starting_cubes_per_player: int,
            lowest_number: int,
            highest_number: int,
            n_numbers_to_remove:int = 0
        ):
            game.players = players
            game.set_starting_cubes(n_starting_cubes_per_player)
            game.lowest_number = lowest_number
            game.highest_number = highest_number
            game.n_numbers_to_remove = n_numbers_to_remove

            game.numbers = {k:v for k,v in zip(range(lowest_number,highest_number), [None])}
            game.number_stack = list(range(lowest_number, highest_number))
            random.shuffle(game.number_stack)

            for _ in range(n_numbers_to_remove):
                game.number_stack.pop()

            game.round_counter = 0 
            game.turn_counter = 0
            game.turn_record = []
            game.latest_synced_turn = -1


    def set_starting_cubes(game, n: int):
        for player in game.players:
            player.cubes = n

    def print_board(game, indentation = 12):
        for line in game.get_board(indentation):
            print(line)
          
    
    def get_board(game, indentation = 12):
        line = ""+" "*indentation
        lines = []
        for n in range(game.lowest_number, game.highest_number ):
            if n == game.num:
                line += color_text('white',f'({str(n).rjust(2)})')
                if n%5==0:
                    lines.append(line)
                    line = ""+" "*indentation
            else:
                for player in game.players:
                    if n in player.numbers:
                        formatted_number = player.format_number(n)
                        break
                else:
                    formatted_number = color_text('black',f'[{str(n).rjust(2)}]')
                line += formatted_number
                if n%5==0:
                    lines.append(line)
                    line = ""+" "*indentation
        while not n%5 == 0:
            n+=1
            line+=" "*4
        return lines

    def get_scoreboard(game):
        lines = []
        #lines.append("              SCOREBOARD                       ")
        #lines.append("_______________________________________________")
        lines.append("| RANK | SCORE |    PLAYER    | CUBES | LADDERS")
        for rank, player in enumerate(sorted(game.players)):
            lines.append(f'|{str(rank+1).center(6)}|{str(player.score).center(7)}{player}')
        return lines

    def print_scoreboard(game):
        for line in game.get_scoreboard():
            print(line)
        
    def print_history(game):
        history=[]
        round = None
        round_counter=0
        turn_counter=0
        while len(history)<12:
            if round == None:
                round_counter-=1
                if abs(round_counter)>len(game.turn_record): break
                round = game.turn_record[round_counter]
            turn_counter-=1
            if abs(turn_counter)>len(round):
                round = None
                turn_counter = 0
                continue
            turn = round[turn_counter]
            history.insert(0,turn)
        for line in history: print(line)
    
    def draw_board_and_score(game):
        scoreboard_lines =game.get_scoreboard()
        scoreboard_dims = get_dims(scoreboard_lines)
        board_lines = game.get_board(0)
        board_dims = get_dims(board_lines)
        lines = []
        for i in range(max(len(scoreboard_lines), len(board_lines))):
            l1 = "" if i>=scoreboard_dims[1] else scoreboard_lines[i]
            l2 = "" if i>=board_dims[1] else board_lines[i]
            l1 = l1.ljust(scoreboard_dims[0])
            l2 = l2.ljust(board_dims[0])
            lines.append(l2+"  |+|  "+l1)
        for line in lines:
            print(line)

    def step_in_terminal(game, redo = False):
        """Run one round with user input/output in the terminal
        """
        if not redo:
            num = game.number_stack.pop(0)
            game.num = num
            game.round_counter+=1
            game.auto_select_counter=0
            print()
            input(f"Press enter to begin round {game.round_counter}")
        else:
            num = game.num
        clear()
        game.draw_board_and_score()

        print()
        print("| ROUND | NUMBER | TURN |    PLAYER    |  CUBES |    ACTION ")
        game.print_history()
        if redo:
            for line in game.turn_lines:
                print(line)
        else:
            game.turn_lines = []
            game.pile = 0
            game.local_counter = 0
        while True:
            #if not redo:
            turn_statement = f'|{str(game.round_counter).center(7)}|' if game.local_counter == 0 else "|       |"
            turn_statement += f'  [{str(num).rjust(2)}]  |'
            turn_statement += f'{str(game.turn_counter).center(6)}|'
            end_turn = False
            player: Player = game.players[game.turn_counter%len(game.players)]
            turn_statement += player.get_name('center', 14) +'|'
            cube_text= "■"*player.cubes if player.cubes<6 else f"■ x {player.cubes}"
            if player.cubes == 0: cube_text = "NONE"
            turn_statement += f' {cube_text.ljust(6)} |'
            if player.cubes == 0:

                if game.pile > 0:
                    turn_statement += color_text(player.color,f" <-- [{str(num).rjust(2)}] & Pile({format_pile(game.pile)})")
                else:
                    turn_statement += color_text(player.color,f" <-- [{str(num).rjust(2)}]")
 
                game.turn_lines.append(turn_statement)
                print(game.turn_lines[-1])
                player.numbers.append(num)
                player.cubes += game.pile
                game.pile = 0
                game.turn_record.append(game.turn_lines)
                game.turn_counter +=1
                game.num = None
                break

            if player.played_by_human and game.auto_select_counter<5:
                #Always update to latest before showing human
                if game.latest_synced_turn != game.turn_counter:
                    game.latest_synced_turn = game.turn_counter
                    game.step_in_terminal(redo = True)
                    return
                choice = None
                phrase = None
                print(turn_statement+' (WATING FOR PLAYER INPUT)')
                pile_statement =  "■"*game.pile if game.pile>0 else "<empty>"
                print(f'NUMBER: [{num}]   PILE: ' +pile_statement)
                phrase = " User Action Needed! Type:\n" 
                phrase += f" 'p' - to pay and throw one cube in the pile\n"
                if game.pile>=1: phrase += f" 't' - to take number [{str(num).rjust(2)}] and {format_pile(game.pile)} from the pile\n"
                else: phrase += f" 't' - to take number [{str(num).rjust(2)}]\n"
                choice = input(phrase)
                if choice == "l": choice = "t"
                if choice in ["t", "p"]:
                    clear_previous_line(6)
                else: 
                    game.auto_select_counter+=1
                    game.step_in_terminal(redo = True)
                    return
            else: # Simulated decision: 50% chance to pay or take
                choice = player.strategy.make_choice(game,player)

            # A Valid choice as been made
            game.turn_counter+=1

            statement = ''
            if choice == "p":
                player.cubes -= 1
                game.pile += 1
                statement += f"  ■  -->    Pile( {format_pile(game.pile)} )"
            else:
                if game.pile>0:
                    #statement += f' {color_text("yellow","<--")} [{num}] & Pile( {format_pile(game.pile)} )'
                    statement += color_text(player.color,f' <-- [{str(num).rjust(2)}] & Pile( {format_pile(game.pile)} )')
                else:
                    statement += color_text(player.color,f' <-- [{str(num).rjust(2)}]')
                player.numbers.append(num)
                player.cubes += game.pile
                game.pile = 0
                end_turn = True

            turn_statement += statement
            game.turn_lines.append(turn_statement)
            print(game.turn_lines[-1])
            
            game.local_counter += 1
            if end_turn:
                game.turn_record.append(game.turn_lines)
                game.turn_counter+=1
                game.num = None
                break

    def step(game):
        """
        Simulate one round of the game
        """
        num = game.number_stack.pop(0)
        game.num = num
        game.round_counter += 1

        game.pile = 0
        local_counter = 0

        while True:
            local_counter += 1
            game.turn_counter += 1
            end_turn = False
            player: Player = game.players[game.turn_counter % len(game.players)]

            if player.cubes == 0:
                player.numbers.append(num)
                player.cubes += game.pile
                game.pile = 0
                game.num = None
                break

            # Simulate choice even for human players
            if player.played_by_human:
                choice = player.strategy.make_choice(game, player)
            else:
                choice = player.strategy.make_choice(game, player)

            if choice == "p":
                player.cubes -= 1
                game.pile += 1
            else:
                player.numbers.append(num)
                player.cubes += game.pile
                game.pile = 0
                end_turn = True


            if end_turn:
                game.num = None
                break
        
    

    def play(game, in_terminal = False):
        if in_terminal:
            while game.number_stack:
                game.step_in_terminal()

            clear()
            game.num = None
            print("GAME FINISHED. FINAL STATE:")
            print("")
            game.draw_board_and_score()
        else:
            while game.number_stack:
                game.step()

