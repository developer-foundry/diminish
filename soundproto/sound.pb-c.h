/* Generated by the protocol buffer compiler.  DO NOT EDIT! */
/* Generated from: sound.proto */

#ifndef PROTOBUF_C_sound_2eproto__INCLUDED
#define PROTOBUF_C_sound_2eproto__INCLUDED

#include <protobuf-c/protobuf-c.h>

PROTOBUF_C__BEGIN_DECLS

#if PROTOBUF_C_VERSION_NUMBER < 1000000
# error This file was generated by a newer version of protoc-c which is incompatible with your libprotobuf-c headers. Please update your headers.
#elif 1003001 < PROTOBUF_C_MIN_COMPILER_VERSION
# error This file was generated by an older version of protoc-c which is incompatible with your libprotobuf-c headers. Please regenerate this file with a newer version of protoc-c.
#endif


typedef struct _Soundwave__SoundWave Soundwave__SoundWave;
typedef struct _Soundwave__SoundWave__Sample Soundwave__SoundWave__Sample;


/* --- enums --- */


/* --- messages --- */

struct  _Soundwave__SoundWave__Sample
{
  ProtobufCMessage base;
  double first;
  double second;
};
#define SOUNDWAVE__SOUND_WAVE__SAMPLE__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&soundwave__sound_wave__sample__descriptor) \
    , 0, 0 }


struct  _Soundwave__SoundWave
{
  ProtobufCMessage base;
  char *name;
  size_t n_samples;
  Soundwave__SoundWave__Sample **samples;
};
#define SOUNDWAVE__SOUND_WAVE__INIT \
 { PROTOBUF_C_MESSAGE_INIT (&soundwave__sound_wave__descriptor) \
    , NULL, 0,NULL }


/* Soundwave__SoundWave__Sample methods */
void   soundwave__sound_wave__sample__init
                     (Soundwave__SoundWave__Sample         *message);
/* Soundwave__SoundWave methods */
void   soundwave__sound_wave__init
                     (Soundwave__SoundWave         *message);
size_t soundwave__sound_wave__get_packed_size
                     (const Soundwave__SoundWave   *message);
size_t soundwave__sound_wave__pack
                     (const Soundwave__SoundWave   *message,
                      uint8_t             *out);
size_t soundwave__sound_wave__pack_to_buffer
                     (const Soundwave__SoundWave   *message,
                      ProtobufCBuffer     *buffer);
Soundwave__SoundWave *
       soundwave__sound_wave__unpack
                     (ProtobufCAllocator  *allocator,
                      size_t               len,
                      const uint8_t       *data);
void   soundwave__sound_wave__free_unpacked
                     (Soundwave__SoundWave *message,
                      ProtobufCAllocator *allocator);
/* --- per-message closures --- */

typedef void (*Soundwave__SoundWave__Sample_Closure)
                 (const Soundwave__SoundWave__Sample *message,
                  void *closure_data);
typedef void (*Soundwave__SoundWave_Closure)
                 (const Soundwave__SoundWave *message,
                  void *closure_data);

/* --- services --- */


/* --- descriptors --- */

extern const ProtobufCMessageDescriptor soundwave__sound_wave__descriptor;
extern const ProtobufCMessageDescriptor soundwave__sound_wave__sample__descriptor;

PROTOBUF_C__END_DECLS


#endif  /* PROTOBUF_C_sound_2eproto__INCLUDED */