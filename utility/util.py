from datetime import datetime

def isValidDate(dt_str):
    try:
        datetime.fromisoformat(dt_str)
    except:
        return False
    return True