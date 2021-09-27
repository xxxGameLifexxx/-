
import zlib 
filename=input("请输入文件位置")
f = open(filename, "rb")
png = f.read()
png_list = list(bytearray(png))
filetype_list = png_list[:8]
type_data= png_list[16:32]
idatdata = b""
i=33

if filetype_list == [0x89, 0x50, 0x4e, 0x47, 0xd, 0xa, 0x1a, 0xa]:

    png_width = (256 ** 3) * type_data[0] + \
                (256 ** 3) * type_data[1] + \
                (256 ** 1) * type_data[2] + \
                (256 ** 0) * type_data[3]
    png_hight = (256 ** 3) * type_data[4] + \
                    (256 ** 2) * type_data[5] + \
                    (256 ** 1) * type_data[6] + \
                    (256 ** 0) * type_data[7]
    print("稍等片刻")
    
    while i<len(png_list):
        length = (256 ** 3) * png_list[i] + \
                     (256 ** 2) * png_list[i + 1] + \
                     (256 ** 1) * png_list[i + 2] + \
                     (256 ** 0) * png_list[i + 3]
        

        
        idatdata +=png[i+8:i+8+length]
        i += 12+length
    unzipedData = zlib.decompress(idatdata)
    Data_list = []
    
    for n in range(png_hight):
        

        Data_list.append(list(unzipedData[n * (3 * png_width + 1):(n + 1) * (3 * png_width + 1)]))
    for x in range(png_hight):
        if Data_list[x][0]==0:
            continue
        elif Data_list[x][0]==1:
            for y in range(3*png_width+1):
                if y<4:
                    Data_list[x][y] += 0 
                else:
                    Data_list[x][y] += Data_list[x][y-3]
                Data_list[x][y] %= 256
        elif Data_list[x][0]==2:
            for y in range(3*png_width+1):
                Data_list[x][y] += Data_list[x-1][y]    
                Data_list[x][y] %= 256
                     
             
        elif Data_list[x][0]==3:
            for y in range(3*png_width+1):
                if y < 4:
                    Data_list[x][y] += Data_list[x - 1][y]/2
                else:
                    Data_list[x][y] += (Data_list[x][y - 3] + Data_list[x - 1][y])/ 2

                Data_list[x][y] %= 256
        elif Data_list[x][0]==4:
            for y in range(3*png_width+1):
                if y < 4:
                    a,c = 0,0
                else:
                    a = Data_list[x][y - 3]
                    c = Data_list[x - 1][y - 3]
                b = Data_list[x - 1][y]

                p = a + b - c
                min_abs = min(abs(a - p), abs(b - p), abs(c - p))
                if min_abs == abs(a - p):
                    Data_list[x][y] += a
                elif min_abs == abs(b - p):
                    Data_list[x][y]+= b
                else:
                    Data_list[x][y] += c
                Data_list[x][y] %= 256
           
    #print(Data_list)    
    while 1:
        m = int(input("please enter x:"))
        m +=1
        n = int(input("please enter y:"))
        print(m)
        print(n)
        if m < png_width and n < png_hight:
           print("r:%d g:%d b:%d" % (Data_list[n][3*m-2]*257,Data_list[n][3*m-1]*257,Data_list[n][3*m]*257))
        else:
           print("OUT OF RANGE ")                            
else:
     print("error")
f.close()