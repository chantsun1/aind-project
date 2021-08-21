"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import itertools

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

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
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    w, h = game.width / 2., game.height / 2.
    own_y, own_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))
    own_distance = float((h - own_y)**2 + (w - own_x)**2)
    opp_distance = float((h - opp_y)**2 + (w - opp_x)**2)
    
    return float((own_moves - opp_moves) + (opp_distance - own_distance))


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
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - 2 * opp_moves)


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
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
#    own_moves = len(game.get_legal_moves(player))
#    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    w, h = game.width / 2., game.height / 2.
    own_y, own_x = game.get_player_location(player)
    opp_y, opp_x = game.get_player_location(game.get_opponent(player))
    own_distance = float((h - own_y)**2 + (w - own_x)**2)
    opp_distance = float((h - opp_y)**2 + (w - opp_x)**2)
    return float(opp_distance - own_distance)
    



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
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def min_max_helper(self, game, max_depth, max_mode, move, current_depth):
        """
        Perform Top-Down Recursion for Minimax Algorithm, starting from Depth 0 to the given max_depth
        Parameters
        ----------
        game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
        
        max_depth : int
        The max_depth specified for the Depth Limited Search in Minimax Algorithm
        
        max_mode : bool
        Specifies maximizing node or minimizing node
        
        move : (int, int)
        The move for which the score is being calculated, used as helper parameter for recursion
        
        current_depth : int
        Starting point for the recursive function. Defaults to zero. Should always be zero.
        
        Returns
        -------
        (int, (int, int))
        The score for the move, and the move
        
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        result_move = None
        moves = game.get_legal_moves()

        if not moves:
            return game.utility(self), (-1, -1)

        if max_depth == current_depth:
            return self.score(game, self), (-1, -1)

        if max_mode:
            max_score = float("-inf")
            for m in moves:
                new_game = game.forecast_move(m)
                init_move = m if current_depth is 0 else move
                score, temp_move = self.min_max_helper(new_game, max_depth, False, init_move, current_depth + 1)
                if score > max_score:
                    max_score, result_move = score, init_move
            return max_score, result_move
        else:
            min_score = float("inf")
            for m in moves:
                new_game = game.forecast_move(m)
                init_move = m if current_depth is 0 else move
                score, temp_move = self.min_max_helper(new_game, max_depth, True, init_move, current_depth + 1)
                if score < min_score:
                    min_score, result_move = score, init_move
            return min_score, result_move

    
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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        score, move = self.min_max_helper(game, depth, True, None, 0)
        return move
        

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            for i in itertools.count():
                best_move = self.alphabeta(game, i+1)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def alpha_beta_helper(self, game, max_depth, max_mode, move, current_depth, alpha=float("-inf"), beta=float("inf")):
        """
        Perform Top-Down Recursion for Minimax Algorithm, starting from Depth 0 to the given max_depth
        Parameters
        ----------
        game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
        
        max_depth : int
        The max_depth specified for the Depth Limited Search in Minimax Algorithm
        
        max_mode : bool
        Specifies maximizing node or minimizing node
        
        move : (int, int)
        The move for which the score is being calculated, used as helper parameter for recursion
        
        current_depth : int
        Starting point for the recursive function. Defaults to zero. Should always be zero.
        
        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers
        
        Returns
        -------
        (int, (int, int))
        The score for the move, and the move
        
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        result_move = None
        moves = game.get_legal_moves()

        if not moves:
            return game.utility(self), (-1, -1)

        if max_depth == current_depth:
            return self.score(game, self), (-1, -1)

        if max_mode:
            max_score = float("-inf")
            for m in moves:
                new_game = game.forecast_move(m)
                init_move = m if current_depth is 0 else move
                score, temp_move = self.alpha_beta_helper(new_game, max_depth, False, init_move, current_depth + 1, alpha, beta)
                if score > max_score:
                    max_score, result_move = score, init_move
                if max_score >= beta:
                    return max_score, result_move
                alpha = max(alpha, max_score)
            return max_score, result_move
        else:
            min_score = float("inf")
            for m in moves:
                new_game = game.forecast_move(m)
                init_move = m if current_depth is 0 else move
                score, temp_move = self.alpha_beta_helper(new_game, max_depth, True, init_move, current_depth + 1, alpha, beta)
                if score < min_score:
                    min_score, result_move = score, init_move
                if min_score <= alpha:
                    return min_score, result_move
                beta = min(beta, min_score)
            return min_score, result_move

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

        # TODO: finish this function!
        score, move = self.alpha_beta_helper(game, depth, True, None, 0, alpha, beta)
        return move
