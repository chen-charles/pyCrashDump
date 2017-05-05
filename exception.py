##    pyCrashDump - Python CrashDump Library
##    Copyright (C) 2017  Jianye Chen
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Lesser General Public
##    License as published by the Free Software Foundation; either
##    version 3 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Lesser General Public License for more details.
##
##    You should have received a copy of the GNU Lesser General Public
##    License along with this library; If not, see <http://www.gnu.org/licenses/>.
##

import os
import sys
import inspect
import time
import pickle

# presets
_print = print
def __void(*args): pass
if os.name == "nt":
	import ctypes
	__user32 = ctypes.windll.LoadLibrary("user32.dll")
	def __msgbox(text="Message", title="Title"): __user32.MessageBoxW(0,str(text),str(title),0x00000010|0x00000000|0x00001000|0x00010000|0x00040000)
else:
	def __msgbox(text="Message", title="Title"): _print(text)


# configurations

_CRASHDUMP_VERSION = 0

# debug
_print = print
_msgbox = __msgbox

# # release
# _print = __void
# _msgbox = __msgbox

# # silent
# _print = __void
# _msgbox = __void




_logfmt = \
'''================================================================================
Level		: %s
Timestamp	: %d
Exc.Type    : %s
RuntimeMsg	: %s
Traceback	: %s
'''

_stackinfo = \
'''
	Stack %s
		fname		: %s
		lineno		: %s
		func		: %s
		codectx		: %s
		index		: %s

'''

class error(Exception):
	def __init__(self, msg, err, e_level="Exception", c_context=10, logfile="CrashDump.log", dumpfile="CrashDump.dump"):
		_print("Starting CrashDump ... ")
		self.msg = msg
		addmsg = str()
		stackinfo = []
		if not issubclass(type(err), Exception): err = Exception(msg)
		self.error = err
		try: c_context = int(c_context)
		except ValueError: c_context = 10
		stack = inspect.trace(c_context)
		try:
			_print("-> collecting stack trace ... ")
			j = 0
			for i in map(list, stack):
				i[4] = "\n"+"".join(list(map(lambda x: "\t"*5+x, i[4])))
				t = (str(j), ) + tuple(map(str, i[1:]))
				stackinfo.append(_stackinfo%t)
				j += 1
			addmsg += "log->%s\t"%(os.getcwd()+os.sep+logfile)
		except Exception:
			addmsg += "log failed\t"
		finally:
			log_text = _logfmt%(str(e_level), int(time.time()), type(err).__name__, msg, "".join(stackinfo))

			try:
				if dumpfile is not None:
					_print("-> collecting final environmental data ... ")
					envdump = dict()
					envdump["version"] = _CRASHDUMP_VERSION
					envdump["error"] = err
					envdump["log"] = log_text

					j = 0
					for i in map(list, stack):
						locals = dict()
						globals = dict()
						for field, value in i[0].f_globals.items():
							try: globals[field] = pickle.dumps(value)
							except: globals[field] = pickle.dumps(str(value))
						for field, value in i[0].f_locals.items():
							try: locals[field] = pickle.dumps(value)
							except: locals[field] = pickle.dumps(str(value))
						envdump[j] = {"locals": locals, "globals": globals}
						j += 1
					envdump["nItems"] = j
					with open(dumpfile, "wb") as f: pickle.dump(envdump, f)
					addmsg += "envdump->%s\t"%(os.getcwd()+os.sep+dumpfile)
				else:
					addmsg += "envdump disabled\t"
			except Exception:
				addmsg += "envdump failed\t"
			finally:
				del stack

		with open(str(logfile), "w") as f: f.write(log_text)

		_print("-> Finished. ")
		_msgbox("CrashDump Result:\n"+addmsg.replace("\t", "\n"), "CrashDump")

	def __str__(self): return type(self.error).__name__ + "(" + str(self.error) + "): " + self.msg




def _main(): raise error("An Exception Is Raised!", ValueError)
if __name__ == "__main__": exit(_main())

