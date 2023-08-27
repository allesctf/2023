#include <pybind11/pybind11.h>

unsigned int key[4]={0xAEF8,0x17FF,0x3137,0x0420}; 

void do_round(uint32_t state, uint32_t *v0, uint32_t* v1, uint32_t* sum, uint32_t const key[4]){
    switch(state){
        case 0:
            *v1 -= (((*v0 << 4) ^ (*v0 >> 5)) + *v0) ^ (*sum + key[(*sum>>11) & 3]);
            break;
        case 1:
            *sum += 0x8647;
            break;
        case 2:
            *sum -= 0x9e380000;
            break;
        case 3:
            *v0 -= (((*v1 << 4) ^ (*v1 >> 5)) + *v1) ^ (*sum + key[*sum & 3]);
        default:
            break;
    }
}

uint64_t decipher(uint64_t v, uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=(v>>32)&0xFFFFFFFF, v1=v&0xFFFFFFFF, sum=0xaa66d2b0;
    for (i=0; i < 48*4; i++) {
        do_round(i&0b11, &v0, &v1, &sum, key);
    }
    uint64_t ret = v0;
    return (ret<<32) | v1;
}

/*
uint64_t encipher(uint64_t v, uint32_t const key[4]) {
    unsigned int i;
    uint32_t v0=(v>>32)&0xFFFFFFFF, v1=v&0xFFFFFFFF, sum=0, delta=0x9E3779B9;
    for (i=0; i < 48; i++) {
        v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum>>11) & 3]);
    }
    uint64_t ret = v0;
    return (ret<<32) | v1;
}

uint64_t gen_license(uint64_t license) {
    return encipher(license, key);
}
*/

int check_license(uint64_t license) {
    switch (decipher(license, key)) {
        case 420:
            return 1;
        case 1337:
            return 2;
        default:
            return 0;
    }
}

PYBIND11_MODULE(license_checker, m) {
    m.doc() = "license checker";

    m.def("check_license", &check_license, "check if license is valid");
 //   m.def("gen_license", &gen_license, "generate license");
}