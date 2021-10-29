import csv
from datetime import datetime, timedelta

from prefect import task, Flow, Parameter
from prefect.schedules import IntervalSchedule


@task(max_retries=5, retry_delay=timedelta(seconds=10))
def extract(path):
    with open(path, "r") as _file:
        text = _file.readline().strip()
    return [int(i) for i in text.split(",")]


@task
def transform(data):
    return [i + 1 for i in data]


@task
def load(path, data):
    with open(path, "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)


def build(schedule=None):
    with Flow("poc-prefect-etl", schedule=schedule) as flow:
        path = Parameter(name="path", required=True)
        extracted = extract(path)
        transformed = transform(extracted)
        load(path, transformed)

    return flow


schedule = IntervalSchedule(
    start_date=datetime.now() - timedelta(seconds=1),
    interval=timedelta(minutes=5)
)

flow = build(schedule=schedule)
# flow.visualize()
flow.run(parameters={
    "path": "./src/values.csv"
})
