import os
import sys
IMAGE_DIRECTORY = None
if getattr(sys,'frozen',False):
    IMAGE_DIRECTORY = os.path.join(os.path.dirname(sys.executable),'Images')
else:
    IMAGE_DIRECTORY = os.path.dirname(__file__)

#A
ADD_NEW_PATIENT = os.path.join(IMAGE_DIRECTORY,"add_new_patient.png")

#B
BACK = os.path.join(IMAGE_DIRECTORY,"back.png")

#C
CANCEL = os.path.join(IMAGE_DIRECTORY,"cancel.png")

#D
DELETE = os.path.join(IMAGE_DIRECTORY,"delete.png")
DETAILS = os.path.join(IMAGE_DIRECTORY,"details.png")

#E
EDIT = os.path.join(IMAGE_DIRECTORY,"Edit.png")

#F
FLASH = os.path.join(IMAGE_DIRECTORY,"flash.png")

#I
ICON = os.path.join(IMAGE_DIRECTORY,"icon.ico")

#L
LINE = os.path.join(IMAGE_DIRECTORY,"Line.png")
LINE_VERTICAL = os.path.join(IMAGE_DIRECTORY,"Line-vertical.png")
LINE_HORIZONTAL = os.path.join(IMAGE_DIRECTORY,"Line-horizontal.png")

#M
MEDICAL_REPORT = os.path.join(IMAGE_DIRECTORY,"medical_report.png")

#O
OK = os.path.join(IMAGE_DIRECTORY,"ok.png")

#P
PRINT = os.path.join(IMAGE_DIRECTORY,"print.png")

#R
RESET = os.path.join(IMAGE_DIRECTORY,"reset.png")

#S
SAVE = os.path.join(IMAGE_DIRECTORY,"save.png")
SEARCH = os.path.join(IMAGE_DIRECTORY,"search.png")
SUBMIT = os.path.join(IMAGE_DIRECTORY,"submit.png")

#U
UNDERLINE = os.path.join(IMAGE_DIRECTORY,"underline.png")
UPDATE = os.path.join(IMAGE_DIRECTORY,"update.png")

#V
VIEW = os.path.join(IMAGE_DIRECTORY,"view.png")