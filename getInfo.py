import hid
import time

devs = hid.enumerate(0x0665, 0x5161)

def parseQGS(s):
	parts = s.split(' ')
	bits = parts[11]

	results = {
	'acInputVoltage': float(parts[0]),
	'acInputFrequency': float(parts[1]),
	'acOutputVoltage': float(parts[2]),
	'acOutputFrequency': float(parts[3]),
	'acOutputCurrent': float(parts[4]),
	'acOutputLoadPercent': float(parts[5]),
	'temperature': float(parts[10]),
	'inputOn': (bits[2] != '1'),
	'batteryLow': (bits[3] == '1'),
	'buzzerCtrl': (bits[9] == '1'),
	'bypassActive': (bits[4] == '1'),
	'hasFault': (bits[5] == '1'),
	'testInProgress': (bits[7] == '1')
	}
	print(results)

def parseQMOD(s):
	if s == 'P':
		return 'Power On'
	if s == 'S':
		return 'Standby'
	if s == 'Y':
		return 'Bypass'
	if s == 'L':
		return 'Line'
	if s =='B':
		return 'Battery'
	return 'Unparsed: ' + s

def doCommand(d, cmd):
	d.write(b'\x00' + cmd.encode('ascii') + b'\r')
	resp = b''
	while True:
		buf = d.read(8, timeout=200)
		if len(buf) == 0:
			break;
		else:
			try:
				idx = buf.index(b'\r')
				resp += buf[0:idx]
			except ValueError:
				resp += buf
	return resp[1:].decode('ascii')

if len(devs) == 1:
	print('Good found only 1 ups')
	dev = devs[0]
	with hid.Device(path=dev['path']) as d:
		qgs = doCommand(d, 'QGS')
		parseQGS(qgs)
		qmod = doCommand(d, 'QMOD')
		print(qmod)
