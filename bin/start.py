import os
import sys

from pip import main
print(os.path.dirname(__file__))
Source_path=os.path.dirname(__file__)
Source_path_parent=os.path.split(Source_path)[0]
print(Source_path)
print(Source_path_parent)
sys.path.append(Source_path)
sys.path.append(Source_path_parent)
print(sys.path)

from core import src

print(__name__)
if __name__=='__main__':
    src.run()