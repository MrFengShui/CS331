/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"

using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) : Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    // To be filled in by you
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}

void MinimaxPlayer::utility(OthelloBoard* b)
{
	int player_1_score = b -> count_score(b -> get_p1_symbol());
	int player_2_score = b -> count_score(b -> get_p2_symbol());
	return player_1_score - player_2_score;
}

std::vector<OthelloBoard> MinimaxPlayer::successor(OthelloBoard* b)
{
	std::vector<OthelloBoard> b_vector;
	int i, j;

	for (i = 0; i < b -> col_size(); i++)
	{
		for (j = 0; j < b -> row_size(); j ++)
		{
			if (b -> is_legal_move(i, j, which_symbol))
			{
				b_vector.push_back(OthelloBoard(b));
			}
		}
	}

	return b_vector;
}

void MinimaxPlayer::minimax(OthelloBoard* b, int depth)
{
	std::vector<OthelloBoard> successor = successor(b);
	int value = max_value(b);
	return successor, value;
}

int MinimaxPlayer::max_value(OthelloBoard* b)
{
	if (b -> has_legal_moves_remaining(b -> get_p1_symbol) == false || b -> has_legal_moves_remaining(b -> get_p2_symbol) == false)
	{
		return utility(b);
	}

	std::vector<OthelloBoard> successor = successor(b);
	int value = 9999999, i;

	for (i = 0; i < successor.size(); i ++)
	{
		min_value = min_value(successor[i]);
		value = (value > min_value) ? value : min_value;
	}

	return value;
}

int MinimaxPlayer::min_value(OthelloBoard* b)
{
	if (b -> is_legal_move())
	{
		return utility(b);
	}

	std::vector<OthelloBoard> successor = successor(b);
	int value = 9999999, i;

	for (i = 0; i < successor.size(); i ++)
	{
		max_value = max_value(successor[i]);
		value = (value < max_value) ? value : max_value;
	}

	return value;
}
