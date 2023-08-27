#include "raylib.h"
#include "util.h"

#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

enum { FMT_MONO, FMT_RGB };

static int frame_width = 800;
static int frame_height = 600;
static int target_fps = 24;
static int zoom = 1;

static int format_type = FMT_MONO;
static uint8_t format_bpp = 1;

static uint8_t *pixels = NULL;
static size_t pixel_cnt = 0;

int (*cleanup)(void) = NULL;
const char *progname = "tis256-vis";

int
main(int argc, char **argv)
{
	char **arg;
	uint8_t *b;
	int x, y;
	size_t i;
	Color c;

	for (arg = argv + 1; *arg; arg++) {
		if (!strcmp(*arg, "--width")) {
			frame_width = atoi(*++arg);
			if (frame_width <= 0) die("bad width '%s'", *arg);
		} else if (!strcmp(*arg, "--height")) {
			frame_height = atoi(*++arg);
			if (frame_height <= 0) die("bad width '%s'", *arg);
		} else if (!strcmp(*arg, "--zoom")) {
			zoom = atoi(*++arg);
			if (zoom <= 0) die("bad zoom '%s'", *arg);
		} else if (!strcmp(*arg, "--format")) {
			arg += 1;
			if (!strcmp(*arg, "mono")) {
				format_type = FMT_MONO;
				format_bpp = 1;
			} else if (!strcmp(*arg, "rgb")) {
				format_type = FMT_RGB;
				format_bpp = 3;
			} else {
				die("bad format '%s'", *arg);
			}
		} else if (!strcmp(*arg, "--fps")) {
			target_fps = atoi(*++arg);
			if (target_fps <= 0) die("bad fps '%s'", *arg);
		} else {
			die("invalid arg '%s'", *arg);
		}
	}

	InitWindow(frame_width * zoom, frame_height * zoom, "tis256-vis");

	pixel_cnt = (size_t) frame_width * (size_t) frame_height * format_bpp;
	pixels = malloc(pixel_cnt);
	if (!pixels) die("malloc:");

	c = (Color) { 255, 255, 255, 255 };
	while (!WindowShouldClose()) {
		BeginDrawing();
		ClearBackground(BLACK);
		if (fread(pixels, pixel_cnt, 1, stdin) != 1)
			break;
		for (b = pixels, i = 0; i < pixel_cnt; i++, b++) {
			switch (format_type) {
			case FMT_MONO:
				c.r = c.g = c.b = *b;
				break;
			case FMT_RGB:
				switch (i % format_bpp) {
				case 0:
					c.r = *b;
					break;
				case 1:
					c.g = *b;
					break;
				case 2:
					c.b = *b;
					break;
				}
			}
			if (i % format_bpp == format_bpp - 2) {
				x = ((int) i / format_bpp) % frame_width;
				y = ((int) i / format_bpp) / frame_width;
				DrawRectangle(x * zoom, y * zoom, zoom, zoom, c);
			}
		}
		EndDrawing();
	}

exit:
	CloseWindow();
}
