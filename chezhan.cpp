#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <locale.h>
#include <wchar.h>

#define MAX_LINE_LENGTH 300
#define MAX_LINES 3500

char zhuangtai;//状态0查找成功，1查找相似车站，2无结果
int fangwei;//1北2南3西4东


typedef struct {
    char chezhan[50];
    char pinyinma[50];
    char pinyin[50];

} Station;

Station stations[MAX_LINES];

void loadStations() {
    FILE* file = fopen("chezhan.txt", "r");
    if (file == NULL) {
        printf("无法打开文件\n");
        return;
    }

    char line[MAX_LINE_LENGTH];
    int i = 0;
    while (fgets(line, sizeof(line), file)) {
        sscanf(line, "%[^,],%[^,],%[^,]", stations[i].chezhan, stations[i].pinyinma, stations[i].pinyin);
        i++;
    }

    fclose(file);
}

void searchStation(char* input) {
    for (int i = 0; i < MAX_LINES; i++) {
        if (strcmp(stations[i].chezhan, input) == 0) {
            printf("车站: %s, 拼音码: %s, 拼音: %s\n", stations[i].chezhan, stations[i].pinyinma, stations[i].pinyin);
            zhuangtai = 0;
            return;
        }
    }
    printf("未找到车站\n");
    zhuangtai = 2;
    return;
}

void xinZeng() {
    FILE* file;
    char xinzeng[50];
    printf("还没找到想要的车站？可以自己新增车站：");
    file = fopen("chezhan_new.txt", "a");
    if (file == NULL) {
        printf("无法打开文件\n");

    }
    scanf("%s", xinzeng);
    fprintf(file, "%s", xinzeng);
    fclose(file);
}void chezhan() {
    char input[50];
    setlocale(LC_ALL, "");
    wchar_t compare[100];
    char xinzeng[50];
    char bei[4] = "北";
    char dong[4] = "东";
    char nan[4] = "南";
    char xi[4] = "西";
    FILE* file;
    loadStations();
    do{
        printf("请输入车站名称: ");
        scanf("%s", input);
        getchar();
        searchStation(input);
        mbstowcs(compare, input, 100);
        wchar_t last_char = compare[wcslen(compare) - 1];  
        if (last_char == L'东' || last_char == L'南' || last_char == L'西' || last_char == L'北'){
            if (zhuangtai == 2) {
                xinZeng();
            }
        }
        else {
            if (zhuangtai == 2) {
                printf("\n或许想查：\n%s东\n%s南\n%s西\n%s北\n",input,input,input,input);
                printf("请输入方位词（1代表北，2代表南，3代表西，4代表东）：");
                scanf("%d", &fangwei);
            }
            if (fangwei == 1) {
                printf("继续查找%s北\n", input);
                strcat(input, bei);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
            else if (fangwei == 2) {
                printf("继续查找%s南\n", input);
                strcat(input, nan);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
            else if (fangwei == 3) {
                printf("继续查找%s西\n", input);
                strcat(input, xi);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
            else if (fangwei == 4) {
                printf("继续查找%s东\n", input);
                strcat(input, dong);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
        }
    } while (strcmp(input, "退出查询"));
    
}