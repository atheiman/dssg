def info(string, obj=None):
    string = "INFO:\n\n%s" % string
    if obj:
        string += "\n\t%s\n" % obj
    print string


def warn(string, obj=None):
    string = "WARNING:\n\n%s" % string
    if obj:
        string += "\n\t%s\n" % obj
    print string


def error(string, obj=None):
    string = "ERROR:\n\n%s" % string
    if obj:
        string += "\n\t%s\n" % obj
    string += "\nCorrect the above issue before continuing."
    raise SystemExit(string)
