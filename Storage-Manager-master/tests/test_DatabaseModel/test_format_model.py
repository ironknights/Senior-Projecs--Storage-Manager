"""Code written by Jacquesne Jones unless otherwise specified."""

from src.DatabaseModel.format import get_state_list, get_state_num, get_state, name_last_first, price_format


def test_get_state_list_last_state():
    state_list = get_state_list()
    assert state_list[51][0] == "WY"


def test_get_state_num():
    assert get_state_num("AL") == 1
    assert get_state_num("WY") == 51
    assert get_state_num("Russia") == 0
    assert get_state_num("") == 0


def test_get_state():
    assert get_state(1) == "AL"
    assert get_state(1, True) == "Alabama"
    assert get_state(29) == "NV"


def test_name_last_first():
    assert name_last_first("Smith", "John", "Albert") == "Smith, John A"


def test_price_format():
    assert price_format("50.00") == "$ 50.00"
