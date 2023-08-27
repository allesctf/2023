// gcc -fPIC -shared -o solv.so solv.c -nostartfiles
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>

extern void** _rtld_global;

void needle(char*n, char*haystack, size_t haystack_size) {
	void* res = memmem(haystack, haystack_size, n, strlen(n));
	if (res)
		puts((char*)res);
	else
		printf("didn't find needle %s\n", n);
}

void __attribute__((constructor)) solve() {
	printf("_rtld_global: %p\n", _rtld_global);
	void* base = *_rtld_global;
	printf("base: %p\n", base);
	// TODO: is there a good way to get the .data section size?
	needle("FLAG{", base, 0x3000);
	needle("CSCG{", base, 0x3000);
}
