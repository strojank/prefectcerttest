from capstone import weather_flow
from prefect.deployments import Deployment
from prefect.filesystems import S3
from prefect.orion.schemas.schedules import RRuleSchedule

rr = RRuleSchedule(rrule="FREQ=daily;UNTIL=20221111T040000Z", timezone="America/Chicago")

s3_block = S3.load("capstone-dev")

deploy = Deployment.build_from_flow(
    flow = weather_flow,
    name = "Capstone",
    storage = s3_block,
    schedule = rr,
)

if __name__ == "__main__":
    deploy.apply()