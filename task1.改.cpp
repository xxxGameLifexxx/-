#include <stdio.h>
int main(){
    FILE*f=fopen("C:\\Users\\y\\Desktop\\ps���ʵϰ\\test2.png","rb");
	if(f)
	{    unsigned char length[5]={0};
         unsigned char type[5]={0};
    
	     fseek(f,8,0);//��������ͷ
	     while(1)   
		{
		     
            fread(length,1,4,f);//������ 
            int a=fread(type,1,4,f); //������ 
            type[a]='\0';
            int n=length[3]+length[2]*256+(length[1]*256*256)+(length[0]*256*256*256),i=0;
            
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
