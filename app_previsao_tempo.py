import requests
import json

accuweatherAPIKey = '0uTw0Jnxw3Re7goG68xXxnAm5ijwl4V6'

def getCoordinates():
    r = requests.get('http://www.geoplugin.net/json.gp')

    if (r.status_code != 200):
        print('Não foi possível obter a localização.')
        return None
    else:
        try:
            localizacao = json.loads(r.text) ## print(type(json.loads(r.text))) -> o json.loads transforma o retorno de str para dicionário
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long'] = localizacao['geoplugin_longitude']
            return coordenadas
        except:
            return None

def getLocalCode(lat, long):
    LocationAPIUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' + accuweatherAPIKey + '&q=' + lat + '%2C' + long + '&language=pt-br'
    r = requests.get(LocationAPIUrl)
    if (r.status_code != 200):
        print('Não foi possível obter o código do local.')
        return None
    else:
        try:
            locationReponse = json.loads(r.text)
            infoLocal = {}
            infoLocal['nomeLocal'] = locationReponse['LocalizedName'] + ', ' + locationReponse['AdministrativeArea']['LocalizedName'] + '. ' + locationReponse['Country']['LocalizedName']
            infoLocal['codigoLocal'] = locationReponse['Key']
            return infoLocal
        except:
            return None

def getCurrentWeather(codigoLocal, nomeLocal):
    CurrentConditionsAPIUrl = 'http://dataservice.accuweather.com/currentconditions/v1/' + codigoLocal + '?apikey=' + accuweatherAPIKey + '&language=pt-br'

    r = requests.get(CurrentConditionsAPIUrl)
    if (r.status_code != 200):
        print('Não foi possível obter o clima atual.')
        return None
    else:
        try:
            CurrentConditionsReponse = json.loads(r.text)
            infoClima = {}
            infoClima['textoClima'] = CurrentConditionsReponse[0]['WeatherText']
            infoClima['temperatura'] = CurrentConditionsReponse[0]['Temperature']['Metric']['Value']
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None

def getForecast(codigoLocal):
    DailyAPIUrl = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + codigoLocal + '?apikey=' + accuweatherAPIKey + '&language=pt-br&metric=true'
    r = requests.get(DailyAPIUrl)
    if (r.status_code != 200):
        print('Não foi possível obter o clima atual.')
        return None
    else:
        try:
            DailyResponse = json.loads(r.text)
            infoClima5Dias = []
            for dia in DailyResponse['DailyForecasts']:
                climaDia = {}
                climaDia['max'] = dia['Temperature']['Maximum']['Value']
                climaDia['min'] = dia['Temperature']['Minimum']['Value']
                climaDia['clima'] = dia['Day']['IconPhrase']
                climaDia['dia'] = dia['EpochDate']
                infoClima5Dias.append(climaDia)
            return infoClima5Dias
        except:
            return None


## Início do programa

try:
    coordenadas = getCoordinates()
    local = getLocalCode(coordenadas['lat'], coordenadas['long'])
    climaAtual = getCurrentWeather(local['codigoLocal'], local['nomeLocal'])
    print('Clima atual em: ' + climaAtual['nomeLocal'])
    print(climaAtual['textoClima'])
    print('Temperatura: ' + str(climaAtual['temperatura']) + '\xb0' + 'C')

    print('\nClima para hoje e para os próximos dias:\n')

    previsao5Dias = getForecast(local['codigoLocal'])
    for dia in previsao5Dias:
        print(dia['dia'])
        print('Máxima: ' + str(dia['max']) + '\xb0' + 'C')
        print('Mínima: ' + str(dia['min']) + '\xb0' + 'C')
        print('Clima: ' + dia['clima'])
        print('-------------------------------')
    
except:
    print('Erro ao processar a solicitação. Entre em contato com o suporte.')
    
