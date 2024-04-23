s = '''
#include <stdio.h>
void generate() { printf("hello");}
'''

def run():
    with open("gen.h", "w") as f:
       f.write(s)
