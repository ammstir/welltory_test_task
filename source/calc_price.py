import datetime as dt
from math import ceil

from .convert_to_documents import convert_to_dynamodb_documents


def calc_int_size(n: int) -> int:
    # Size of int = (1 byte per every 2 digits) + 1 byte
    return ceil(len(str(n)) / 2) + 1


def calc_list_size(l: list[int]) -> int:
    # Size of list of ints = (size of all elements) + (elements amount) + 3 bytes
    items_size = sum(calc_int_size(n) for n in l)

    return items_size + len(l) + 3


def calc_doc_size(doc: dict[str, int | list[int]]) -> int:
    # returns total bytes amount for document
    # attribute size = (len of key name) + (value size)
    return sum(
        [
            1,  # len of key "u"
            calc_int_size(doc["u"]),
            1,  # len of key "t"
            calc_int_size(doc["t"]),
            1,  # len of key "v"
            calc_list_size(doc["v"]),
        ]
    )


def calc_doc_request_units(doc: dict) -> tuple[int, int]:
    size = calc_doc_size(doc)
    # 1 WRU per whole 1 KB
    wru = ceil(size / 1024)
    # 1 RRU per whole 4 KB
    rru = ceil(size / 4096)

    return wru, rru


def calc_costs(user_id: int, day: dt.date, activity_scores: list[int]) -> str:
    USERS = 1_000_000
    DAYS_IN_MONTH = 30
    WRU_PRICE = 1.25 / 1e6  # per WRU
    RRU_PRICE = 0.25 / 1e6  # per RRU

    # writing happens once a day
    total_writes_per_day = USERS * 2  # 2 docs per user in a day
    total_writes_per_month = total_writes_per_day * DAYS_IN_MONTH

    # for 1 hour report we need 1 document, request happens once a day
    hourly_reads_per_day = USERS
    hourly_reads_per_month = hourly_reads_per_day * DAYS_IN_MONTH

    # for 12 hour report we need 2 documents (worst case scenario)
    # request happens once a day
    twelve_hour_reads_per_day = USERS * 2
    twelve_hour_reads_per_month = twelve_hour_reads_per_day * DAYS_IN_MONTH

    # generate docs for DB per user per day
    docs = convert_to_dynamodb_documents(
        user_id=user_id, day=day, activity_scores=activity_scores
    )

    # calc request units per user docs per day
    total_wru_per_user = 0
    total_rru_per_user = 0
    for doc in docs:
        wru_per_user, rru_per_user = calc_doc_request_units(doc)
        total_rru_per_user += rru_per_user
        total_wru_per_user += wru_per_user

    # do the math
    write_cost_per_user = total_wru_per_user * WRU_PRICE
    read_cost_per_user = total_rru_per_user * RRU_PRICE

    total_writes_cost = total_writes_per_month * write_cost_per_user
    total_twelve_hour_reads_cost = twelve_hour_reads_per_month * read_cost_per_user
    total_hourly_reads_cost = hourly_reads_per_month * read_cost_per_user

    total_cost = (
        total_writes_cost + total_hourly_reads_cost + total_twelve_hour_reads_cost
    )

    return "${:.2f}".format(total_cost)
