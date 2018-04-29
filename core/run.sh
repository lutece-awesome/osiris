gcc -o core.bin core.c -O2 -lpthread
gcc -o do.bin do.c -w
./core.bin 1500 67108864 67108864 67108864 "sample.in" "user.out" "sample.out" "./do.bin" "../checker/wcmp.bin sample.in user.out sample.out 1>/dev/null 2>&1"