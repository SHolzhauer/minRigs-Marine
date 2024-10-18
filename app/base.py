import datetime

class Logboek:

    def __init__(self):
        self._logboek = "logboek.csv"

    def log(self, unit, metric):
        if unit not in ['vaaruren', 'tank', 'temp', 'status']:
            raise ValueError("unit not supported")
        
        tijd = datetime.datetime.now()

        with open(self._logboek, "a") as logboek:
            logboek.write(f"{tijd},{unit},{metric}\n")