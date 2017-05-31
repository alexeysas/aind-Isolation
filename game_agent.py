"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def center_score(game, player): 
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)

    return float((h - y)**2 + (w - x)**2)

def free_area_score(game, player, e=2, spaces = None): 
    y, x = game.get_player_location(player)

    if spaces == None:
        spaces = game.get_blank_spaces()

    data = [1 for sy, sx in spaces if (sy - y) + (sy - y) <= e]

    res = sum(data)
    return res

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    simulation = game.copy()

    delta = 0

    while True:
        moves = simulation.get_legal_moves()
        moves_count = len(moves)
        if moves_count == 0:
            if simulation.is_winner(player):
                delta = 1
            else:
                delta = -1
            break
        selected_move = random.randint(0, moves_count - 1)
        simulation.apply_move(moves[selected_move])

    return float(own_moves - opp_moves + 20 * delta)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    #defensive player
    #spaces = game.get_blank_spaces()

    #if len(spaces) > 300:
    #   return -center_score(game, player)# + center_score(game, game.get_opponent(player))

     #opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
   
    own_moves = len(game.get_legal_moves(player))
    return float(-own_moves)

    #return float(own_moves - opp_moves + free_area_score(game, player) - free_area_score(game, game.get_opponent(player)))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(free_area_score(game, player) - free_area_score(game, game.get_opponent(player)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth      
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.best_move = (-1, -1)


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        self.best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            move = self.minimax(game, self.search_depth)
            return move

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return self.best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA

                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        _, move = self.minimax_search(game, depth)
        return move

    def minimax_search(self, game, depth):
        """ min max """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves()
        moves_count = len(moves)

        #print(game.to_string())

        #chck for TERMINAL-TEST - return position score for minimax player
        if moves_count <= 0:
            score = game.utility(self)
            #print('Terminal test')
            move = (-1, -1)
            return score, move

        if depth == self.search_depth:
            self.best_move = moves[0]

        if depth == 0:
            score = self.score(game, self)
            move = (-1, -1)
            return score, move

        res = [(self.minimax_search(game.forecast_move(m), depth - 1)[0], m) for m in moves]
        #print(res)

        if game.active_player == self:
            score, move = max(res)
        else:
            score, move = min(res)

        return score, move

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        self.best_move = (-1, -1)

        try:
            i = 1
            while True:
                self.best_move = self.alphabeta(game, i)
                i = i + 1
            return self.best_move
        except SearchTimeout:
            return self.best_move
       
        return self.best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        _, move = self.max_value(game, depth, alpha, beta)

        return move

    def terminal_test(self, game, moves, depth):
        """ Checks if we need to finish search:
        Either no valid move or max-depth reached
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves_count = len(moves)

        if moves_count <= 0:
            score = game.utility(self)
            #print('Terminal test')
            return True, score

        if depth == 0:
            score = self.score(game, self)
            #print('Leaf node, value:{}'.format(score))
            return True, score

        return False, None

    def max_value(self, game, depth, a, b):

        moves = game.get_legal_moves()
        res_move = None

        is_eos, score = self.terminal_test(game, moves, depth)
        if is_eos:
            return score, res_move

       #print('Entering max node, depth: {}, a: {}, b: {}, moves: {}'.format(depth, a, b, moves))

        res = float("-inf")
        res_move = moves[0]
        for move in moves:
            score, _ = self.min_value(game.forecast_move(move), depth - 1, a, b)
            #print('Evaluated move: {}, score: {}'.format(move, score))
            if score > res:
                res = score
                res_move = move

            if res >= b:
                return res, res_move

            a = max(a, res)

        return res, res_move

    def min_value(self, game, depth, a, b):

        moves = game.get_legal_moves()
        res_move = None

        is_eos, score = self.terminal_test(game, moves, depth)
        if is_eos:
            return score, res_move

        #print('Entering min node, depth: {}, a: {}, b: {}, moves: {}'.format(depth, a, b, moves))

        res = float("inf")
        res_move = moves[0]
        for move in moves:
            score, _ = self.max_value(game.forecast_move(move), depth - 1, a, b)
            #print('Evaluated move: {}, score: {}'.format(move, score))
            if score < res:
                res = score
                res_move = move

            if res <= a:
                return res, res_move

            b = min(b, res)

        return res, res_move
