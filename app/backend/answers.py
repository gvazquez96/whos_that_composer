import random


def wrong_answers(p, piece_list, gamemode):
    """
    creates new list of pieces without correct answer
    then creates a list of 3 false random answers
    this means that this function assumes a total number of pieces in pieces_list
    of at least 4 pieces (correct answer + 3 false answers)
    """
    new_list = []
    for piece in piece_list:
        if getattr(piece, gamemode) != getattr(p, gamemode) and str(getattr(piece, gamemode)) not in new_list:
            new_list.append(str(getattr(piece, gamemode)))
    false_answers = random.sample(new_list, 3)

    return false_answers


def options_table(answer, wrong_answers):
    """
    returns a joined list of all possible answers
    """

    correct = [answer]
    false = wrong_answers
    complete = correct + false
    random.shuffle(complete)
    return complete
