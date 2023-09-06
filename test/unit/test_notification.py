from unittest import TestCase, mock

from src.libs.notification import SMSNotification


class TestSMSNotification(TestCase):

    __FAKE_API_KEY = '123'

    @mock.patch('callmebot.send_free_notification')
    def test_send_notification_when_invalid_api_key(self, mock_send_notification):
        # Given
        mock_send_notification.return_value = False, 'APIKey is invalid'
        expected_message_error_contains = 'APIKey is invalid'
        # When
        notification = SMSNotification(self.__FAKE_API_KEY)
        success, message = notification.send_notification('Just a message', '+555599887766')
        # Then
        mock_send_notification.assert_called_once()
        self.assertFalse(success)
        is_expected_message = False
        if expected_message_error_contains in message:
            is_expected_message = True
        self.assertTrue(is_expected_message)

    @mock.patch('callmebot.send_free_notification')
    def test_send_notification_when_success(self, mock_send_notification):
        # Given
        expected_message = 'Success'
        mock_send_notification.return_value = True, expected_message
        # When
        notification = SMSNotification(self.__FAKE_API_KEY)
        success, message = notification.send_notification('Just a message', '+555599887766')
        # Then
        mock_send_notification.assert_called_once()
        self.assertTrue(success)
        self.assertEqual(message, expected_message)

    def test_is_singleton(self):
        notification_one = SMSNotification(self.__FAKE_API_KEY)
        notification_two = SMSNotification(self.__FAKE_API_KEY)
        self.assertEqual(notification_one, notification_two)
