from app.builtins import built_ins
import os

def built_in_complete(text):
    return [built_in for built_in in built_ins if built_in.startswith(text)]

def complete_from_path(text):
    completions = []
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for path in paths:
        if os.path.isdir(path) is False:
            continue

        for file in os.listdir(path):
            if file.startswith(text):
                completions.append(file)
    
    return completions


completions = set()

def complete(text, state):
    global completions
   
    if state == 0:
        completions.clear()
        completions.update(built_in_complete(text))
        completions.update(complete_from_path(text))
        if len(completions) == 1:
            completions.add(completions.pop() + " ")

    if state < len(completions):
        return list(completions)[state]
   
    return None

    
