// Function to calculate the difference in minutes between two times
int shijianjisuan1(char* start, char* end) {
    int h1, m1, s1, h2, m2, s2;
    sscanf(start, "%d:%d:%d", &h1, &m1, &s1);
    sscanf(end, "%d:%d:%d", &h2, &m2, &s2);

    // Convert the times to minutes
    int time1 = h1 * 60 + m1;
    int time2 = h2 * 60 + m2;

    // If the end time is earlier than the start time, it means the time has crossed midnight
    if (time2 < time1) {
        time2 += 24 * 60;  // Add 24 hours to the end time
    }

    return time2 - time1;
}