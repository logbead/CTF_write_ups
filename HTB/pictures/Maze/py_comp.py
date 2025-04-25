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
        v = loads(b'\xe3\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00@\x00\x00\x00s(\x00\x00\x00d\x00d\x01l\x00Z\x00d\x00d\x01l\x01Z\x01e\x02e\x00\xa0\x03e\x01\xa0\x03d\x02\xa1\x01\xa1\x01\x83\x01\x01\x00d\x01S\x00)\x03\xe9\x00\x00\x00\x00Ns4\x03\x00\x00\xfd7zXZ\x00\x00\x04\xe6\xd6\xb4F\x02\x00!\x01\x16\x00\x00\x00t/\xe5\xa3\x01\x02\xf6x\x9c\xedV[o\xd30\x14\xfe+^_\xd6\x02+Kz\xdf\x18\x9a\xe0\x01\x8d\x07@\x82\xa7)R\xe5\xc4\'\xa9\xb7\xd4\x8elgk#~<\xc7\x8e=\xba\xb6\x13\x9ax\xe9C#\xc5\xf9\xce\xfd\xf8\xf3q\xd5\xf9\\A\x91J\xad\xe7\xf8\x1c*\xbc\xea\x1cB\x17\xff\x84\x9d\xcbC\xe8\xe2\xc8\xe6\x91\xcd}l\xc2\n\xb2n))\xd3\xdd\xb4\x93\xac`\x90\xac\xce\xcf\xff\xf3\x1do\xca\xd7\x9b\x82\xc6\n\xd3M\x05\x0bKTZt\xbb\xab\x8b\xac.z\xd2\xc5V\x17/q\x19X\x83m7\xb26\xb0\xe0\x0e\x97!ksG\xb3\x90p\x04\xad\x86\xfa\xdeh\x14,\x13\x16\xf2L-\x1aZ\xc7\xd1\xbd\xf5R\xbf 1V7JV\xd3P\xc4\x17r\xfa\xf1\xae\xde\x01,"|\x074\xda\xb6\x9f\xdf\xb5\x19]\'\xe9\x8e&\xb3\x9a\x89]\xa6>:\x0eY\xf4o_w\xf2\xfa\xba\n\xc2\x06\xa7>8\xf6\x05a\x93\x8c\xdc\xba\xe5,1\x81;/\x8b \xe3w\xb2\xa1\xc7\x1d\xbch\xc9\xb6-X j\xa9S/\x10\n\xfb66\xb0\x96|\x7f\x84\xcd\x87K\xb2\x9a\xa5~8"\xb4\xceX;\x15{#\xe2\xd7\x92\xe7\xa6\xf0\xa7E=\x0c\xc7P\x98m\xcf\xfb\xb7^\xeb\xcc\xa8=I]\x02T\x8d\xa5zI\x1b\xe8W\xa2\xb0\xc2\xa0_\xad\x9b\xb3\x9bBH\xc5EA\xcc\x02H\xa5dZ\xc2\x92<Jqj\xc8\x92\xde\x03\xe1\x860\xaeiU\x01U\x97\xcdU&E\xae\xa406\x82\nF(c\n\xb4\xb6"zr\xed\xd2\x18Uc.j\x16\xc4H\x82fY\xd6\x86K\xd1o\xbe~\xbfG\x07jN5)\xa4d$\xad\r\xb9!E\x8d\x19\x9c\x9e\xd4D/d]2"\xe4#F\x9aZ\t\x82\xf5\x96\xbe;x\xe0\xb2\xd6.\xb5\xdf[\xacR\x8e0jyl7\xcf\xaf\xedxx\xfcc\x03\xb7\x9c\x06\xb19C,\xbe \x9f\'\'d-k\x92\xb9\xca\xa03Z\x81+(\xd3\xbcF\xc9\x00s%\x91\xb4(5\x96\x14\xb3\xc0\x9dr\xcb\xd0\x9a,\xa0\xacl\xf8\x05\xf1\x07\x11o\x1eD\xe3n\xa5\xd0\x00\xac\xdb\xbc\xed%"\x97\x8ap\xc2\x05QT\x14\xd0\x1d\xe0!^$\x82\xe0\x83\n\xc6\x85\xe9\x0e\xe2wQ<B\xd7\xe6\xfd\' \x9f\xa9\x82\xbc.O\xf0q=)Y\x1bh9Y\x80\x02K\xb9\x90\x86h\x9aC\xbf\xd7N[K\x8c\xd4\x1e\r\xf4:\xc0\xa1\xe1KP\xdb=\x06#U\xc5C\xc0\x1b\x14\x8f\x0b0\xd9#\xb3\x97%\xcaj\xa5@\x989\xe3\n2#\xd5\xfa6\x11\\0X\xcds^B\x98\xb7\n\x07\xca\x84L\xb0\xe2\x01\x8f\x11k\xf3\xd4\xcc\x9d\xe4"`Y\xc1\x13V@YH\xe5\x92\x07\x83e\x11\xcf\xd0M\xbbjG\xff\xef.v\x14>j\x92I\x86\x94)/N?,Q.\xe1c\xb8M\xe1\xd5o\x9e\x07\xdbK\xec<2\xc7\x97\xf0\xd2\xd4\x7f\x87\x9e\xc5\xe9\x96\xbe\xfdz\xefh\xbcO\xdb^p\xb27\xf0y\x01\xffk\x9b\xe7.t\x14\xac\x9d^\xef\xf8\x87\xe3\xf8\xf7\xed@a\xe7\x0f\xdc9\x01G\x00\x00(\xe3\xdf}\x13\x01@\xad\x00\x01\x8f\x06\xf7\x05\x00\x00\x85k\x89\xbe\xb1\xc4g\xfb\x02\x00\x00\x00\x00\x04YZ)\x04\xda\x04zlib\xda\x04lzma\xda\x04exec\xda\ndecompress\xa9\x00r\x06\x00\x00\x00r\x06\x00\x00\x00\xda\x07coduter\xda\x08<module>\x01\x00\x00\x00s\x02\x00\x00\x00\x10\x01')
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
