from abc import ABC, abstractclassmethod
# from callmebot import send_free_notification # Module from GitHub


class SMSNotification(ABC):
    @abstractclassmethod
    def send_notification(message: str, phone_number: str, api_key: str):
        pass


class FakeNotification(SMSNotification):
    @staticmethod
    def send_notification(message: str, phone_number: str, api_key: str):
        pass