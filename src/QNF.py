from interpreter import *
from helpers import *
from scanner import *
from ast_ import *
source = readFile("./main.qnf")
source = """
b = true;
a = -(((3+3) * 4) / 6);
if (a > 3) && b:
    println "wtv";
elif true && false:
    println "Test";
elif true && 1:
    println "This should show";
else:
    print "nothing";
//a = 1;
//{
//    a = a + 2;
//    println a;
//}
// println token;
// token = "one";
// println token + " love";
// println true;
// expr = -((2 + 1 / 3 * 9) + 2);
// print expr + 1;
// print " That Num";
"""
_scanner = Scanner(source)
_tokens = _scanner.scan()
_parser = LLParser(_tokens)
stmts = _parser.parse()
[print(stmt) for stmt in stmts]
print("--"*30)
ASTInterpreter().interpret(stmts)