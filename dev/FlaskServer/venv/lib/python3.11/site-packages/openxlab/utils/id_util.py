import uuid


def generate_unique_id(length):
    """
    get fixed length uuid
    """
    unique_id = str(uuid.uuid4().int)
    unique_id = unique_id[:length]
    return unique_id
