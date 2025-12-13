import requests


def integracao_voos_finalizados():
    try:
        result = requests.get(url='http://localhost:8001/finalizados')
        response = result.json()
        return response
    except Exception as e:
        print("Ocorreu um erro inesperado: ", e)
        return "Ocorreu um erro inesperado"


def integracao_voos_ativos():
    try:
        result = requests.get(url='http://localhost:8001')
        response = result.json()
        return response
    except Exception as e:
        print("Ocorreu um erro inesperado: ", e)
        return "Ocorreu um erro inesperado"
