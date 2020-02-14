import os
import sys
DIRECTORY = None
if(getattr(sys,"frozen",False)):
    DIRECTORY = os.path.join(os.path.dirname(sys.executable),"external_packages")
else:
    DIRECTORY = os.path.join(__file__)

Backend = os.path.join(DIRECTORY,"backend.py")
PopupDialogs = os.path.join(DIRECTORY,"popup_dialogs.py")
WidgetCreater = os.path.join(DIRECTORY,"widget_Creater.py")