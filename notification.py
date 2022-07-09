#
# Sending free messages/notifications using WhatsApp (CallMeBot)
# <gabrielrih>
#
import requests


URL = "https://api.callmebot.com/whatsapp.php"


def send_free_notification(message, phoneNumber, apiKey, enableDebugMode = False):
    if enableDebugMode == 'False':
        http_code, response = _callAPI(apiKey, phoneNumber, message)
        if http_code == 200:
            isSuccess = True
        else:
            isSuccess = False
        return isSuccess, response
    else: # It simulates success without actually send the notification
        return True, "Success!"


def _callAPI(apiKey, phoneNumber, message):
    payload = {'phone': phoneNumber, 'text': message, 'apikey': apiKey}
    response = requests.get(URL, params=payload)
    return response.status_code, response.text