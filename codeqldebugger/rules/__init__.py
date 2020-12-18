from codeqldebugger.rules.summary import *
from codeqldebugger.rules.languages import *
from codeqldebugger.rules.dependencies import *

RULES = {
    "100": sources,
    "101": databaseSinks,
    "102": xssSinks,
    "210": projectLombokCheck,
    "251": kotlinDetected,
    "255": jspCheck,
}
