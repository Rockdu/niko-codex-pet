# Animation source format

The atlas has eight columns and eleven rows. Each cell is 192 × 208 pixels;
the complete image is 1536 × 2288 pixels. `pet/pet.json` declares
`spriteVersionNumber: 2`.

| Row | State | Used cells |
| --- | --- | --- |
| 0 | Idle | 6, plus neutral in column 6 |
| 1 | Running right | 8 |
| 2 | Running left | 8 |
| 3 | Waving | 4 |
| 4 | Jumping | 5 |
| 5 | Failed | 8 |
| 6 | Waiting | 6 |
| 7 | Working / lamp interaction | 6 |
| 8 | Review | 6 |
| 9–10 | Look directions | 16 total, clockwise from up |

The app advances atlas coordinates to select poses. This pet also uses an
animated WebP container to control idle timing. Each of its sixteen temporal
frames has identical artwork outside the first six idle cells. Those six cells
contain the same idle pose within each temporal frame, so whichever idle column
the app selects shows the current blink and body movement.

The temporal durations total 6,220 ms. Blink phases last 60 ms closing,
90 ms closed, and 70 ms opening. All idle poses use the exact same lower rows
177–207, keeping the boots and sole pixels fixed while the upper body dips.
The jump row uses five poses: crouch, toe push-off, tucked feet in the air,
landing compression, and settled stance.

`source/atlas.webp` is the editable static atlas. `source/idle/*.webp` contains
the sixteen full-size idle cells, in the order listed in `source/animation.json`.
The build tool copies each idle cell into the first six columns and uses
lossless `webpmux` assembly. It verifies every decoded RGBA pixel and frame
duration against the input before finishing. Encoder versions may produce
different file hashes while preserving identical pixels and timing.

These are the final editable raster sources. Rebuilding does not repeat the
AI generation process or require proprietary skill files, model access,
credentials, or the original work environment.

The static fallback contains ordinary atlas poses. It omits the extra intrinsic
WebP timing. Some hosts may freeze atlas coordinates for reduced motion or
thumbnails without pausing the WebP itself; use `--static` if that behavior is
undesirable. The native desktop widget is not automatically refreshed by the
installer.
