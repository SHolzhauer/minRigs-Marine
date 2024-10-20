from git import Repo
import datetime
import os
import http.client as httplib

class Logboek:

    def __init__(self):
        self._logboek = "logboek.csv"

    def log(self, unit, metric):
        if unit not in ['vaaruren', 'tank', 'temp', 'status', 'rpm', 'system']:
            raise ValueError("unit not supported")
        
        tijd = datetime.datetime.now()

        with open(self._logboek, "a") as logboek:
            logboek.write(f"{tijd},{unit},{metric}\n")


def startup():
    logboek = Logboek()
    # Check if there is a network connection
    if not internet_on():
        logboek.log("system", 'geen internet connectie; Kan niet controleren op updates.')
        return
    
    # Check if a new version is available
    repo = Repo(os.getcwd())
    assert not repo.bare

    # Fetch the latest changes from the remote
    origin = repo.remotes.origin
    fetch_info = origin.fetch()

    # Get the active branch
    local_branch = repo.active_branch
    remote_branch = repo.refs[f'origin/{local_branch.name}']

    if remote_branch.commit.hexsha != local_branch.commit.hexsha and \
        remote_branch.commit.committed_datetime > local_branch.commit.committed_datetime:
        logboek.log("system", 'updating application')
        # TODO: replace kivy ui with an update screen
        # Pull changes if remote has new commits
        origin.pull()
        # Restart the application
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        logboek.log("system", 'no update required')


def shutdown():
    logboek = Logboek()

    # Check if there is a network connection
    if not internet_on():
        logboek.log("system", 'geen internet connectie; Kan log file niet uploaden.')
        return


def internet_on() -> bool:
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    startup()
