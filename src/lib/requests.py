import requests

MALL_ID = '1'

SPOTS_AVAILABLE = 'https://plumia-bot.onrender.com/api/spots/available?mallId=' + MALL_ID
DEPARTED = 'https://plumia-bot.onrender.com/api/visit/departed'
ARRIVED = 'https://plumia-bot.onrender.com/api/visit/arrived'



def getSpotsAvailable():
    response = requests.get(SPOTS_AVAILABLE)
    
    if (response.status_code != 200):
        return None

    return response.json()
