from unittest import skip


def paginate(collection, page: int, limit: int, filter_query: dict = {}):
    skip = (page - 1) * limit

    data = list(
        collection.find(filter_query)
        .sort("_id", 1)
        .skip(skip)
        .limit(limit)
    )

    total = collection.count_documents(filter_query)

    return{
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    }