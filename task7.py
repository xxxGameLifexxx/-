from zlib import decompress, compress
def unfilter(Data_list, png_hight, png_width):
    # 还原RGB信息
    for i in range(png_hight):
        if Data_list[i][0] == 0:
            continue
        elif Data_list[i][0] == 1:
            for j in range(0, (3 * png_width + 1)):
                if j < 4:
                    Data_list[i][j] += 0
                else:
                    Data_list[i][j] += Data_list[i][j - 3]
                Data_list[i][j] %= 256

        elif Data_list[i][0] == 2:
            for j in range(1, (3 * png_width + 1)):
                Data_list[i][j] += Data_list[i - 1][j]
                Data_list[i][j] %= 256

        elif Data_list[i][0] == 3:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    Data_list[i][j] += Data_list[i - 1][j] // 2
                else:
                    Data_list[i][j] += (Data_list[i][j - 3] + Data_list[i - 1][j]) // 2
                Data_list[i][j] %= 256

        else:
            for j in range(1, (3 * png_width + 1)):
                if j < 4:
                    a, c = 0, 0
                else:
                    a = Data_list[i][j - 3]
                    c = Data_list[i - 1][j - 3]
                b = Data_list[i - 1][j]

                p = a + b - c
                min_abs = min(abs(a - p), abs(b - p), abs(c - p))
                if min_abs == abs(a - p):
                    Data_list[i][j] += a
                elif min_abs == abs(b - p):
                    Data_list[i][j] += b
                else:
                    Data_list[i][j] += c
                Data_list[i][j] %= 256

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
beginlist = png[0:33]
endlist = png[leng-12:leng]

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
   # print(png_width)
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
    unzipedData = decompress(idatdata)
#还原rgb  
    Data_list = []
    for n in range(png_hight):
        Data_list.append(list(unzipedData[n * (3 * png_width + 1):(n + 1) * (3 * png_width + 1)]))
#    for n in range (png_hight):
 #       print(Data_list[n][0])
 #   print("next")
    Data_list = unfilter(Data_list,png_hight,png_width)
 #   for n in range (png_hight):
    #    print(Data_list[n][0])
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




#转为灰度图    

    for i in range(png_hight):
        for j in range(1, 3 * png_width + 1, 3):
            gray = (Data_list[i][j]*299 + Data_list[i][j + 1]*587 + Data_list[i][j + 2]*114) //1000
            Data_list[i][j], Data_list[i][j + 1], Data_list[i][j + 2] = gray, gray, gray         
            #边缘检测算法sobel
    gray_list_1 = []
    gray_list_x = []
    gray_list_y = []
    gray_list_2 = []
    for Dataline in Data_list:
        gray_list_1.append(Dataline[1::3])
        gray_list_2.append(Dataline[1::3]) 
    x1, x2, x3, y1, y2, y3, z1, z2, z3, a, b = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    boundary = int(input("界限(越小边缘越清晰，但噪点越多):"))
    #推荐界限180-270
    for i in range(png_hight):
        for j in range(png_width):
            x1 = gray_list_1[i - 1][j - 1]
            x2 = gray_list_1[i - 1][j]
            x3 = gray_list_1[i - 1][(j + 1) % png_width]
            y1 = gray_list_1[i][j - 1]
            y2 = gray_list_1[i][j]
            y3 = gray_list_1[i][(j + 1)% png_width ]
            z1 = gray_list_1[(i + 1)% png_hight ][j - 1]
            z2 = gray_list_1[(i + 1) % png_hight][j]
            z3 = gray_list_1[(i + 1)% png_hight ][(j + 1) % png_width]
            if j == 0:
                x1, y1, z1 = 0, 0, 0
            elif j == png_width - 1:
                x3, y3, z3 = 0, 0, 0
            if i == 0:
                x1, x2, x3 = 0, 0, 0
            elif i == png_hight - 1:
                z1, z2, z3 = 0, 0, 0
            a = -1 * x1 + 1 * x3 + -2 * y1 + 2 * y3 + -1 * z1 + 1 * z3
            b = -1 * z1 + 1 * x1 + -2 * z2 + 2 * x2 + -1 * z3 + 1 * x3

            if (a ** 2 + b ** 2) ** (1 / 2) < boundary:
                gray_list_2[i][j] = 255
            else:
                gray_list_2[i][j] = 0
            Data_list[i][3 * j + 1], Data_list[i][3*j+2], Data_list[i][3*j+3] =\
               gray_list_2[i][j],gray_list_2[i][j],gray_list_2[i][j]
    Data_list = filter(Data_list, png_hight, png_width)
    newdata = []
    for x in range(png_hight):
            for y in range(3*png_width+1):
                Data_list[x][y]=int(Data_list[x][y])
    for i in Data_list:
        newdata += i
 
    unzipbytes = bytearray(newdata)

    zipbytes = compress(bytes(unzipbytes))
    testfile = open("C:\\Users\\y\\Desktop\\ps后端实习\\test7.png", mode='w+b')
    testfile.write(beginlist + len(zipbytes).to_bytes(length=4, byteorder='big') + \
            b'IDAT' + zipbytes + b'abcd' + endlist)
else:
    print("not png")
f.close()
testfile.close()   