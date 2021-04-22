import json
import parser
import scanner
# cmd
text='''
module main
import math
import io
import os
import net.socket
import sys,json,xml

const age=17

main(int age,[]int nums, map[int]string names) {
    num int=45
    mut x []int=0
}
'''
    # if t1{}
    # age
    # if 5 > 2 + 5 {
    #     while i<5{}
    #     if 5**8{}
    # }
    # test    ()
    # io.math.sin()
    # math.cos(5+6)
    # 5+5
    # 8**2
# filename='input.c'
# text=open(filename).read()
# lexer = lex.lex(debug=1)
tokens=scanner.tokens
yacc = parser.yacc.yacc(debug=1, write_tables=0)
result = yacc.parse(text)
# print(result)
print(json.dumps(result,indent=4))
