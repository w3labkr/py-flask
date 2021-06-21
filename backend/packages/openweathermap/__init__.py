def openweathermap(template, **kwargs):
    if (template == 'weather'):
        from .tmpl.weather import weather
        return weather(**kwargs)
    elif (template == 'forecast'):
        from .tmpl.forecast import forecast
        return forecast(**kwargs)