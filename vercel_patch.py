import builtins
import os

# 1. Patch open() to prevent Read-Only crashes on Vercel
original_open = builtins.open
def safe_open(file, mode='r', *args, **kwargs):
    if isinstance(mode, str) and ('w' in mode or 'a' in mode or '+' in mode):
        try:
            return original_open(file, mode, *args, **kwargs)
        except OSError:
            import io
            if 'b' in mode:
                return io.BytesIO()
            else:
                return io.StringIO()
    return original_open(file, mode, *args, **kwargs)
builtins.open = safe_open

# 2. Patch os.makedirs
original_makedirs = os.makedirs
def safe_makedirs(*args, **kwargs):
    try:
        original_makedirs(*args, **kwargs)
    except OSError:
        pass
os.makedirs = safe_makedirs
