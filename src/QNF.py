from interpreter import *
from helpers import *
from scanner import *
from ast_ import *
source = readFile("./main.qnf")
source = """
a = 0;
for (b = 1; a < 10000; b = temp + b) {
 println a;
 temp = a;
 a = b;
}
a = [1,2,3,"test",2];
foreach i in a {
    println i;
}
count = 0;
foreach a {
    println count;
    count = count + 1;
    if count > 2 {
        break;
    }
}
c = 1;
while true {
    if c >= 3 {
        println "Breaking While Loop";
        break;
    }
    else {
        println c;
    }
    c = c + 1;
}
"""
_scanner = Scanner(source)
_tokens = _scanner.scan()
print(_tokens)
_parser = LLParser(_tokens)
stmts = _parser.parse()
[print(stmt) for stmt in stmts]
print("--"*30)
ASTInterpreter().interpret(stmts)
