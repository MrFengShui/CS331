/*
 * MinimaxPlayer.h
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */

#ifndef MINIMAXPLAYER_H
#define MINIMAXPLAYER_H

#include "OthelloBoard.h"
#include "Player.h"
#include <vector>

/**
 * This class represents an AI player that uses the Minimax algorithm to play the game
 * intelligently.
 */
class MinimaxPlayer : public Player {
public:

	/**
	 * @param symb This is the symbol for the minimax player's pieces
	 */
	MinimaxPlayer(char symb);

	/**
	 * Destructor
	 */
	virtual ~MinimaxPlayer();

	/**
	 * @param b The board object for the current state of the board
	 * @param col Holds the return value for the column of the move
	 * @param row Holds the return value for the row of the move
	 */
    void get_move(OthelloBoard* b, int& col, int& row);

    /**
     * @return A copy of the MinimaxPlayer object
     * This is a virtual copy constructor
     */
    MinimaxPlayer* clone();

private:

	char which_symbol;

	struct OthelloBoardState
	{
		int column, row, value;
		OthelloBoard* board;
	};

	/**
	 * @param b The board object for the current state of the board
	 */
	bool is_over(OthelloBoard* b);

	/**
	 * @param b The board object for the current state of the board
	 */
	int utility(OthelloBoard* b);

	/**
	 * @param b The board object for the current state of the board
	 */
	std::vector<OthelloBoardState> successor(OthelloBoard* b);

	/**
	 * @param b The board object for the current state of the board
	 * @param col Holds the return value for the column of the move
	 * @param row Holds the return value for the row of the move
	 */
	MinimaxPlayer::OthelloBoardState minimax_decision(OthelloBoard *b, int& col, int& row);

	/**
	 * @param b The board object for the current state of the board
	 */
	int max_value(OthelloBoard* b);

	/**
	 * @param b The board object for the current state of the board
	 */
	int min_value(OthelloBoard* b);

};


#endif
