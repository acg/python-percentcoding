#ifndef __PERCENTCODING_PERCENTCODING_H__
#define __PERCENTCODING_PERCENTCODING_H__

#include <sys/types.h>
#include <inttypes.h>

size_t percent_encode(const char *src, size_t len, char *dst, const char *tohex);

size_t percent_decode(const char *src, size_t len, char *dst);

size_t btox(register uint8_t c, register char* s);

#endif

