def histogram(lst):
    hist = {}
    for item in lst:
        hist[item] = hist.get(item, 0) + 1
    return hist

def is_rank_sequence(hand):
    rank_order = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    ranks = [card[0] for card in hand]

    if all(rank in ranks for rank in ['A', '2', '3', '4', '5']):
        ranks = ['1' if rank == 'A' else rank for rank in ranks]

    rank_indices = [rank_order.index(rank) for rank in ranks]
    rank_indices.sort()

    return rank_indices == list(range(rank_indices[0], rank_indices[0] + 5))

def hand_rank(hand):
    hand_rank_list = [card[0] for card in hand]
    hand_color_list = [card[1] for card in hand]

    hand_rank_histogram = histogram(hand_rank_list)
    hand_color_histogram = histogram(hand_color_list)

    is_hand_rank_seq = is_rank_sequence(hand)

    if (5 in hand_color_histogram.values()) and ('A' in hand_rank_list) and is_hand_rank_seq:
        return 10
    elif (5 in hand_color_histogram.values()) and is_hand_rank_seq:
        return 9
    elif 4 in hand_rank_histogram.values():
        return 8
    elif sorted(hand_rank_histogram.values()) == [2, 3]:
        return 7
    elif 5 in hand_color_histogram.values():
        return 6
    elif is_hand_rank_seq:
        return 5
    elif 3 in hand_rank_histogram.values():
        return 4
    elif list(hand_rank_histogram.values()).count(2) == 2:
        return 3
    elif 2 in hand_rank_histogram.values():
        return 2
    else:
        return 1
