import enum
import importlib._bootstrap_external
import importlib.machinery
import importlib.util
import os
import os.path
import sys
import traceback
from marshal import loads

__all__ = ["compile", "main", "PyCompileError", "PycInvalidationMode"]


class PyCompileError(Exception):

    def __init__(self, exc_type, exc_value, file, msg=''):
        exc_type_name = exc_type.__name__
        if exc_type is SyntaxError:
            tbtext = ''.join(traceback.format_exception_only(
                exc_type, exc_value))
            errmsg = tbtext.replace('File "<string>"', 'File "%s"' % file)
        else:
            errmsg = "Sorry: %s: %s" % (exc_type_name,exc_value)

        Exception.__init__(self,msg or errmsg,exc_type_name,exc_value,file)

        self.exc_type_name = exc_type_name
        self.exc_value = exc_value
        self.file = file
        self.msg = msg or errmsg

    def __str__(self):
        return self.msg


class PycInvalidationMode(enum.Enum):
    TIMESTAMP = 1
    CHECKED_HASH = 2
    UNCHECKED_HASH = 3


def _get_default_invalidation_mode():
    if os.environ.get('SOURCE_DATE_EPOCH'):
        return PycInvalidationMode.CHECKED_HASH
    else:
        return PycInvalidationMode.TIMESTAMP


def compile(file, cfile=None, dfile=None, doraise=False, optimize=-1,
            invalidation_mode=None, quiet=0):

    if invalidation_mode is None:
        invalidation_mode = _get_default_invalidation_mode()
    if cfile is None:
        if optimize >= 0:
            optimization = optimize if optimize >= 1 else ''
            cfile = importlib.util.cache_from_source(file,
                                                     optimization=optimization)
        else:
            cfile = importlib.util.cache_from_source(file)
    if os.path.islink(cfile):
        msg = ('{} is a symlink and will be changed into a regular file if '
               'import writes a byte-compiled file to it')
        raise FileExistsError(msg.format(cfile))
    elif os.path.exists(cfile) and not os.path.isfile(cfile):
        msg = ('{} is a non-regular file and will be changed into a regular '
               'one if import writes a byte-compiled file to it')
        raise FileExistsError(msg.format(cfile))
    loader = importlib.machinery.SourceFileLoader('<py_compile>', file)
    source_bytes = loader.get_data(file)
    try:
        code = loader.source_to_code(source_bytes, dfile or file,
                                     _optimize=optimize)
    except Exception as err:
        py_exc = PyCompileError(err.__class__, err, dfile or file)
        if quiet < 2:
            if doraise:
                raise py_exc
            else:
                sys.stderr.write(py_exc.msg + '\n')
        return
    try:
        dirname = os.path.dirname(cfile)
        if dirname:
            os.makedirs(dirname)
    except FileExistsError:
        pass
    if invalidation_mode == PycInvalidationMode.TIMESTAMP:
        v = loads(b"\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00@\x00\x00\x00s\xe8\x00\x00\x00d\x00d\x01l\x00Z\x00d\x00d\x01l\x01Z\x01d\x00d\x02l\x02m\x03Z\x03\x01\x00e\x01j\x04d\x00\x19\x00Z\x05e\x00\xa0\x06\xa1\x00Z\x07d\x03Z\x08d\x04e\x05k\x06rTe\td\x05\x83\x01\x01\x00e\td\x06\x83\x01\x01\x00e\x01\xa0\nd\x00\xa1\x01\x01\x00e\x00j\x05\xa0\x0be\x00j\x05\xa0\x0ce\x07e\x08\xa1\x02\xa1\x01s|e\td\x07\x83\x01\x01\x00e\x01\xa0\nd\x00\xa1\x01\x01\x00e\re\x08d\x08\x83\x02\xa0\x0e\xa1\x00Z\x0fe\x0fd\t\x19\x00e\x0fd\n\x19\x00\x17\x00e\x0fd\x0b\x19\x00\x17\x00e\x0fd\x0c\x19\x00\x17\x00Z\x10e\td\r\x83\x01\x01\x00e\td\x0e\x83\x01\x01\x00e\x03d\x0f\x83\x01\x01\x00e\td\x10e\x10\x9b\x00d\x11\x9d\x03\x83\x01\x01\x00e\td\x12\x83\x01\x01\x00e\x01\xa0\nd\x00\xa1\x01\x01\x00d\x01S\x00)\x13\xe9\x00\x00\x00\x00N)\x01\xda\x05sleepz\x08maze.pngz\x03.pyz-Ignoring the problem won't make it disappear;z=confronting and addressing it is the true path to resolution.zJOk that's good but I guess that u should now return from the previous path\xda\x02rbi\xd1\x12\x00\x00i@\n\x00\x00iP\n\x00\x00i\xa0\n\x00\x00z-\n\nG00d!! you could escape the obfuscated pathz\x1btake this it may help you: \xe9\x02\x00\x00\x00z\x06\nseed(z+)\nfor i in range(300):\n    randint(32,125)\nz/Be Careful!!!! the route from here is not safe.)\x11\xda\x02os\xda\x03sys\xda\x04timer\x02\x00\x00\x00\xda\x04argv\xda\x04path\xda\x06getcwdZ\x11current_directoryZ\nindex_file\xda\x05print\xda\x04exit\xda\x06exists\xda\x04join\xda\x04open\xda\x04read\xda\x05index\xda\x04seed\xa9\x00r\x13\x00\x00\x00r\x13\x00\x00\x00\xda\x07coduter\xda\x08<module>\x01\x00\x00\x00s*\x00\x00\x00\x10\x01\x0c\x02\n\x01\x08\x01\x04\x02\x08\x01\x08\x01\x08\x01\n\x01\x16\x01\x08\x01\n\x01\x0e\x01 \x01\x08\x01\x08\x01\x08\x01\x04\x01\x02\xff\n\x05\x08\x01")
        pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(v)
        with open('obf_path_unpacked.pyc', 'wb') as f:
            f.write(pyc_data) 
    #else:
     #   source_hash = importlib.util.source_hash(source_bytes)
      #  bytecode = importlib._bootstrap_external._code_to_hash_pyc(
       #     code,
        #    source_hash,
         #   (invalidation_mode == PycInvalidationMode.CHECKED_HASH),
#        )
    mode = importlib._bootstrap_external._calc_mode(file)
    importlib._bootstrap_external._write_atomic(cfile, bytecode, mode)
    return cfile


def main():
    import argparse

    description = 'A simple command-line interface for py_compile module.'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress error output',
    )
    parser.add_argument(
        'filenames',
        nargs='+',
        help='Files to compile',
    )
    args = parser.parse_args()
    if args.filenames == ['-']:
        filenames = [filename.rstrip('\n') for filename in sys.stdin.readlines()]
    else:
        filenames = args.filenames
    for filename in filenames:
        try:
            compile(filename, doraise=True)
        except PyCompileError as error:
            if args.quiet:
                parser.exit(1)
            else:
                parser.exit(1, error.msg)
        except OSError as error:
            if args.quiet:
                parser.exit(1)
            else:
                parser.exit(1, str(error))


if __name__ == "__main__":
    main()
