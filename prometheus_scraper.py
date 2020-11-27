import platform
import collectd
from prometheus_client.parser import text_string_to_metric_families
import requests

def config_func(config):
    endpoint_set = False
    endpoint_set = False
    interval = 60

    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key.lower() == 'endpoint':
            endpoint = val
            endpoint_set = True
        elif key.lower() == 'endpoint_name':
            endpoint_name = val
            endpoint_name_set = True
        elif key.lower() == 'interval':
            interval = val
        else:
            collectd.info(f'prometheus_scraper: Unknown config key "{key}"')


    if endpoint_set and endpoint_name_set:
        collectd.info(f'prometheus_scraper: python version {platform.python_version()}')
        collectd.info(f'prometheus_scraper: Using {endpoint} for {endpoint_name} on ')

        global ENDPOINT
        ENDPOINT = endpoint
        global ENDPOINT_NAME
        ENDPOINT_NAME = endpoint_name
        global INTERVAL
        INTERVAL = interval


def parse_func(metrics):

    for family in text_string_to_metric_families(metrics):
        for sample in family.samples:

            if family.type == 'summary':
                print(family.type)
                pass
            elif family.type == 'histogram':
                print(family.type)
                pass
            else:
                val = collectd.Values()
                val.plugin = ENDPOINT_NAME
                val.interval = INTERVAL
                val.type = family.type

                if len(sample.labels) > 0:
                    joined = ''.join(key + '_' + str(val) for key, val in sample.labels.items())
                    val.type_instance = sample.name + '.' + joined
                else:
                    val.type_instance = sample.name

                print(f'type_instance: {val.type_instance}')

                val.values = [sample.value]
                val.dispatch()


def read_func():

    try:
        metrics = requests.get(url=ENDPOINT)
        metrics.raise_for_status()
        parse_func(metrics.text)
    except requests.exceptions.RequestException as e:
        collectd.error(f'failed to retrive metrics: {e}')


collectd.register_config(config_func)
collectd.register_read(read_func, INTERVAL)
