import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'modules'))

from callee import say_hello

say_hello()