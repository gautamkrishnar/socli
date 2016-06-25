import sys,os
try:
    x = sys.getwindowsversion()[0]
    if x == "10":
        print("windows detected")
        try:
            tet_shell = os.environ['SHELL']
        except Exception:
            print("shell detected")
except Exception:
    pass