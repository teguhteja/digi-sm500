import os, time as t

for i in range(1,100):
    a = f"C:\\Users\\teguhteja\\P\\PythonProjects\\Digi01\\my_dat_files\\digiwtcp.exe RD {i} 192.168.168.125"
    print(a)
    os.system(a)
    t.sleep(5)
    