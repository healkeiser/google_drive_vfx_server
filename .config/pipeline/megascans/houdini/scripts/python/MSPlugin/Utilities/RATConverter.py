import os
import time
from datetime import datetime, timedelta
import subprocess
import threading
import platform


def ratify(file, newFile):
    sargs = ["icp", file, newFile]    

    curPlatform = platform.system()
    if ("darwin" in curPlatform.lower()) or ("linux" in curPlatform.lower()):
        p = subprocess.Popen(sargs, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=False)
    else:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(sargs, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=False,
                            startupinfo=si)
    result = p.communicate()   
    

def ConvertToRAT(components):
    
    threads = []
    for index, textureData in enumerate(components):
        texPath = textureData["path"]
        newFile = os.path.splitext(texPath)[0] + ".rat"
        components[index]["path"] = newFile
        if os.path.isfile(newFile):
            continue
        
        t = threading.Thread(name="Converter", target=ratify, args=(texPath, newFile))
        threads.append(t)
        t.start()

    for thread in threads:
       thread.join()




