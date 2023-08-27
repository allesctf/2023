#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include <curl/curl.h>

__attribute__((noreturn)) void fail(const char* msg) {
	fprintf(stderr, "%s. bye!\n", msg);
	exit(1);
}

char buf[100] = { 0 };

int main(void)
{
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	CURL* handle = curl_easy_init();
	int menu = 0;
	while (true) {
		printf(" <----------- cUrLy ------------>\n");
		printf("0 => curl_easy_setopt with number\n");
		printf("1 => curl_easy_setopt with string\n");
		printf("2 => curl_easy_perform\n");
		printf(" <------------------------------>\n");
		if (scanf("%d", &menu) != 1) fail("couldn't read menu choice");
		switch (menu) {
			case 0:
			case 1: {
				CURLoption option;
				int option_ = 0;
				CURLcode res;
				printf("option? ");
				if (scanf("%d", &option_) != 1) fail("couldn't read CURLoption code");
				option = option_;
				if (menu == 0) {
					unsigned long long value = 0;
					printf("value? ");
					if (scanf("%llu", &value) != 1) fail("couldn't read option value");
					res = curl_easy_setopt(handle, option, value);
				} else {
					char buf[100] = { 0 };
					printf("string value? ");
					if (scanf("%99s", buf) != 1) fail("could't read option value");
					res = curl_easy_setopt(handle, option, buf);
				}

				if(res != CURLE_OK)
					fprintf(stderr, "curl_easy_setopt() failed: %s\n",
					        curl_easy_strerror(res));
				break;
			}
			case 2: {
				CURLcode res = curl_easy_perform(handle);
				if(res != CURLE_OK)
					fprintf(stderr, "curl_easy_perform() failed: %s\n",
					        curl_easy_strerror(res));
				break;
			}
			default:
				printf("bye\n");
				exit(0);
		}
	}
	return 0;
}
