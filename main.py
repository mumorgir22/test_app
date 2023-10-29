import asyncio

import pymongo
from datetime import datetime
from dateutil.relativedelta import relativedelta


async def aggregate_salaries(dt_from, dt_upto, group_type):
    dataset = []
    labels = []
    result = {}
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["sampleDB"]
    collection = db["sample_collection"]

    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)
    current_date = dt_from

    if group_type == "hour":
        delta = relativedelta(hours=1)
    elif group_type == "day":
        delta = relativedelta(days=1)
    elif group_type == "month":
        delta = relativedelta(months=1)
    else:
        raise ValueError("Неверный тип агрегации")

    while current_date <= dt_upto:
        next_date = current_date + delta
        result = list(
            collection.aggregate(
                [
                    {"$match": {"dt": {"$gte": current_date, "$lt": next_date}}},
                    {
                        "$group": {
                            "_id": {
                                "year": {"$year": "$date"},
                                "month": {"$month": "$date"},
                                "day": {"$dayOfMonth": "$date"},
                                "hour": {"$hour": "$date"},
                            },
                            "total_salary": {"$sum": "$value"},
                        }
                    },
                ]
            )
        )
        total_salary = sum(item["total_salary"] for item in result)
        dataset.append(total_salary)
        labels.append(current_date.isoformat())
        result = {"dataset": dataset, "labels": labels}
        current_date = next_date
    client.close()
    return result
