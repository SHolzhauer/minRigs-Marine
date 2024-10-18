from datetime.datetime import now

class Logboek:

    def __init__(self):
        self._logboek = "logboek.csv"

    def log(self, unit, metric):
        if unit not in ['vaaruren', 'tank', 'temp', 'status']:
            raise ValueError("unit not supported")
        
        
        with open(self._logboek, "a") as logboek:
            logboek.write(f"{now()},{unit},{metric}")