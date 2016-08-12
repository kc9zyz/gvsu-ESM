# Measures battery state-of charge based on voltage level
def batteryLevel(adc):
    level = adc.read()[1]

    if level > 38:
        return (100,level)
    elif level > 37.2:
        return (75,level)
    elif level > 36.6:
        return (50,level)
    elif level > 36:
        return (25,level)
    else:
        return (0,level)
