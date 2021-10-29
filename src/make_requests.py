import httpx
import prefect

from datetime import datetime, timedelta

from prefect import task, Flow, Parameter
from prefect.schedules import IntervalSchedule

# Defines the scheduler interval
schedule = IntervalSchedule(
    start_date=datetime.now() - timedelta(seconds=1),
    interval=timedelta(seconds=1)
)

@task(tags=["web"])
def retrieve_url(url):
    """
    Given a URL (string), retrieves html and
    returns the html as a string.
    """
    logger = prefect.context.get("logger")

    def make_request():
        logger.info("Making a request")
        with httpx.Client() as client:
            response = client.get(url)

        logger.info(f"{response}")
        return response

    response = make_request()

    if response.ok:
        return response.text
    else:
        raise ValueError("{} could not be retrieved.".format(url))



def build_flow(schedule=None):
    with Flow("make-requests", schedule=schedule) as flow:
        retrieve_url("https://httpbin.org/status/200")

    return flow


flow = build_flow(schedule=schedule)

# flow.visualize()
# flow.run(parameters={
#     "path": "./src/values.csv"
# })

# flow.register("requests-flow")
flow.run()
