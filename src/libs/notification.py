import callmebot


def singleton(class_):
    instances = {}
    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance


@singleton
class SMSNotification():
    def __init__(self, api_key: str):
        self.api_key = api_key

    def send_notification(self, message: str, phone_number: str) -> (bool, str):
        return callmebot.send_free_notification(message, phone_number, self.api_key)
