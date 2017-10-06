pyCrashDump
========
python detailed crashdump generator for post-production debugging  
supports both *python 2.x* and *python 3.x*

## Usage

Generates full stack trace details (across all source files) as a log and a dump.  
* simply wrap around your outer-most main function to capture all exceptions with in  
* .log is a simple text version of the caller stack trace with code contexts  
* .dump (which includes a copy of .log) saves all preservable environmental details of all stack layers in *pickle* format for furthur analysis  

```python
## python 3.x example

import exception
def _main(): return 5/0

if __name__ == "__main__":
    try: exit(_main())

    # if you are running python 2.x
    # then this should be
    # except Exception, err:
    except Exception as err:
        raise exception.error("your message", err)
```


## Generated Sample

[CrashDump.log](https://github.com/chen-charles/pyCrashDump/blob/master/sample/CrashDump.log)  

[CrashDump.dump](https://github.com/chen-charles/pyCrashDump/blob/master/sample/CrashDump.dump)  

## License

[Version 3 of the GNU Lesser General Public Licence (LGPLv3)](https://github.com/chen-charles/pyCrashDump/blob/master/LICENSE)  
