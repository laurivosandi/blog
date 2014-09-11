.. title: Implementing MP3 player in C
.. author: Lauri Võsandi <lauri.vosandi@gmail.com>
.. date: 2013-12-15
.. tags: libmad, MP3, zero-copy, mmap, PulseAudio, libao

Implementing MP3 player in C
============================

Surprised by the lack of English-written articles about MP3 decoding in C,
I thought that I should put down a couple of words about that.

First of all, there are many was to read a file. Most modern operating
systems have `mmap() <http://en.wikipedia.org/wiki/Mmap>`_ syscall,
which basically maps the file contents to virtual memory space,
which means that you can access the file just
by reading an address in memory. The kernel transparently fetches 
a chunk of file from the harddisk and caches it in the physical memory.
This makes dozen tasks easier - no need to keep track of buffers and
reduces excessive copies in memory thus getting one step closer to
`zero-copy <http://en.wikipedia.org/wiki/Zero-copy>`_ architecture.

Secondly, there are many libraries for decoding particular audio format.
Even for MP3 there are several:
LGPL v2.1 licensed `libmpg123 <http://www.mpg123.de/>`_,
GPL v2 licensed `libmad <http://sourceforge.net/projects/mad/>`_ and
LGPL licensed `liblame <http://lame.sourceforge.net/>`_.
Note that *libmad* is using fixed-point arithmetic which performs
several times better on FPU-less ARM processors which suck at floating point
arithmetic. You might find an ARM processor in a mobile phone,
NAS-box, Cubieboard and in a Raspberry Pi.

Thirdly and finally there are many libraries for audio output. Note that 
decoder library produces simply PCM-audio samples. In case of Linux based
machines one could directly use
`alsa-lib <http://www.alsa-project.org/main/index.php/Main_Page>`_
feed the samples to kernel, which in turn transfers them to the audio chip.
Modern distributions intercept ALSA output and hook those applications to the
`PulseAudio <http://www.freedesktop.org/wiki/Software/PulseAudio/>`_ audioserver.
PulseAudio allows on-the-fly switching of audio output between headphones,
HDMI output or Bluetooth headset and other fancy stuff that you would expect 
from modern operating system. In that case one might use PulseAudio libraries to
feed the PCM samples directly to PulseAudio server.
There are of course libraries like `libao <http://www.xiph.org/ao/>`_ 
which build yet another abstraction layer on top of ALSA, PulseAudio and others,
but at the moment of writing it seems to be not so well maintained in Ubuntu package management.

So, here goes a sample using libmad and libpulse:

.. code:: c

    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <sys/stat.h>
    #include <sys/mman.h>
    #include <mad.h>
    #include <pulse/simple.h>
    #include <pulse/error.h>

    pa_simple *device = NULL;
    int ret = 1;
    int error;
    struct mad_stream mad_stream;
    struct mad_frame mad_frame;
    struct mad_synth mad_synth;

    void output(struct mad_header const *header, struct mad_pcm *pcm);

    int main(int argc, char **argv) {
        // Parse command-line arguments
        if (argc != 2) {
            fprintf(stderr, "Usage: %s [filename.mp3]", argv[0]);
            return 255;
        }

        // Set up PulseAudio 16-bit 44.1kHz stereo output
        static const pa_sample_spec ss = { .format = PA_SAMPLE_S16LE, .rate = 44100, .channels = 2 };
        if (!(device = pa_simple_new(NULL, "MP3 player", PA_STREAM_PLAYBACK, NULL, "playback", &ss, NULL, NULL, &error))) {
            printf("pa_simple_new() failed\n");
            return 255;
        }

        // Initialize MAD library
        mad_stream_init(&mad_stream);
        mad_synth_init(&mad_synth);
        mad_frame_init(&mad_frame);

        // Filename pointer
        char *filename = argv[1];

        // File pointer
        FILE *fp = fopen(filename, "r");
        int fd = fileno(fp);

        // Fetch file size, etc
        struct stat metadata;
        if (fstat(fd, &metadata) >= 0) {
            printf("File size %d bytes\n", (int)metadata.st_size);
        } else {
            printf("Failed to stat %s\n", filename);
            fclose(fp);
            return 254;
        }

        // Let kernel do all the dirty job of buffering etc, map file contents to memory
        char *input_stream = mmap(0, metadata.st_size, PROT_READ, MAP_SHARED, fd, 0);

        // Copy pointer and length to mad_stream struct
        mad_stream_buffer(&mad_stream, input_stream, metadata.st_size);

        // Decode frame and synthesize loop
        while (1) {

            // Decode frame from the stream
            if (mad_frame_decode(&mad_frame, &mad_stream)) {
                if (MAD_RECOVERABLE(mad_stream.error)) {
                    continue;
                } else if (mad_stream.error == MAD_ERROR_BUFLEN) {
                    continue;
                } else {
                    break;
                }
            }
            // Synthesize PCM data of frame
            mad_synth_frame(&mad_synth, &mad_frame);
            output(&mad_frame.header, &mad_synth.pcm);
        }

        // Close 
        fclose(fp);

        // Free MAD structs
        mad_synth_finish(&mad_synth);
        mad_frame_finish(&mad_frame);
        mad_stream_finish(&mad_stream);

        // Close PulseAudio output
        if (device)
            pa_simple_free(device);

        return EXIT_SUCCESS;
    }

    // Some helper functions, to be cleaned up in the future
    int scale(mad_fixed_t sample) {
         /* round */
         sample += (1L << (MAD_F_FRACBITS - 16));
         /* clip */
         if (sample >= MAD_F_ONE)
             sample = MAD_F_ONE - 1;
         else if (sample < -MAD_F_ONE)
             sample = -MAD_F_ONE;
         /* quantize */
         return sample >> (MAD_F_FRACBITS + 1 - 16);
    }
    void output(struct mad_header const *header, struct mad_pcm *pcm) {
        register int nsamples = pcm->length;
        mad_fixed_t const *left_ch = pcm->samples[0], *right_ch = pcm->samples[1];
        static char stream[1152*4];
        if (pcm->channels == 2) {
            while (nsamples--) {
                signed int sample;
                sample = scale(*left_ch++);
                stream[(pcm->length-nsamples)*4 ] = ((sample >> 0) & 0xff);
                stream[(pcm->length-nsamples)*4 +1] = ((sample >> 8) & 0xff);
                sample = scale(*right_ch++);
                stream[(pcm->length-nsamples)*4+2 ] = ((sample >> 0) & 0xff);
                stream[(pcm->length-nsamples)*4 +3] = ((sample >> 8) & 0xff);
            }
            if (pa_simple_write(device, stream, (size_t)1152*4, &error) < 0) {
                fprintf(stderr, "pa_simple_write() failed: %s\n", pa_strerror(error));
                return;
            }
        } else {
            printf("Mono not supported!");
        }
    }

You may compile this snippet by linking against the appropriate libraries:

.. code:: bash

    gcc -o player player.c -lpulse -lpulse-simple -lmad -g

On Ubuntu you of course have to first install the dependencies:

.. code:: bash

    sudo apt-get install libpulse-dev libmad0-dev libpulse0 libmad

References:

* `MPEG audio decoder <http://en.wikipedia.org/wiki/MPEG_Audio_Decoder>`_
* `libmad+libao <http://home.eeworld.com.cn/my/space-uid-179477-blogid-32464.html>`_
* `libmad - MPEG audio decoding library: low level API <http://m.baert.free.fr/contrib/docs/libmad/doxy/html/low-level.html>`_
* `Steven's space <http://hi.baidu.com/steven926/item/44ad7e7c5a93ef336cc37c6b>`_
