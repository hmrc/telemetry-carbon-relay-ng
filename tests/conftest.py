import datetime
import socket
import time

import docker
import pytest


def current_timestamp() -> int:
    now = datetime.datetime.now()
    return int(now.timestamp())


class MetricHelper:
    def __init__(
        self, carbon_relay_ng_host: str = "localhost", carbon_relay_ng_port: int = 2003
    ) -> None:
        self.clickhouse_container = self.find_clickhouse_container()

        self.carbon_relay_ng_host = carbon_relay_ng_host
        self.carbon_relay_ng_port = carbon_relay_ng_port

    def send_metric(
        self, path: str, value: int | float, timestamp: int = current_timestamp()
    ) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.carbon_relay_ng_host, self.carbon_relay_ng_port))

        message = f"{path} {value} {timestamp}".encode()

        total_sent = 0
        while total_sent < len(message):
            sent = sock.send(message[total_sent:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            total_sent = total_sent + sent

        sock.close()

    def find_clickhouse_container(
        self, container_name: str = "^clickhouse$"
    ) -> docker.models.containers.Container:
        docker_client = docker.from_env()
        containers = docker_client.containers.list(filters={"name": container_name})
        assert len(containers) > 0, "No ClickHouse containers found"
        assert len(containers) == 1, "Multiple ClickHouse containers found"
        return containers[0]

    def exec_query(self, query: str) -> str:
        exit_code, output = self.clickhouse_container.exec_run(
            f'clickhouse-client --query "{query}"'
        )
        return output.decode()

    def get_metric_path_with_value(
        self,
        value: str,
        retry_delay: float = 0.25,
        max_retries: int = 20,
    ) -> str | None:
        for _ in range(1 + max_retries):
            output = self.exec_query(
                f"SELECT Path FROM graphite.graphite WHERE Value = {value}"
            )

            if output != "":
                return output.strip()

            time.sleep(retry_delay)

        return None

    def delete_metrics_with_value(self, value: str):
        self.exec_query(f"DELETE FROM graphite.graphite WHERE Value = {value}")
        assert (
            self.exec_query(f"SELECT Path FROM graphite.graphite WHERE Value = {value}")
            == ""
        )


@pytest.fixture(scope="session")
def metric_helper():
    return MetricHelper()
