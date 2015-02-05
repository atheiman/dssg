def info(string, obj=None):
    string = "INFO - %s" % string
    if obj:
        string += " - %s" % obj
    print string


def warn(string, obj=None):
    string = "WARNING - %s" % string
    if obj:
        string += " - %s" % obj
    print string


def error(string, exception=None, obj=None):
    string = "ERROR - %s" % string
    if obj:
        string += " - %s" % obj
    if exception:
        string += "\n\tException: %s" % exception
    string += "\nCorrect the above error before continuing."
    raise SystemExit(string)
