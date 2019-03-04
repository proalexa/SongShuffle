from os import remove, system, rename, rmdir
from shutil import rmtree

system("python3 -m pip install pyinstaller")
system("pyinstaller -y -F \"./main.py\"")
rmtree("./build")
rename("./dist/main", "./main")
rmdir("dist")
remove("main.spec")
