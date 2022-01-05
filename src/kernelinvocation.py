from numba import cuda
import numpy

@cuda.jit
def my_kernel(io_array):
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    # Block width, i.e. number of threads per block
    bw = cuda.blockDim.x
    # Compute flattened index inside the array
    pos = tx + ty * bw
    if pos < io_array.size:  # Check array boundaries
        io_array[pos] *= 2 # do the computation

def kernel_invocation():

    data = numpy.ones(256)
    threadsperblock = 32 
    blockspergrid = (data.size + (threadsperblock - 1)) // threadsperblock

    my_kernel[blockspergrid, threadsperblock](data)

    print(data)

kernel_invocation()