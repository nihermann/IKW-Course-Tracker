from IKWScraper import check_for_updates
import time


if __name__ == '__main__':

    DEBUG = True

    while True:

        update = check_for_updates(headless=True)

        # todo if there is an update, do something with it. F.e. send a mail
        if update:
            pass

        if DEBUG:
            break

        # sleep for an hour
        time.sleep(3600)

