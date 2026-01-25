from app.builtins import built_ins
import os

def built_in_complete(text):
    return [built_in + " " for built_in in built_ins if built_in.startswith(text)]

def complete_from_path(text):
    completions = []
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for path in paths:
        if os.path.isdir(path) is False:
            continue

        for file in os.listdir(path):
            if file.startswith(text):
                completions.append(file + " ")
    
    return completions


completions = []

def complete(text, state):
    global completions
    if state == 0:
        completions = built_in_complete(text)
        completions.extend(complete_from_path(text))
    
    if state < len(completions):
        return completions[state]
   
    return None

    
