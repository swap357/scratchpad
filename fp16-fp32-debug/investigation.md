# FP16 vs FP32 performance investigation

## benchmarking results from llama3_simple.py
```bash
llama3.np % llama3_simple.py - FP32 vs FP16

Performance Comparison:
FP32 forward time: 0.0077s
FP16 forward time: 0.1612s
ratio (FP32/FP16): 0.05x

numerical differences (FP32 vs FP16):
logits_fp32: [[[-2.0439878  1.7101182 -2.04355   ... -2.0439973 -2.0439239 -2.0437572]]]
logits_fp16: [[[-2.045  1.719 -2.045 ... -2.045 -2.045 -2.045]]]
Max absolute diff: 4.11e-02
Mean absolute diff: 2.59e-03
Median absolute diff: 1.20e-03

Top 5 predictions
FP32 top-k: [29891  1497   952 29892 24867]
FP16 top-k: [29891   952  1497 29892 24867]
```

## test_matmul.py
```bash
llama3.np % cat test_matmul.py

import sys

# Get dtype from command line argument
dtype = np.float32 if len(sys.argv) < 2 else np.float16 if sys.argv[1] == 'fp16' else np.float32

# Create 512x512 matrices
a = np.random.rand(512, 512).astype(dtype)
b = np.random.rand(512, 512).astype(dtype)
c = np.matmul(a, b)
print(f"matmul complete: {c.shape} with {dtype}")
```

## dtrace results for fp32 matmul
```bash
(llama3.np) (base) swap357@Mac llama3.np % sudo dtrace -n 'pid$target::*gemm*:entry { trace(probefunc); }' -c 'python3 test_matmul.py fp32'
dtrace: system integrity protection is on, some features will not be available

dtrace: description 'pid$target::*gemm*:entry ' matched 35 probes
matmul done: (512, 512) with <class 'numpy.float32'>
dtrace: pid 51524 has exited
CPU     ID                    FUNCTION:NAME
 10  64210 cblas_dgemm$NEWLAPACK$ILP64:entry   cblas_dgemm$NEWLAPACK$ILP64      
 10  64210 cblas_dgemm$NEWLAPACK$ILP64:entry   cblas_dgemm$NEWLAPACK$ILP64      
 10  64197                  APL_dgemm:entry   APL_dgemm                        
 10  64210 cblas_dgemm$NEWLAPACK$ILP64:entry   cblas_dgemm$NEWLAPACK$ILP64      
  7  64205 cblas_sgemm$NEWLAPACK$ILP64:entry   cblas_sgemm$NEWLAPACK$ILP64      
  7  64195                  APL_sgemm:entry   APL_sgemm                        
```

## dtrace results for fp16 matmul
```bash
(llama3.np) (base) swap357@Mac llama3.np % sudo dtrace -n 'pid$target::*gemm*:entry { trace(probefunc); }' -c 'python3 test_matmul.py fp16'
dtrace: system integrity protection is on, some features will not be available

dtrace: description 'pid$target::*gemm*:entry ' matched 35 probes
matmul done: (512, 512) with <class 'numpy.float16'>
dtrace: pid 51556 has exited
CPU     ID                    FUNCTION:NAME
  9  64716 cblas_dgemm$NEWLAPACK$ILP64:entry   cblas_dgemm$NEWLAPACK$ILP64      
  9  64716 cblas_dgemm$NEWLAPACK$ILP64:entry   cblas_dgemm$NEWLAPACK$ILP64      
  9  64703                  APL_dgemm:entry   APL_dgemm                        
  9  64716 cblas_dgemm$NEWLAPACK$ILP64:entry   cblas_dgemm$NEWLAPACK$ILP64
```

## TLDR - np.matmul with fp16 does not use vectorized instructions, fp32 uses: 
```bash
7  64205 cblas_sgemm$NEWLAPACK$ILP64:entry   cblas_sgemm$NEWLAPACK$ILP64      
7  64195                  APL_sgemm:entry   APL_sgemm   
```

actual mul- fmla instructions are on APL_sgemm -> libBLAS.dylib`___lldb_unnamed_symbol5332