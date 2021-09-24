#include <stdio.h>
int main(){
    FILE*f=fopen("C:\\Users\\y\\Desktop\\ps后端实习\\test2.png","rb");
	if(f){
		fseek(f,16,0);//跳过数据头,长度,类型 
		unsigned char width[100]={0};
		unsigned char height[100]={0};
		fread(width,4,1,f);
		fread(height,4,1,f);
		printf("width:%d\n",width[3]+(width[2]*256)+(width[1]*256*256)+width[0]*256*256*256); 
		printf("height:%d\n",height[3]+(height[2]*256)+(height[1]*256*256)+(height[0]*256*256*256));
		printf("bitdeath：%d\n",fgetc(f)) ; 
	    printf("colortype:%d\n",fgetc(f)); 
     	printf("giltermethod:%d\n",fgetc(f)); 
    	printf("interlacemethod:%d\n",fgetc(f)); 
		
		
	}else
    {
        printf("err");
    }
	fclose(f);	
    return 0;
} 
