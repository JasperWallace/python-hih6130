import smbus
from datetime import datetime

__all__ = ['HIH6130']


class HIH6130:
	'''
		HIH6130() defines a new RHT sensor with default address of 0x27.
	'''
	def __init__(self, address = 0x27):
		self.address = address
		self.status = None
		self.rh = None
		self.t = None
		self._buffer = None
		self.timestamp = None
		
		try:
			self.i2c = smbus.SMBus(1)
		except:
			raise IOError("Could not find i2c device.")

	def read(self):
		'''
			read from the i2c bus at address defined above.
		'''
		try:
			self._buffer = self.i2c.read_i2c_block_data(self.address, 0, 4)
		except:
			raise IOError("Could not read from i2c device located at %s." % self.address )
		
		self.timestamp = datetime.now()
		self.status = self._buffer[0] >> 6 & 0x03
		self.rh = round(((self._buffer[0] & 0x3f) << 8 | self._buffer[1]) * 100.0 / (2**14 - 1), 2)
		self.t = round((float((self._buffer[2] << 6) + (self._buffer[3] >> 2)) / (2**14 - 1)) * 165.0 - 40, 2)

		return