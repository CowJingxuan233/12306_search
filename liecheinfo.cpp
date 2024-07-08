#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//时间计算
int time_diff(char* start, char* end) {
    int h1, m1, s1, h2, m2, s2;
    sscanf(start, "%d:%d:%d", &h1, &m1, &s1);
    sscanf(end, "%d:%d:%d", &h2, &m2, &s2);

    int time1 = h1 * 60 + m1;
    int time2 = h2 * 60 + m2;

    if (time2 < time1) {
        time2 += 24 * 60;
    }

    return time2 - time1;
}

void liecheinfo() {
    char train_num[10];
    char prev_time[10] = "";

    FILE* file = fopen("train2007.txt", "r");
    if (file == NULL) {
        printf("打不开\n");
        return;
    }

    do {
        printf("请输入车次：");
        scanf("%s", train_num);

        char line[256];
        int found = 0;
        while (fgets(line, sizeof(line), file)) {
            char num1[10], num2[10];
            char station[50], time1[10], time2[10];

            sscanf(line, "%[^,],%[^,],%*d,%[^,],%[^,],%s", num1, num2, station, time1, time2);



            if ((strcmp(num1, train_num) == 0 || strcmp(num2, train_num) == 0)) {
                if (strcmp(num2, "nan") == 0) {
                    int stay_time = time_diff(time1, time2);
                    int total_time = strcmp(prev_time, "") == 0 ? 0 : time_diff(prev_time, time1);
                    if (strcmp(time1, "START") == 0) {
                        printf("车次: %s\t站名: %s\t始发站, 出站时间: %s\n", num1, station, time2);
                        found = 1;
                        strcpy(prev_time, time2);
                    }
                    else if (strcmp(time1, time2) == 0) {
                        printf("车次: %s\t站名: %s\t终点站\t到站时间: %s", num1, station, time2);
                        if (total_time >= 60) {
                            printf(", 历时: %d小时%d分钟\n", total_time / 60, total_time - 60 * (total_time / 60));
                        }
                        else {
                            printf(", 历时: %d分钟\n", total_time);
                        }
                    }
                    else {
                        printf("车次: %s\t站名: %s\t到站时间: %s, 停留: %d分钟, 出站时间: %s", num1, station, time1, stay_time, time2);
                        if (stay_time >= 15) {
                            printf(", **可能换挂**");
                        }
                        if (total_time >= 60) {
                            printf(", 历时: %d小时%d分钟\n", total_time / 60, total_time - 60 * (total_time / 60));
                        }
                        else {
                            printf(", 历时: %d分钟\n", total_time);
                        }
                        found = 1;
                        strcpy(prev_time, time2);
                    }
                }
                else {
                    if ((strcmp(num1, train_num) == 0 || strcmp(num2, train_num) == 0)) {
                        int stay_time = time_diff(time1, time2);
                        int total_time = strcmp(prev_time, "") == 0 ? 0 : time_diff(prev_time, time1);
                        if (strcmp(time1, "START") == 0) {
                            printf("车次: %s/%s\t站名: %s\t始发站, 出站时间: %s\n", num1, num2, station, time2);
                            found = 1;
                            strcpy(prev_time, time2);
                        }
                        else if (strcmp(time1, time2) == 0) {
                            printf("车次: %s/%s\t站名: %s\t终点站,到站时间: %s", num1, num2, station, time2);
                            if (total_time >= 60) {
                                printf(", 历时: %d小时%d分钟\n", total_time / 60, total_time - 60 * (total_time / 60));
                            }
                            else {
                                printf(", 历时: %d分钟\n", total_time);
                            }
                        }
                        else {
                            printf("车次: %s/%s\t站名: %s\t到站时间: %s, 停留: %d分钟, 出站时间: %s", num1, num2, station, time1, stay_time, time2);
                            if (stay_time >= 15) {
                                printf(", **可能换挂**");
                            }
                            if (total_time >= 60) {
                                printf(", 历时: %d小时%d分钟\n", total_time / 60, total_time - 60 * (total_time / 60));
                            }
                            else {
                                printf(", 历时: %d分钟\n", total_time);
                            }
                            found = 1;
                            strcpy(prev_time, time2);
                        }
                    }
                }
            }
        }

        if (!found) {
            printf("未找到车次\n");
        }

        // Reset the file pointer to the beginning of the file
        fseek(file, 0, SEEK_SET);

    } while (strcmp(train_num, "exit") != 0);

    fclose(file);
}