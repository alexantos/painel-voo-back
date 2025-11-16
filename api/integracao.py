import requests


def integracao_aeroporto():
    try:
        result = requests.get(url='http://localhost:8001')
        response = result.json()
        return response
    except Exception as e:
        print("Ocorreu um erro inesperado: ", e)
        return "Ocorreu um erro inesperado"
