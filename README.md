# OSRS Wiki prices API wrapper
Wrapper for the OSRS wiki prices API

# Usage
Initialize the API class with a user agent and contact as arguments

`api = PricesAPI("DESCRIPTION OF APP HERE", "CONTACT ADDRESS HERE")`

## Retrieve the latest available prices

`latest = api.latest()`

`latest_mapped = api.latest(mapping=True)`

The mapping argument adds additional information about each item (available from the /mapping endpoint) to the return value.

It is also possible to return the prices as a pandas dataframe:

`latest_df = api.latest_df(mapping=True)`

## Retrieve volumes

`volumes = api.volumes(mapping=True)`

`volumes_df = api.volumes_df(mapping=True)`


## Retrieve timed pricing data
`prices = api.prices("5m", mapping=True)`

`prices_df = api.prices_df("5m", mapping=True)`

Valid time values are: `5m`, `1h`, `6h` and `24h`

## Retrieve time series data
`timeseries = api.timeseries("5m", 2)`

`timeseries_df = api.timeseries_df("5m", 2)`

The first argument is the time interval, second argument is the item ID

Valid time values are: `5m`, `1h`, `6h` and `24h`

## Retrieve mapping data
`mapping = api.mapping()`

`mapping_df = api.mapping_df()`




