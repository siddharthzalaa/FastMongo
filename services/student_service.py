def student_helper(student) -> dict:
    if not student:
        return None

    return {
        "id": str(student.get("_id")),
        "name": student.get("name"),
        "age": student.get("age"),
        "hobbies": student.get("Hobbies", []),
        "bio": student.get("bio"),
        "identity": student.get("identity"),
        "experience": student.get("experience"),
        "student_id": student.get("student_id"),
        "department_id": student.get("department_id")
    }