from datetime import date, datetime, timedelta

from .convert_to_documents import convert_to_dynamodb_documents
from .sample_data import sample_scores


def test_creates_document_for_every_hour():
    documents = convert_to_dynamodb_documents(
        user_id=1, day=date(2022, 12, 23), activity_scores=sample_scores
    )

    assert len(documents) == 2


def test_passes_user_id_to_all_documents():
    USER_ID = 12345

    documents = convert_to_dynamodb_documents(
        user_id=USER_ID, day=date(2022, 12, 23), activity_scores=sample_scores
    )

    assert all(doc["u"] == USER_ID for doc in documents)


def test_has_all_activity_scores_for_each_hour():
    HOURS_IN_CHUNK = 12
    CHUNK_SIZE = 120 * HOURS_IN_CHUNK

    documents = convert_to_dynamodb_documents(
        user_id=1, day=date(2022, 12, 23), activity_scores=sample_scores
    )

    i = 0
    dt = datetime(2022, 12, 23, 0, 0)
    for doc in documents:
        assert len(doc["v"]) == CHUNK_SIZE
        assert doc["v"] == sample_scores[i : i + CHUNK_SIZE]

        assert doc["t"] == int(dt.timestamp())

        i += CHUNK_SIZE
        dt += timedelta(hours=HOURS_IN_CHUNK)
