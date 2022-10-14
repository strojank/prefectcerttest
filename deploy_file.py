from flow_101 import weather_flow
from prefect.deployments import Deployment
from prefect.filesystems import S3
from prefect.filesystems import GitHub

github_block = GitHub.load("ghtest")

s3_block = S3.load("prefecttestks")

deploy = Deployment.build_from_flow(
    flow = weather_flow,
    name = "Python deploy file",
    storage = github_block,
)

if __name__ == "__main__":
    deploy.apply()