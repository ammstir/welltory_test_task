import datetime as dt


def convert_to_dynamodb_documents(
    user_id: int, day: dt.date, activity_scores: list[int]
) -> list[dict[str, int | list[int]]]:
    # every minute is 30 sec * 2, 60 min in hour, total 12 hours
    HOURS_IN_CHUNK = 12
    CHUNK_SIZE = 120 * HOURS_IN_CHUNK

    total_scores_amount = len(activity_scores)
    # convert to datetime with start at midnight
    current_time = dt.datetime.combine(day, dt.datetime.min.time())

    documents = []
    # generate docs for every hours segment with start at 00 min
    for i in range(0, total_scores_amount, CHUNK_SIZE):
        scores = activity_scores[i : i + CHUNK_SIZE]
        doc = {
            "u": user_id,
            "t": int(current_time.timestamp()),  # Convert to UNIX timestamp
            "v": scores,
        }
        documents.append(doc)
        # go to next hours segment
        current_time += dt.timedelta(hours=HOURS_IN_CHUNK)

    return documents
