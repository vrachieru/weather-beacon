<p align="center">
    <img src="https://user-images.githubusercontent.com/5860071/49688211-41b4fd00-fb17-11e8-871a-773f11eeaf4f.png" width="100px" />
    <br/>
    <a href="https://github.com/vrachieru/weather-beacon/releases/latest">
        <img src="https://img.shields.io/badge/version-0.0.1-brightgreen.svg?style=flat-square" alt="Version">
    </a>
    <a href="https://travis-ci.org/vrachieru/weather-beacon">
        <img src="https://img.shields.io/travis/vrachieru/weather-beacon.svg?style=flat-square" alt="Version">
    </a>
    <br/>
    Weather condition awareness through smart lighting
</p>

This project aims to provide an easy way of being aware of upcoming weather conditions before you leave home in the morning.  
Forecasts are relayed through smart lights via color coded messages regarding temperature and weather conditions.  
For example an alternating blue light (signaling a lower temperature) and purple light (signaling rainy conditions).

## Features

* Color coded temperature
* Color coded weather conditions

## Configuration

Configuration is done via the [config.yaml](https://github.com/vrachieru/weather-beacon/blob/master/config.yaml) file.  
Please take a look there for a full working example.

#### Darksky

All usage requires a Dark Sky API key, which you can obtain from the [Dark Sky developer site](https://darksky.net/dev/).  
Provide the timeframe for the displayed forecast as an integer between `0` (current conditions) and `48` representing the number of hour into the future as well as the location for the forecast.  

```yaml
darksky: 
  apikey: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

forecast:
  timeframe: 12 # in hours 0-48
  location:
    latitude: 47.1615
    longitude: 27.5841
```

#### Lightshow

```yaml
lightshow:
  brightness: 100 # beacon brightness
  transition:
    duration: 2 # duration of transition between colors
    delay: 60 # time between color transitions
  temperature:
    colors:
      - name: cold # descriptive name
        rgb: [0, 147, 255] # color for temperature range
        min: 10 # minimum temperature 
        max: 20 # maximum temperature
        default: true # is default color for when current temperature is not in any configured ranges
  condition: 
    colors:
      - name: clear or mostly clear # descriptive name
        rgb: [185, 255, 179]  # color for condition set
        icon: # list of condition triggers for current color
          - clear-day
          - clear-night
          - partly-cloudy-day
          - partly-cloudy-night
        default: true # is default color for when current condition is not in any configured sets
```

#### Beacons

Currently supported beacons are only [Yeelight](https://github.com/vrachieru/xiaomi-yeelight-api) smart bulbs.  

```yaml
beacons:
  - name: bedroom lamp
    type: yeelight
    ip: 192.168.xxx.xxx
```

## License

MIT