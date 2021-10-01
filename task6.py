import zlib 
def unfilter(Data_list, png_hight, png_width):
     #print (png_hight)
     
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
            for y in range(1,3*png_width+1):
                
                Data_list[x][y] += Data_list[x-1][y]    
                Data_list[x][y] %= 256
                     
             
        elif Data_list[x][0]==3:
            for y in range(1,3*png_width+1):
                if y < 4:
                    Data_list[x][y] += Data_list[x - 1][y]//2
                else:
                    Data_list[x][y] += (Data_list[x][y - 3] + Data_list[x - 1][y])// 2

                Data_list[x][y] %= 256
        elif Data_list[x][0]==4:
            for y in range(1,3*png_width+1):
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
     return Data_list
def filter(Data_list, png_hight, png_width):
    for i in range(png_hight - 1, -1, -1):
        if Data_list[i][0] == 0:
            continue
        elif Data_list[i][0] == 1:
            for j in range(3 * png_width, 0, -1):
                if j < 4:
                    Data_list[i][j] -= 0
                else:
                    Data_list[i][j] -= Data_list[i][j - 3]
                Data_list[i][j] %= 256

        elif Data_list[i][0] == 2:
            for j in range(3 * png_width, 0, -1):
                Data_list[i][j] -= Data_list[i - 1][j]
            Data_list[i][j] %= 256

        elif Data_list[i][0] == 3:
            for j in range(3 * png_width, 0, -1):
                if j < 4:
                    Data_list[i][j] -= Data_list[i - 1][j] // 2
                else:
                    Data_list[i][j] -= (Data_list[i][j - 3] + Data_list[i - 1][j]) // 2
                Data_list[i][j] %= 256

        else:
            for j in range(3 * png_width, 0, -1):
                if j < 4:
                    a, c = 0, 0
                else:
                    a = Data_list[i][j - 3]
                    c = Data_list[i - 1][j - 3]
                b = Data_list[i - 1][j]

                p = a + b - c
                min_abs = min(abs(a - p), abs(b - p), abs(c - p))
                if min_abs == abs(a - p):
                    Data_list[i][j] -= a
                elif min_abs == abs(b - p):
                    Data_list[i][j] -= b
                else:
                    Data_list[i][j] -= c
                Data_list[i][j] %= 256
    return Data_list




     
filename=input("请输入文件位置")
f = open(filename, "rb")
png = f.read()
leng=len(png)
png_list = list(bytearray(png))
filetype_list = png_list[:8]
type_data = png_list[16:24]
#beginlist = png[0:33]
#endlist = png[leng-12:leng]
idatdata = bytes()
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
      
        TYPE=png[i+4:i+8]
        if TYPE.decode() == "IDAT":
            idatdata += png[i+8:i+8+length]
        i += 12+length
    unzipedData = zlib.decompress(idatdata)
#还原rgb  
    Data_list = []
    for n in range(png_hight):
        
        Data_list.append(list(unzipedData[n * (3 * png_width + 1):(n + 1) * (3 * png_width + 1)]))
    Data_list = unfilter(Data_list,png_hight,png_width)
    
#修改像素点
    print("1) Original image\n2) Change image\n")
    Choose = int(input())
    if Choose==2:
        while 1:
            m = int(input("please enter x:"))
            m +=1
            n = int(input("please enter y:"))
            Choose_2=int(input("please enter 2(r) or 1(g) or 0(b):"))
            Choose_3=int(input("please enterthe number you want change"))
            if Choose_3<0 or Choose_3>255   :
                print("OUT OF RANGE ")
            else:
                Data_list[n][3*m-Choose_2]=Choose_3
            br = int(input("please enter 1 to continue or 0 to break"))
            if br==0:
                break
    elif Choose==1:
        print("no change")
#转灰度
    for i in range(png_hight):
        for j in range(1, 3 * png_width + 1, 3):
            gray = (Data_list[i][j]*299 + Data_list[i][j + 1]*587 + Data_list[i][j + 2]*114) //1000
            Data_list[i][j], Data_list[i][j + 1], Data_list[i][j + 2] = gray, gray, gray    
#准备映射            
    ascii_char = list('$"_&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-/+@<>i!:;,\^`.')
   
#过滤rgb
    #Data_list = filter(Data_list, png_hight, png_width)
    txt=''
#灰度映射字符
    nu_down = int(input("please set the number of characters in  Vertical direction:\n"))
    nu_right = int(input("please set the number of characters in  Horizontal direction:\n"))
    down = png_hight // nu_down
    right = png_width // nu_right
    for i in range(0, png_hight, down):
        for j in range(1, 3 * png_width + 1, right * 3):
            sum = 0
            for yy in Data_list[i:i + down]:
                for xx in yy[j:j + right * 3:3]:
                    sum += xx
            txt += ascii_char[sum // (down * right) // 4]
        txt += "\n"
     
    testfile = open("C:\\Users\\y\\Desktop\\ps后端实习\\test7", mode='w')
    testfile.write(txt)
else:
    print("not png")
f.close()
testfile.close()
     


