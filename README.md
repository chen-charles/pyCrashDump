pyCrashDump
========
python3 detailed crashdump generator for post-production debugging

## Usage

Generates full stack trace details (across all source files) as a log and a dump.  
* .log is a simple text version of the caller stack trace with code contexts  
* .dump (which includes a copy of .log) saves all preservable environmental details of all stack layers in *pickle* format for furthur analysis  

```
import exception
def a(): return 5/0

try: a()
except Exception as err: raise exception.error("your message", err)
```

## Generated Sample

[CrashDump.log](https://github.com/chen-charles/pyCrashDump/blob/master/sample/CrashDump.log)  

[CrashDump.dump](https://github.com/chen-charles/pyCrashDump/blob/master/sample/CrashDump.dump)  

## License

[Version 3 of the GNU Lesser General Public Licence (LGPLv3)](https://github.com/chen-charles/pyCrashDump/blob/master/LICENSE)  
