#include "percentcoding.h"


size_t percent_encode(const char *src, size_t len, char *dst, const char *tohex)
{
  const char *p;
  uint8_t c;
  char c0, c1;
  size_t size = 0;

  for (p=src; p-src<len; p++)
  {
    c = (uint8_t)*p;
    c0 = tohex[c*2];
    c1 = tohex[c*2+1];

    if (c0 | c1) {
      if (dst) { *dst++ = '%'; *dst++ = c0; *dst++ = c1; }
      size += 3;
    }
    else {
      if (dst) *dst++ = c;
      size += 1;
    }
  }

  return size;
}


size_t percent_decode(const char *src, size_t len, char *dst)
{
  const char *p;
  char c;
  int nibble = 0;
  unsigned char byte = 0;
  size_t size = 0;

  for (p=src; p-src<len; p++)
  {
    c = *p;

    if (nibble)
    {
      if (c >= '0' && c <= '9')
        byte |= (c - '0');
      else if (c >= 'a' && c <= 'f')
        byte |= 0xa + (c - 'a');
      else if (c >= 'A' && c <= 'F')
        byte |= 0xA + (c - 'A');
      else if (c == '%' && nibble == 1) {
        if (dst) *dst++ = '%';
        size++;
        nibble = byte = 0;
      }
      else {
          /* Invalid hex, copy previous token literally */
          do {
            char d = *(p-nibble);
            if (dst) *dst++ = d;
            size++;
          } while (nibble--);
          nibble = byte = 0;
      }

      if (nibble == 1) {
        nibble++;
        byte <<= 4;
      }
      else if (nibble == 2) {
        if (dst) *dst++ = (char)byte;
        ++size;
        nibble = byte = 0;
      }
    }
    else
    {
      if (c == '%')
        nibble = 1;
      else {
        if (dst) *dst++ = c;
        ++size;
      }
    }
  }

  return size;
}


/* Utility function. */

size_t btox(register uint8_t c, register char* s)
{
  register unsigned int pos;
  register uint8_t n;

  s+=1;

  for (pos=0; pos<2; pos++)
  {
    n = c & 0x0f;
    c >>= 4;

    if (s) {
      if (n < 10)
        *s-- = '0' + n;
      else
        *s-- = 'a' + (n - 10);
    }
  }

  return pos;
}

