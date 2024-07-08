#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <locale.h>
#include <wchar.h>

#define MAX_LINE_LENGTH 300
#define MAX_LINES 3500

char zhuangtai;//״̬0���ҳɹ���1�������Ƴ�վ��2�޽��
int fangwei;//1��2��3��4��


typedef struct {
    char chezhan[50];
    char pinyinma[50];
    char pinyin[50];

} Station;

Station stations[MAX_LINES];

void loadStations() {
    FILE* file = fopen("chezhan.txt", "r");
    if (file == NULL) {
        printf("�޷����ļ�\n");
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
            printf("��վ: %s, ƴ����: %s, ƴ��: %s\n", stations[i].chezhan, stations[i].pinyinma, stations[i].pinyin);
            zhuangtai = 0;
            return;
        }
    }
    printf("δ�ҵ���վ\n");
    zhuangtai = 2;
    return;
}

void xinZeng() {
    FILE* file;
    char xinzeng[50];
    printf("��û�ҵ���Ҫ�ĳ�վ�������Լ�������վ��");
    file = fopen("chezhan_new.txt", "a");
    if (file == NULL) {
        printf("�޷����ļ�\n");

    }
    scanf("%s", xinzeng);
    fprintf(file, "%s", xinzeng);
    fclose(file);
}void chezhan() {
    char input[50];
    setlocale(LC_ALL, "");
    wchar_t compare[100];
    char xinzeng[50];
    char bei[4] = "��";
    char dong[4] = "��";
    char nan[4] = "��";
    char xi[4] = "��";
    FILE* file;
    loadStations();
    do{
        printf("�����복վ����: ");
        scanf("%s", input);
        getchar();
        searchStation(input);
        mbstowcs(compare, input, 100);
        wchar_t last_char = compare[wcslen(compare) - 1];  
        if (last_char == L'��' || last_char == L'��' || last_char == L'��' || last_char == L'��'){
            if (zhuangtai == 2) {
                xinZeng();
            }
        }
        else {
            if (zhuangtai == 2) {
                printf("\n������飺\n%s��\n%s��\n%s��\n%s��\n",input,input,input,input);
                printf("�����뷽λ�ʣ�1������2�����ϣ�3��������4��������");
                scanf("%d", &fangwei);
            }
            if (fangwei == 1) {
                printf("��������%s��\n", input);
                strcat(input, bei);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
            else if (fangwei == 2) {
                printf("��������%s��\n", input);
                strcat(input, nan);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
            else if (fangwei == 3) {
                printf("��������%s��\n", input);
                strcat(input, xi);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
            else if (fangwei == 4) {
                printf("��������%s��\n", input);
                strcat(input, dong);
                searchStation(input);
                if (zhuangtai == 2) {
                    xinZeng();
                }
            }
        }
    } while (strcmp(input, "�˳���ѯ"));
    
}