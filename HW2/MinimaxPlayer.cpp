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

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row)
{
    // To be filled in by you
	which_symbol = symbol;
	MinimaxPlayer::OthelloBoardState best_state = minimax_decision(b, col, row);
	col = best_state.column;
	row = best_state.row;
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}

bool MinimaxPlayer::is_over(OthelloBoard* b)
{
	bool flag_1 = b -> has_legal_moves_remaining(b -> get_p1_symbol()) == false;
	bool flag_2 = b -> has_legal_moves_remaining(b -> get_p2_symbol()) == false;
	return flag_1 || flag_2;
}

int MinimaxPlayer::utility(OthelloBoard* b)
{
	int player_1_score = b -> count_score(b -> get_p1_symbol());
	int player_2_score = b -> count_score(b -> get_p2_symbol());
	return player_1_score - player_2_score;
}

std::vector<MinimaxPlayer::OthelloBoardState> MinimaxPlayer::successor(OthelloBoard* b)
{
	std::vector<MinimaxPlayer::OthelloBoardState> b_vector;
	OthelloBoardState *state;
	int i, j;

	for (i = 0; i < b -> get_num_cols(); i++)
	{
		for (j = 0; j < b -> get_num_rows(); j ++)
		{
			if (b -> is_legal_move(i, j, which_symbol))
			{
				state = new OthelloBoardState;
				state -> board = new OthelloBoard(*b);
				state -> board -> play_move(i, j, which_symbol);
				state -> column = i;
				state -> row = j;
				state -> value = -1;
				b_vector.push_back(*state);
			}
		}
	}

	return b_vector;
}

MinimaxPlayer::OthelloBoardState MinimaxPlayer::minimax_decision(OthelloBoard* b, int& col, int& row)
{
	int move = 999999999, i, best;
	std::vector<MinimaxPlayer::OthelloBoardState> state_vec = successor(b);

	for (i = 0; i < state_vec.size(); i ++)
	{
		int tmp_value = max_value(state_vec[i].board);

		if (tmp_value < move)
		{
			move = tmp_value;
			best = i;
		}
	}

	return state_vec[best];
}

int MinimaxPlayer::max_value(OthelloBoard* b)
{
	if (is_over(b))
	{
		return utility(b);
	}

	std::vector<MinimaxPlayer::OthelloBoardState> state_vec = successor(b);
	int value = -100, i;
	which_symbol = b -> get_p2_symbol();

	for (i = 0; i < state_vec.size(); i ++)
	{
		int tmp_value = min_value(state_vec[i].board);
		value = std::max(value, tmp_value);
	}

	return value;
}

int MinimaxPlayer::min_value(OthelloBoard* b)
{
	if (is_over(b))
	{
		return utility(b);
	}

	std::vector<MinimaxPlayer::OthelloBoardState> state_vec = successor(b);
	int value = 100, i;
	which_symbol = b -> get_p1_symbol();

	for (i = 0; i < state_vec.size(); i ++)
	{
		int tmp_value = max_value(state_vec[i].board);
		value = std::min(value, tmp_value);
	}

	return value;
}
