import datetime as dt

import pytest

from .sample_data import sample_scores
from ..source.calc_price import (
    calc_costs,
    calc_doc_size,
    calc_int_size,
    calc_list_size,
    calc_doc_request_units,
)


@pytest.mark.parametrize("n, expected_size", [(1, 2), (1_000_000, 5)])
def test_calc_int_size(n, expected_size):
    size = calc_int_size(n)

    assert size == expected_size


@pytest.mark.parametrize("lst, expected_size", [([10], 6), (sample_scores, 8643)])
def test_calc_list_size(lst, expected_size):
    size = calc_list_size(lst)

    assert size == expected_size


@pytest.mark.parametrize(
    "doc, expected_size",
    [
        ({"u": 1, "t": 1693820347, "v": [60, 61, 78]}, 23),
        ({"u": 1_000_000, "t": 1693820347, "v": sample_scores}, 8657),
    ],
)
def test_calc_doc_size(doc, expected_size):
    size = calc_doc_size(doc)

    assert size == expected_size


def test_calc_doc_request_units():
    wru, rru = calc_doc_request_units(
        {"u": 1_000_000, "t": 1693820347, "v": sample_scores}
    )

    assert wru == 9
    assert rru == 3


def test_calc_costs():
    total_cost = calc_costs(
        user_id=1_000_000, day=dt.date(2023, 10, 24), activity_scores=sample_scores
    )

    assert total_cost == "$840.00"
