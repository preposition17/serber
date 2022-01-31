from threading import Thread
import time

from models import Session
from models import models


class Settings:
    def __init__(self):
        with Session() as db_session:
            settings = db_session.query(models.Settings).all()
            for setting in settings:
                self.__dict__.update({
                    setting.key: setting.current
                })


    def _update(self):
        while True:
            with Session() as db_session:
                settings = db_session.query(models.Settings).all()
                for setting in settings:
                    self.__dict__.update({
                        setting.key: setting.current
                    })
                time.sleep(1)


    def updater_start(self):
        updater_thread = Thread(target=self._update)
        updater_thread.start()