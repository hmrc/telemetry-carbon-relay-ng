import dataclasses

import pytest

@dataclasses.dataclass
class EnvoyTask:
    instance_id: str
    task_id: str
    zone: str

@dataclasses.dataclass
class MicroserviceTask(EnvoyTask):
    service_name: str

@dataclasses.dataclass
class IngressGatewayTask(EnvoyTask):
    shard: int

@dataclasses.dataclass
class ConsulAPIGatewayTask(EnvoyTask):
    datacenter: str
    consul_uuid: str



@pytest.mark.parametrize(
    "ingress_gateway_task, metric_type, metric_path",
    [
        (
            IngressGatewayTask(
                instance_id="i-9693b71f972105d0f",
                task_id="944a78e9ba1c2423894a3c0d51e935b5",
                zone="protected",
                shard=0,
            ),
            "gauge",
            "cluster.cds_egress_mdtp-app-mesh_platform-status-backend-protected_http_8080.membership_total",
        ),
        (
            IngressGatewayTask(
                instance_id="i-b77c49bfcf8f3b8aa",
                task_id="aef738ef6e54b9d23cb072a787f616a4",
                zone="protected-rate",
                shard=3,
            ),
            "counter",
            "control_plane.connected_state",
        ),
        (
            IngressGatewayTask(
                instance_id="i-3e135ef4cbe766e37",
                task_id="22ff9155c7c045f4ff9179b5bb25b24d",
                zone="public-monolith",
                shard=1,
            ),
            "timing",
            "http.ingress.downstream_rq_5xx",
        ),
    ],
)
def test_rewrite_ingressgateway_envoy_metrics(
    ingress_gateway_task,
    metric_type,
    metric_path,
    metric_helper,
):
    value = 1000000001

    original_path = f"telegraf.{ingress_gateway_task.instance_id}.{metric_type}.envoy.ingressgateway-{ingress_gateway_task.zone}-{ingress_gateway_task.shard}.{ingress_gateway_task.task_id}.{metric_path}"
    expected_path = f"microservice.ingressgateway-{ingress_gateway_task.zone}.{ingress_gateway_task.task_id}.envoy.{metric_type}.{metric_path}"

    metric_helper.delete_metrics_with_value(value)
    metric_helper.send_metric(original_path, value)
    assert metric_helper.get_metric_path_with_value(value) == expected_path


@pytest.mark.parametrize(
    "microservice_task, metric_type, metric_path",
    [
        (
            MicroserviceTask(
                instance_id="i-9693b71f972105d0f",
                task_id="944a78e9ba1c2423894a3c0d51e935b5",
                zone="protected",
                service_name="platform-status-backend",
            ),
            "gauge",
            "cluster_ingress_http_8080.upstream_rq_time.90_percentile",
        ),
        (
            MicroserviceTask(
                instance_id="i-b77c49bfcf8f3b8aa",
                task_id="aef738ef6e54b9d23cb072a787f616a4",
                zone="protected-rate",
                service_name="back-office-adapter",
            ),
            "counter",
            "cluster_ingress_http_8080.upstream_rq_[2345][0-9][0-9]",
        ),
        (
            MicroserviceTask(
                instance_id="i-3e135ef4cbe766e37",
                task_id="22ff9155c7c045f4ff9179b5bb25b24d",
                zone="public-monolith",
                service_name="classic-helpdesk-proxy",
            ),
            "timing",
            "cluster_ingress_http_8080.upstream_rq_{400,401,403,404,500,502,503,504}",
        ),
    ],
)
def test_rewrite_envoy_microservice(
    microservice_task,
    metric_type,
    metric_path,
    metric_helper,
):
    value = 1000000002

    virtual_node_name = f"{microservice_task.service_name}-{microservice_task.zone}"

    original_path = f"telegraf.{microservice_task.instance_id}.{metric_type}.envoy.{virtual_node_name}.{microservice_task.task_id}.{metric_path}"
    expected_path = (
        f"microservice.{microservice_task.service_name}.{microservice_task.task_id}.envoy.{metric_type}.{metric_path}"
    )

    metric_helper.delete_metrics_with_value(value)
    metric_helper.send_metric(original_path, value)
    assert metric_helper.get_metric_path_with_value(value) == expected_path


