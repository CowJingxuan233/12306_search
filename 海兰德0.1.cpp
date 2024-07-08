#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <windows.h>
#include "chezhan.cpp"
#include "liecheinfo.cpp"
#include "shijianjisuan1.cpp"
#include "jindutiao.cpp"
int main()
{
    jindutiao();
    system("cls");
    int choose;
    printf("---------------------\n");
    printf("海兰德复刻版\n");
    printf("输入1-5选择功能：\n");
    printf("1：查找车站信息\n");
    printf("2：查找列车信息\n");
    printf("3：定制运转\n");
    printf("4：查找线路信息\n");
    printf("5：下关站配属查询\n");
    printf("6：动车组交路\n");
    printf("---------------------\n");
    scanf("%d", &choose);
    switch(choose){
        case 1:
            system("cls");
            chezhan();
            break;

        case 2:
            system("cls");
            liecheinfo();
            break;
        case 4:
            printf("星期四\n");
            break;
        default:
            break;
    }
        




}
