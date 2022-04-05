from typing import List, Tuple

values = ["BAR", "виноград", "лимон", "семь"]


def get_score_change(dice_value):

    if dice_value in (1, 22, 43):
        return 7

    elif dice_value in (16, 32, 48):
        return 5

    elif dice_value == 64:
        return 10

    else:
        return -1


def get_combo_text(dice_value: int):

    # return [values[(dice_value - 1) // i % 4]for i in (1, 4, 16)]

    dice_value -= 1
    result = []
    for _ in range(3):
        result.append(values[dice_value % 4])
        dice_value //= 4
    return result


def get_combo_data(dice_value: int):

    return (
        get_score_change(dice_value),
        ', '.join(get_combo_text(dice_value))
    )
