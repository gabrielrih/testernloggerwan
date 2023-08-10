def get_downtime_in_minutes(time_since_the_epoch_when_it_was_down: float, time_since_the_epoch_when_it_turns_up: float) -> int:
    downtime = time_since_the_epoch_when_it_turns_up - time_since_the_epoch_when_it_was_down
    return round(downtime / 60, 2) # returns in minutes


def custom_notification_message(error_message: str, downtime_in_minutes: int) -> str:
    error_message = str(error_message)
    custom_message = "Internet connection was down but now it is up again."
    custom_message += " Downtime: " + str(downtime_in_minutes) + ' minute(s).'
    if error_message:
        custom_message += " Error: " + str(error_message)
    return custom_message