@pytest.mark.parametrize(
    "api_gateway_task, service_name, metric_type, metric_path",
    [
        (
            ConsulAPIGatewayTask(
                instance_id="i-9693b71f972105d0f",
                task_id="ac7bdf74f13327b6e352481485f431f8",
                zone="protected",
                datacenter="integration",
                consul_uuid="34267186-43f7-4d2d-9efc-77227297f0a9",
            ),
            "platform-status-backend",
            "gauge",
            "membership_total",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-b77c49bfcf8f3b8aa",
                task_id="c37e1f1599eb99e776655a34af2cbb4e",
                zone="protected-rate",
                datacenter="production",
                consul_uuid="1dc4b725-b32c-4556-ad45-e480acc70ca1",
            ),
            "back-office-adapter",
            "counter",
            "upstream_rq_retry",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-3e135ef4cbe766e37",
                task_id="ceb827fcc79c8848ff539494f0c57eb7",
                zone="public-monolith",
                datacenter="staging",
                consul_uuid="980406b3-f90e-4031-9562-a7a556cf3842",
            ),
            "classic-helpdesk-proxy",
            "timing",
            "upstream_rq_time",
        ),
    ],
)
def test_rewrite_envoy_consul_apigw(
    api_gateway_task,
    service_name,
    metric_type,
    metric_path,
    metric_helper,
):
    value = 1000000003

    original_path = f"telegraf.{api_gateway_task.instance_id}.{metric_type}.envoy.consul-apigw.{api_gateway_task.datacenter}.{api_gateway_task.zone}.{api_gateway_task.task_id}.cluster.{service_name}-{api_gateway_task.zone}.default.{api_gateway_task.datacenter}.internal.{api_gateway_task.consul_uuid}.consul.{metric_path}"
    expected_path = f"microservice.consul-apigw-{api_gateway_task.datacenter}-{api_gateway_task.zone}.{api_gateway_task.task_id}.envoy.{metric_type}.cluster.{service_name}-{api_gateway_task.zone}.default.{api_gateway_task.datacenter}.internal.{api_gateway_task.consul_uuid}.consul.{metric_path}"

    metric_helper.delete_metrics_with_value(value)
    metric_helper.send_metric(original_path, value)
    assert metric_helper.get_metric_path_with_value(value) == expected_path


@pytest.mark.parametrize(
    "api_gateway_task, service_name, metric_type, metric_path",
    [
        (
            ConsulAPIGatewayTask(
                instance_id="i-9693b71f972105d0f",
                task_id="ac7bdf74f13327b6e352481485f431f8",
                zone="protected",
                datacenter="integration",
                consul_uuid="34267186-43f7-4d2d-9efc-77227297f0a9",
            ),
            "platform-status-backend",
            "gauge",
            "membership_total",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-b77c49bfcf8f3b8aa",
                task_id="c37e1f1599eb99e776655a34af2cbb4e",
                zone="protected-rate",
                datacenter="production",
                consul_uuid="1dc4b725-b32c-4556-ad45-e480acc70ca1",
            ),
            "back-office-adapter",
            "counter",
            "upstream_rq_retry",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-3e135ef4cbe766e37",
                task_id="ceb827fcc79c8848ff539494f0c57eb7",
                zone="public-monolith",
                datacenter="staging",
                consul_uuid="980406b3-f90e-4031-9562-a7a556cf3842",
            ),
            "classic-helpdesk-proxy",
            "timing",
            "upstream_rq_time",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-3a6695138a3b377a1",
                task_id="6639bc62629822a74d9572cf0b0c4338",
                zone="public-monolith",
                datacenter="engineer-environment",
                consul_uuid="121e9ca8-5a0e-4804-b004-91e1a3f46984",
            ),
            "classic-helpdesk-proxy",
            "timing",
            "upstream_rq_time",
        ),
    ],
)
def test_rewrite_envoy_consul_apigw_app_mesh_compatibility_cluster_name(
    api_gateway_task,
    service_name,
    metric_type,
    metric_path,
    metric_helper,
):
    """
    Test that Consul API gateway App Mesh compatibility metrics are rewritten with App Mesh cluster names
    """
    value = 1000000004

    original_path = f"telegraf.{api_gateway_task.instance_id}.{metric_type}.app-mesh-compat.envoy.consul-apigw.{api_gateway_task.datacenter}.{api_gateway_task.zone}.{api_gateway_task.task_id}.cluster.{service_name}-{api_gateway_task.zone}.default.{api_gateway_task.datacenter}.internal.{api_gateway_task.consul_uuid}.consul.{metric_path}"
    expected_path = f"microservice.ingressgateway-{api_gateway_task.zone}.consul-{api_gateway_task.task_id}.envoy.{metric_type}.cluster.cds_egress_mdtp-app-mesh_{service_name}-{api_gateway_task.zone}_http_8080.{metric_path}"

    metric_helper.delete_metrics_with_value(value)
    metric_helper.send_metric(original_path, value)
    assert metric_helper.get_metric_path_with_value(value) == expected_path


