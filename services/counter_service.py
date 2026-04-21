from pymongo import ReturnDocument

def get_next_student_id(db):
    counter = db["counters"].find_one_and_update(
        {"_id": "student_id"},
        {"$inc": {"sequence_value": 1}},
        return_document=ReturnDocument.AFTER
    )
    return counter["sequence_value"]


def get_next_department_id(db):
    counter = db["counters"].find_one_and_update(
        {"_id": "deptId"},
        {"$inc": {"sequence_value": 1}},
        return_document=ReturnDocument.AFTER
    )
    return counter["sequence_value"]