import yaml
from sys import maxsize
from darksky import DarkSky
from yeelight import SmartBulb, Flow, RGBTransition, SleepTransition

def get_forecast():
    '''
    Returns forecast for configured timeframe
    '''
    darksky = DarkSky(config['darksky']['apikey'])
    forecast = darksky.get(config['forecast']['location']['latitude'], config['forecast']['location']['longitude'])
    timeframe = config['forecast']['timeframe']

    if timeframe == 0:
        forecast = [forecast.currently]
    else:
        forecast = forecast.hourly.data[:timeframe]

    temperature = mean(list(map(lambda hour: hour.apparentTemperature, forecast)))
    condition = get_most_significant_condition(list(map(lambda hour: hour.icon, forecast)))

    return {
        'temperature': temperature,
        'condition': condition
    }

def mean(numbers):
    '''
    Returns mean for list of numbers
    '''
    return float(sum(numbers)) / max(len(numbers), 1)

def get_most_significant_condition(conditions):
    '''
    Returns the most significant condition from provided list
    '''
    weighted_conditions = ['clear-day', 'clear-night', 'partly-cloudy-day', 'partly-cloudy-night', 'cloudy', 'fog', 'wind', 'rain', 'sleet', 'snow', 'hail', 'thunderstorm', 'tornado']
    conditions.sort(key=lambda condition: weighted_conditions.index(condition))

    return conditions[-1]

def get_temperature_color(temp):
    '''
    Returns the color for the provided temperature
    '''
    is_temp_in_range = lambda color: temp >= color.get('min', -maxsize) and temp < color.get('max', maxsize)
    is_default = lambda color: color.get('default', False)

    colors = config['lightshow']['temperature']['colors']
    default = next(filter(is_default, colors), {})
    color = next(filter(is_temp_in_range, colors), default)

    return color.get('rgb')

def get_condition_color(condition):
    '''
    Returns the color for the provided condition
    '''
    is_condition_in_list = lambda color: condition in color.get('icon', [])
    is_default = lambda color: color.get('default', False)

    colors = config['lightshow']['condition']['colors']
    default = next(filter(is_default, colors), {})
    color = next(filter(is_condition_in_list, colors), default)

    return color.get('rgb')

def update_yeelight_beacon(beacon, temperature_color, condition_color):
    '''
    Updates a Yeelight beacon
    '''
    brightness = config['lightshow']['brightness']
    duration = config['lightshow']['transition']['duration'] * 1000
    delay = config['lightshow']['transition']['delay'] * 1000

    flow = Flow(
        0,
        Flow.actions.recover,
        [
            RGBTransition(*temperature_color, duration, brightness),
            SleepTransition(delay),
            RGBTransition(*condition_color, duration, brightness),
            SleepTransition(delay)
        ]
    )

    bulb = SmartBulb(beacon['ip'])
    bulb.start_flow(flow)


if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.load(f)

    forecast = get_forecast()

    temperature_color = get_temperature_color(forecast['temperature'])
    condition_color = get_condition_color(forecast['condition'])

    print ('temp - %s - %s' % (forecast['temperature'], temperature_color))
    print ('condition - %s - %s' % (forecast['condition'], condition_color))

    for beacon in config['beacons']:
        if beacon['type'] == 'yeelight':
            update_yeelight_beacon(beacon, temperature_color, condition_color)
