import sys

# Get dtype from command line argument
dtype = np.float32 if len(sys.argv) < 2 else np.float16 if sys.argv[1] == 'fp16' else np.float32

# Create 512x512 matrices
a = np.random.rand(512, 512).astype(dtype)
b = np.random.rand(512, 512).astype(dtype)
c = np.matmul(a, b)
print(f"matmul complete: {c.shape} with {dtype}")

