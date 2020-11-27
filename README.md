# collectd_prometheus_scraper
collect metrics from prometheus metrics endpoints using collectd

this is (potentially misguided) attempt scrape prometheus metrics using the collectd python plugin. 

my particular use case is to get these metrics into splunk without using any prometheus infrastructure (dont hold it against me), but i expect this will work for any other collectd write plugin.

any and all feedback welcome!

## config, using the collectd python plugin

```
LoadPlugin python
<Plugin python>
    ModulePath "/opt/collectd"
    LogTraces true
    Import "prometheus_scraper"
    <Module prometheus_scraper>
        Endpoint "http://192.168.0.200:5001/metrics"
        Endpoint_name "docker_registry"
    </Module>
</Plugin>
```


