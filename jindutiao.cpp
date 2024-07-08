
#include <windows.h> // for Sleep()

void displayProgressBar(int percentage) {
    int barWidth = 50; // 进度条长度

    printf("\r[");
    int pos = barWidth * percentage / 100;
    for (int i = 0; i < barWidth; ++i) {
        if (i < pos)
            printf("=");
        else
            printf(" ");
    }
    printf("] %d%%", percentage);
    fflush(stdout);
}

void jindutiao() {
    int progressIntervals[] = { 20, 34, 50, 70, 99 };
    const char* messages[] = {
        "访问文件...",
        "加载车站列表...",
        "加载2005年数据库...",
        "加载2024年数据库...",
        "清除缓存..."
    };

    int messageIndex = 0;
    for (int i = 1; i <= 100; i++) {
        displayProgressBar(i);

        if (messageIndex < sizeof(progressIntervals) / sizeof(progressIntervals[0]) && i == progressIntervals[messageIndex]) {
            printf("\n%s", messages[messageIndex]);
            fflush(stdout);

            if (i == 34 || i == 70) {
                Sleep(500);  // 等待2秒
            }
            else {
                Sleep(100);  // 等待1秒
            }
            messageIndex++;
            // 光标上移一行，继续显示进度条
            printf("\033[A");  // ANSI转义序列，上移一行
        }

        Sleep(10);  // 等待60毫秒以模拟整体6秒的进度（100个单位 x 60毫秒 = 6000毫秒 = 6秒）
    }

    printf("\n");
    system("cls");
    printf("[==================================================] 100% \n");
    printf("===================加载成功！欢迎使用====================");
}
