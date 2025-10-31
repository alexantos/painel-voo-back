import requests



def integracao_aeroporto():
    try:
        result = requests.get(url='localhost:8001')
        response = result.json()
        return 'Atualizado os eventos com sucesso!'

    except Exception as e:
        print("Ocorreu um erro inesperado: ", e)
        return "Ocorreu um erro inesperado"
