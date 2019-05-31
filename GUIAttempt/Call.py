def Submit(name):
    
    if name == "":
        CalledText = "What is your name?"
    else:
        CalledText = "Hello, "+name+"!"

    return CalledText
