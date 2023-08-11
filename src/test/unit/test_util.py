import time

from unittest import TestCase
from src.libs.util import get_downtime_in_minutes, custom_notification_message


class TestUtil(TestCase):
    def test_get_downtime_in_minutes(self):
        # Given
        start_time = time.time()
        end_time = start_time + 1000
        # When
        downtime = get_downtime_in_minutes(start_time, end_time)
        # Then
        self.assertGreater(downtime, 1)

    def test_custom_notification_without_error_message(self):
        # Given
        downtime_in_minutos = 10
        # When
        custom_message = custom_notification_message('', downtime_in_minutos)
        # Then
        expected_message = 'Internet connection was down but now it is up again. Downtime: 10 minute(s).'
        self.assertEqual(custom_message, expected_message)

    def test_custom_notification_with_error_message(self):
        # Given
        message = 'My custom error'
        downtime_in_minutos = 5
        # When
        custom_message = custom_notification_message(message, downtime_in_minutos)
        print(custom_message)
        # Then
        expected_message = f'Internet connection was down but now it is up again. Downtime: 5 minute(s). Error: {message}'
        self.assertEqual(custom_message, expected_message)
