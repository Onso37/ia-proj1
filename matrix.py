import time

size = int(input("Matrix size:"))

dim = size*size
matrix_a = [1 for i in range(dim)]
matrix_b = [(i//size+1) for i in range(dim)]
matrix_c = [0 for i in range(dim)]

start = time.time()

for i in range(size):
	for j in range(size):
		temp = 0
		for k in range(size):
			temp += matrix_a[i*size + k] * matrix_b[k*size + j]
		matrix_c[i*size + j] = temp

end = time.time()

print(f"Execution time is {end-start}")

print("Result matrix:")
for i in range(min(10, size)):
	print(matrix_c[i], end=" ")