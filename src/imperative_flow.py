import httpx
import csv

from prefect import task, Task, Flow
from prefect.tasks.shell import ShellTask
from prefect.executors import DaskExecutor



class Extract(Task):
    def __init__(self, path: str, **kwargs):
        self.path = path
        self.data = None
        super().__init__(**kwargs)

    def do_somethig(self):
        with httpx.Client() as client:
            response = client.get(self.path)

        self.logger.info(f"{response}")
        self.data = response

    def get_data(self):
        return self.data

    def run(self):
        self.logger.info("saving reference data...")
        self.do_somethig()


class Transform(Task):

    def __init__(self, data = None, **kwargs):
        self.data = data
        super().__init__(**kwargs)

    def do_some_data_tranformation(self):
        self.logger.info(f"Doing something with the received data {self.data}")

    def run(self):
        self.do_some_data_tranformation()



class Load(Task):

    def __init__(self, data, **kwargs):
        self.data = data
        super().__init__(**kwargs)

    def do_some_with_tranformed_data():
        print(f"Doing something with the transformed data {self.data}")

    def run(self):
        self.do_some_with_tranformed_data()


class ShowOutput(Task):
    def run(self, std_out):
        print(std_out)


# ls_task = ShellTask(command="ls", return_all=True)
# show_output = ShowOutput()

# flow = Flow("list_files")
# show_output.set_upstream(ls_task, key="std_out", flow=flow)

# flow.run()

flow = Flow("My Imperative flow")

extract = Extract(path="https://httpbin.org/status/200")
extracted_data = extract.data

transform = Transform()
# transform.bind(data=extracted_data)

flow.set_dependencies(
    task=transform,
    upstream_tasks=[extract]
)

# load = Load(data=[10])
# flow.set_dependencies(
#     task=load,
#     upstream_tasks=[Transform(data=[10])]
# )

# flow.visualize()
if __name__=="__main__":
    flow.run(executor=DaskExecutor())

# with Flow("poc-prefect-etl") as flow:
#     etl = ETL()
#     etl.extract()
#     etl.transform()
#     etl.load()
