from flow_101 import weather_flow
from prefect.deployments import Deployment
from prefect.filesystems import S3
from prefect.filesystems import GitHub
from prefect.infrastructure import Process
from prefect.infrastructure.docker import DockerContainer

#docker_container_block = DockerContainer.load("localdockertest")


infra = Process.load("processtest")
#github_block = GitHub.load("ghtest")

s3_block = S3.load("prefecttestks")

deploy = Deployment.build_from_flow(
    flow = weather_flow,
    name = "Python deploy file",
    storage = s3_block,
    infrastructure = infra,
    #infrastructure = docker_container_block
)

if __name__ == "__main__":
    deploy.apply()