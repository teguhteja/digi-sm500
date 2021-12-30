# digi-sm500
Exploration Data from Digi-SM500 using terminal

### DISCLAIMER :
I only explored using digiwtcp and .dat files. I'm not a developer of digiwtcp, digi-Net and Digi-Map 

![Digi SM500 Pic](/assets/SM_500_MK4.png "Digi SM500")

The SM-500MK4 system scale with fast processing and printing speeds up to 150mm/s, will be your best companion to increase throughput and operation efficiency during busy times. [SM-500MK4](https://www.digisystem.com/products/PRD00292/)

<br/>

# Problem insert data
There are 2 ways to insert data into weighing machine, such as the manual method and using a supporting application. The manual method is by entering data one by one through the keyboard on the scales. This requires a long processing time and is prone to errors. 

The second way is by using supporting applications such as Digi-Map and digi-Net. The Digi-Map application functions to map input from csv into .mdb while digi-Net sends data in .mdb to the weighing machine. Although this is faster than manual, there is vulnerability in mapping, it takes up a lot of work, so it becomes a burden for operations
<br/>
<br/>
# Solution 
To overcome the problem of entering data into the scales automatically, several questions were encountered
1. How to skip the Digi-Map and digi-net process?
2. What files are sent to the weighing machine?
3. What formats are sent to the weighing machine?
<br/>
<br/>

## How to skip the Digi-Map and digi-net process ?
after looking for the use of digi SM500 found the digiwtcp can send files to the scales using the format 

```cmd
digiwtcp.exe WR SM192.168.168.1F37.DAT
```
<br>
WR is command <br>
192.168.168.1 is IP Machine of Weighning<br>
37 is Table what used<br>
<br/>

WR function means it will write a file into the weighing machine. Some of the commands available and this is case sensitive :
<ul>
<li> RD - read </li>
<li> WR - write </li>
<li> DEL - delete </li>
<li> DELFI - delete file </li>
<li> RD_DEL - read and then delete </li>
</ul>
<br>
digiwtcp will generate a result file after doing the process of sending the file, which contains the ip and the results of the process. that below is meaning of result and can use it in json 

<br/>
<br/>

```
0 = no error
-1 = Open file error
-2 = Read from file error
-3 = Write to file error
-4 = Network initialize error
-5 = Network open error
-6 = Network read error
-7 = Network write error
-8 = Machine read error
-9 = Machine write error
-10 = Machine no record error
-11 = Machine space error
-12 = Undefined error
```
<br/>

for documentation please look at [doc/TWSWTCP.pdf](https://https://github.com/teguhteja/digi-sm500/doc/TWSWTCP.pdf) 
<br><br>
## What files are sent to the weighing machine ?
Like the example above to send a file using the .DAT format which contains numbers in hex format. Then F37 as a table is used in operations. Try to read other tables using command :
```cmd
digiwtcp.exe RD SM192.168.168.1F1.DAT
```

After read file from machine will find many empty and filled tables. If it is empty then it will write code 'E2' and it contains data will write Hex data

for generate file from all file then using this in python

```python
import os, time as t

for i in range(1,100):
    a = f"digiwtcp.exe RD {i} 192.168.168.125"
    print(a)
    os.system(a)
    t.sleep(5)

```
<br>

## What formats are sent to the weighing machine ?
When open a .dat file from a weighing machine and find a long number format in hex. Based on the documentation from [doc/jbptunikompp-gdl-s1-2006-didinjamal-2857-jurnal_d-n.doc](https://https://github.com/teguhteja/digi-sm500/doc/jbptunikompp-gdl-s1-2006-didinjamal-2857-jurnal_d-n.doc) in table 3-1 and adapted to the Digi-Map and Digi-Net applications then 1 data ends at C000.<br>
as an example
```
00000004004A00005D208D010000001109320004000000000997000000000000000000000000800060000000000000000000000713494D424F4F5354204C4F5A454E4745532035530C00
```
when made into the description table
<br>
| No | Description           | Length    | Example                                                 | Remark                                                     |
|----|-----------------------|-----------|---------------------------------------------------------|------------------------------------------------------------|
| 1  | PLU NUMBER            | 8         | 00000004                                                | Id of record  or PLU code                                  |
| 2  | PLU RECORD SIZE       | 4         | 004A                                                    | Length of record.  Hex Format. 4A=74(DEC) 74*2=148         |
| 3  | PLU STATUS            | 4         | 0000                                                    | Default format  from Digi-Net                               |
| 4  | PLU STATUS 2          | 6         | 5D208D                                                  | Default format  from Digi-Net                               |
| 5  | UNIT PRICE            | 8         | 01000000                                                | =1.000.000/Kg                                              |
| 6  | LABEL 1 FORMAT        | 2         | 11                                                      | Default format  from Digi-Net                               |
| 7  | BARCODE FORMAT        | 2         | 09                                                      | Default format  from Digi-Net                               |
| 8  | EAN DATA              | 14        | 24000400000000                                          | 32 = code barcode<br> 0004 = plu code                          |
| 9  | USED BY DATE          | 4         | 0997                                                    | Default format  from Digi-Net                               |
| 10 | DEF1                  | 50        | 000000000000000 000000000800060 000000000000000<br>0000007 | Default format  from Digi-Net                               |
| 11 | Name Record Size(NRS) | 2         | 13                                                      | Length of name record.  Hex Format. 13=19(DEC) (19+1)*2=40 |
| 12 | COMMODITY NAME        | (NRS+1)*2<br>(19+1)*2=40 | 494D424F4F5354 204C4F5A454E47 45532035530C              | 49=I, 4D=M, 42=B ... then  IMBOOST LOZENGES 5S             |
| 13 | BCC                   | 2         | 00                                                      | Default format  from Digi-Net                               |


<br/>For convert COMMODITY NAME from HEX to ASCI then use code below :

```python
def my_convert_hex(hex_string):
    bytes_object = bytes.fromhex(hex_string)
    return bytes_object.decode("ASCII")

```

### Reference
1. [Hex to ASCII ](https://www.rapidtables.com/convert/number/hex-to-ascii.html)
2. [Hex to Dec](https://www.rapidtables.com/convert/number/hex-to-decimal.html)