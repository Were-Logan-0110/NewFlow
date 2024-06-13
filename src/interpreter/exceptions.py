def error(line: int,message: str):
    report(line,"",message)
def report(line: int,where: str,message: str):
    print(f"[Line {line}] Error{where}: {message}")