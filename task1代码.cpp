#include <stdio.h>
int main(){
    FILE*f=fopen("C:\\Users\\y\\Desktop\\ps后端实习\\test2.png","rb");
	if(f)
	{    unsigned char length[5]={0};
         unsigned char type[5]={0};
    
	     fseek(f,8,0);//跳过数据头
	     while(1)   
		{
		     
            int a=fread(length,1,4,f);//读长度 
            int b=fread(type,1,4,f); //读类型 
            length[a]='\0';
            type[b]='\0';
            int n=(length[0] << 24) + (length[1] << 16) + (length[2] << 8) + length[3],i=0;
            
			printf("length=%8d",n);
            printf("type:%s",type);
            printf("crc:");
            fseek(f,n,1);
            for(i=1;i<=4 ;i++) {
            	printf("%3d,",fgetc(f));
		    }
		    printf("\n");
			if(n==0){
				break;
			}   
	    } ;
    }else
    {
        printf("err");
    }
	fclose(f);	
    return 0;
}
