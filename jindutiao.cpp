
#include <windows.h> // for Sleep()

void displayProgressBar(int percentage) {
    int barWidth = 50; // ����������

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
        "�����ļ�...",
        "���س�վ�б�...",
        "����2005�����ݿ�...",
        "����2024�����ݿ�...",
        "�������..."
    };

    int messageIndex = 0;
    for (int i = 1; i <= 100; i++) {
        displayProgressBar(i);

        if (messageIndex < sizeof(progressIntervals) / sizeof(progressIntervals[0]) && i == progressIntervals[messageIndex]) {
            printf("\n%s", messages[messageIndex]);
            fflush(stdout);

            if (i == 34 || i == 70) {
                Sleep(500);  // �ȴ�2��
            }
            else {
                Sleep(100);  // �ȴ�1��
            }
            messageIndex++;
            // �������һ�У�������ʾ������
            printf("\033[A");  // ANSIת�����У�����һ��
        }

        Sleep(10);  // �ȴ�60������ģ������6��Ľ��ȣ�100����λ x 60���� = 6000���� = 6�룩
    }

    printf("\n");
    system("cls");
    printf("[==================================================] 100% \n");
    printf("===================���سɹ�����ӭʹ��====================");
}
