# morton.pyx
#
# to build: python morton-setup.py build_ext --inplace

#cdef static unsigned int *B = [0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF]
#cdef static unsigned int *S = [1, 2, 4, 8]

ctypedef unsigned int UInt


def interleave(UInt x,UInt y):
	"""Interleave bits of two numbers using Binary Magic Numbers.
	From the book Bit Twiddling Hacks by Sean Eron Anderson."""

	cdef UInt *B = [0x55555555, 0x33333333, 0x0F0F0F0F, 0x00FF00FF]
	cdef UInt *S = [1, 2, 4, 8]

	#cdef UInt x # Interleave lower 16 bits of x and y, so the bits of x
	#cdef UInt y # are in the even positions and bits from y in the odd;
	cdef UInt z # z gets the resulting 32-bit Morton Number.  
	                # x and y must initially be less than 65536.

	x = (x | (x << S[3])) & B[3]
	x = (x | (x << S[2])) & B[2]
	x = (x | (x << S[1])) & B[1]
	x = (x | (x << S[0])) & B[0]

	y = (y | (y << S[3])) & B[3]
	y = (y | (y << S[2])) & B[2]
	y = (y | (y << S[1])) & B[1]
	y = (y | (y << S[0])) & B[0]

	z = x | (y << 1);

	return z