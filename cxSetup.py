import cx_Freeze as cx
import platform
import os
import Images

if platform.system()=="Windows":
    PYTHON_DIR = os.path.dirname(os.path.dirname(os.__file__))

os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_DIR,'tcl','tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_DIR,'tcl','tk8.6')

include_files = [('Images','Images'),(os.path.join(PYTHON_DIR,'DLLs','tcl86t.dll'),''),(os.path.join(PYTHON_DIR,'DLLs','tk86t.dll'),'')]


target_name = None
base = None
if platform.system()=="Windows":
    base = "Win32GUI"
    target_name = 'Doc Manager.exe'

shortcut_data = [
    ('DesktopShortcut','DesktopFolder','Doc Manager','TARGETDIR',
        '[TARGETDIR]'+target_name,None,'Data Entry application for hospitals/clinics',None,None,None,None,'TARGETDIR'
        ),(
            'MenuShortcut','ProgramMenuFolder','Doc Manager','TARGETDIR','[TARGETDIR]'+target_name,None,
            'Data Entry application for hospitals/clinics',None,None,None,None,'TARGETDIR'
        )
]

cx.setup(name = "Doc Manager",
         version = "1.0",
         author = "Harshvardhan Singh",
         author_email = "harshvardhansingh458@gmail.com",
         description = "Patient Data Entry Application medical clinic",
         options = {'build_exe':{'packages':["tkinter","os","sqlite3","shutil","datetime","reportlab","time","webbrowser","threading","external_packages"],'include_files':include_files},
                    'bdist_msi':{
                        'upgrade_code':'{83A4FBB5-5727-4195-ADA6-2765FB571421}','data':{'Shortcut':shortcut_data}
                    }},
         executables = [cx.Executable("ui_module.py",base = base,targetName=target_name,icon=Images.ICON)])
