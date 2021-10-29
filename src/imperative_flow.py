import httpx
import csv

from prefect import task, Task, Flow


class Extract(Task):
    def __init__(self, source: str = "local", path: str = "./etl", **kwargs):
        self.source = source
        self.path = path
        super().__init__(**kwargs)

    def run(self):
        data = None
        if self.source == "remote":
            with httpx.Client() as client:
                data = client.get(self.path).json()
        else:
            with open(f"{self.path}/values.csv", "r") as _file:
                text = _file.readline().strip()
            data = [int(i) for i in text.split(",")]

        return data


class Transform(Task):

    def __init__(self, data, **kwargs):
        self.data = data
        super().__init__(**kwargs)

    def run(self):
        return [i + 1 for i in self.data]


class Load(Task):

    def __init__(self, data, path: str = "./src", **kwargs):
        self.data = data
        self.path = path
        super().__init__(**kwargs)

    def run(self):
        with open(f"{self.path}/transformed_values.csv", "w") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(self.data)


class ETL(Task):

    def __init__(self, source: str = "local", path: str = "./etl", **kwargs):
        self.source = source
        self.path = path
        self.data = None
        self.transformed_data = None

        super().__init__(**kwargs)

    def extract(self):
        print(f"Extracting from {self.source} source")
        if self.source == "remote":
            with httpx.Client() as client:
                self.data = client.get(self.path).json()
        else:
            with open(f"{self.path}/values.csv", "r") as _file:
                text = _file.readline().strip()
            self.data = [int(i) for i in text.split(",")]


    def transform(self):
        print(f"Transforming: {self.data}")
        self.transformed_data = [i + 1 for i in self.data]


    def load(self):
        with open(f"{self.path}/transformed_values.csv", "w") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(self.transformed_data)

    def run(self):
        self.extract()
        self.transform()
        self.load()


flow = Flow("My Imperative flow")

transform = Transform(data=[10])
flow.set_dependencies(
    task=transform,
    upstream_tasks=[Extract()]

)

load = Load(data=[10])
flow.set_dependencies(
    task=load,
    upstream_tasks=[Transform(data=[10])]
)

flow.visualize()

# flow.run()

# with Flow("poc-prefect-etl") as flow:
#     etl = ETL()
#     etl.extract()
#     etl.transform()
#     etl.load()
