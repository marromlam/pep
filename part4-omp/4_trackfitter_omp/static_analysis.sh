# #1 == avxsingle or avxdouble
objdump -C -D $1 | cut -f3| awk '{print $1}' | ../../wf  | sort -k2 
