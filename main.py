import json
import os
import pprint
import urllib.request

from dotenv import load_dotenv

try:
    load_dotenv(dotenv_path='config.env')

    URL = os.environ.get('URL')

    response = urllib.request.urlopen(URL)

    body_response = response.read()
    json_response = json.loads(body_response.decode('utf-8'))
    data = json_response['personas']
    for personas in data:
        print(f"Nombre: {personas['nombre']} . Edad: {personas['edad']}")

    with open("data.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # pprint.pprint(json_response)
except urllib.error.URLError as e:
    print(f"No se pudo conectar. Error: {e}")
except json.JSONDecoder as e:
    print(f"Error rlacionado con json: {e}")
except Exception as e:
    print(f"Error: {e}")