from app.builtins import built_ins

completions = []

def complete(text, state):
    global completions
    if state == 0:
        completions = [built_in + " " for built_in in built_ins if built_in.startswith(text)]
    if state < len(completions):
        return completions[state]
    else:
        completions = []
        return None

    