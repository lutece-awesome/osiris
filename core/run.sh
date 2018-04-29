rm data.out
gcc -o core.bin core.c -O2 -lpthread
gcc -o do.bin do.c -w
./core.bin 1500 67108864 67108864 67108864 "./do.bin >data.out 2>/dev/null"