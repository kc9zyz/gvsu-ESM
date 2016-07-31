def windspeed(adc):
    level = adc.read()[0]
    if level < 0.4:
        level = 0.4
    return ((level-0.4) / 1.6)*72.47
