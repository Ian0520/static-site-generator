
import os
import shutil


def copy_static(src: str, dest: str) -> None:
    if not os.path.exists(src):
        raise RuntimeError("the static source does not exist")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    
    for path in os.listdir(src):
        old = os.path.join(src, path)
        new = os.path.join(dest, path)
        if os.path.isfile(old):
            shutil.copy(old, dest)
        else:
            copy_static(old, new)