@pytest.mark.parametrize(
    "api_gateway_task, metric_type, metric_path",
    [
        (
            ConsulAPIGatewayTask(
                instance_id="i-9693b71f972105d0f",
                task_id="ac7bdf74f13327b6e352481485f431f8",
                zone="protected",
                datacenter="integration",
                consul_uuid="34267186-43f7-4d2d-9efc-77227297f0a9",
            ),
            "gauge",
            "http.ingress_upstream_zone-wildcard.downstream_rq_5xx",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-b77c49bfcf8f3b8aa",
                task_id="c37e1f1599eb99e776655a34af2cbb4e",
                zone="protected-rate",
                datacenter="production",
                consul_uuid="1dc4b725-b32c-4556-ad45-e480acc70ca1",
            ),
            "counter",
            "http.ingress_upstream_zone-wildcard.downstream_rq_2xx",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-3e135ef4cbe766e37",
                task_id="ceb827fcc79c8848ff539494f0c57eb7",
                zone="public-monolith",
                datacenter="staging",
                consul_uuid="980406b3-f90e-4031-9562-a7a556cf3842",
            ),
            "timing",
            "grpc.ads.streams_closed_0",
        ),
        (
            ConsulAPIGatewayTask(
                instance_id="i-3a6695138a3b377a1",
                task_id="6639bc62629822a74d9572cf0b0c4338",
                zone="public-monolith",
                datacenter="engineer-environment",
                consul_uuid="121e9ca8-5a0e-4804-b004-91e1a3f46984",
            ),
            "timing",
            "http.ingress_upstream_zone-wildcard.downstream_rq_time.50_percentile",
        ),
    ],
)
def test_rewrite_envoy_consul_apigw_app_mesh_compatibility_other(
    api_gateway_task, metric_type, metric_path, metric_helper
):
    """
    Test that Consul API gateway App Mesh compatibility metrics are rewritten to match App Mesh metric paths
    """
    value = 1000000005

    original_path = f"telegraf.{api_gateway_task.instance_id}.{metric_type}.app-mesh-compat.envoy.consul-apigw.{api_gateway_task.datacenter}.{api_gateway_task.zone}.{api_gateway_task.task_id}.{metric_path}"
    expected_path = f"microservice.ingressgateway-{api_gateway_task.zone}.consul-{api_gateway_task.task_id}.envoy.{metric_type}.{metric_path}"

    metric_helper.delete_metrics_with_value(value)
    metric_helper.send_metric(original_path, value)
    assert metric_helper.get_metric_path_with_value(value) == expected_path


@pytest.mark.parametrize(
    "microservice_task, metric_type, metric_path",
    [
        (
            MicroserviceTask(
                instance_id="i-9693b71f972105d0f",
                task_id="944a78e9ba1c2423894a3c0d51e935b5",
                zone="protected",
                service_name="platform-status-backend",
            ),
            "gauge",
            "membership_total",
        ),
        (
            MicroserviceTask(
                instance_id="i-b77c49bfcf8f3b8aa",
                task_id="aef738ef6e54b9d23cb072a787f616a4",
                zone="protected-rate",
                service_name="back-office-adapter",
            ),
            "counter",
            "upstream_rq_retry",
        ),
        (
            MicroserviceTask(
                instance_id="i-3e135ef4cbe766e37",
                task_id="22ff9155c7c045f4ff9179b5bb25b24d",
                zone="public-monolith",
                service_name="classic-helpdesk-proxy",
            ),
            "timing",
            "upstream_rq_time",
        ),
        (
            MicroserviceTask(
                instance_id="i-3e135ef4cbe766e37",
                task_id="22ff9155c7c045f4ff9179b5bb25b24d",
                zone="public-monolith",
                service_name="classic-helpdesk-proxy",
            ),
            "timing",
            "upstream_rq_time",
        ),
    ],
)
def test_rewrite_envoy_consul_microservice_app_mesh_compatibility_cluster_name(
    microservice_task,
    metric_type,
    metric_path,
    metric_helper,
):
    """
    Test that microservice App Mesh compatibility metrics are rewritten with App Mesh cluster names
    """
    value = 1000000006

    original_path = f"telegraf.{microservice_task.instance_id}.{metric_type}.app-mesh-compat.envoy.{microservice_task.service_name}.{microservice_task.zone}.{microservice_task.task_id}.cluster.local_app.{metric_path}"
    expected_path = f"microservice.{microservice_task.service_name}.consul-{microservice_task.task_id}.envoy.{metric_type}.cluster.cluster_ingress_http_8080.{metric_path}"

    metric_helper.delete_metrics_with_value(value)
    metric_helper.send_metric(original_path, value)
    assert metric_helper.get_metric_path_with_value(value) == expected_path


def test_rewrite_cip(metric_helper):
    value = 1000000007

    original_path = "telegraf.ip-10-64-28-152_eu-west-2_compute_internal.arn:aws:ecs:eu-west-2:893166705434:cluster-paas-3094.arn:aws:ecs:eu-west-2:893166705434:cluster-paas-3094.fluentbit.cip-hello-flask-3094-blue.687b8171da1349069b1f94e69da30153-3040842310.fluentbit.1.arn:aws:ecs:eu-west-2:893166705434:task-paas-3094-687b8171da1349069b1f94e69da30153.ecs_container_mem.hierarchical_memory_limit"
    expected_path = "cip.metrics.ecs.paas-3094.cip-hello-flask-3094.blue.687b8171da1349069b1f94e69da30153.fluentbit.ecs_container_mem.hierarchical_memory_limit"

    metric_helper.delete_metrics_with_value(value)
    metric_helper.send_metric(original_path, value)
    assert metric_helper.get_metric_path_with_value(value) == expected_path
