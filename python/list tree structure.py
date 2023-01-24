#Replace with Seedir
#https://stackoverflow.com/a/49912639
#DisplayablePath.make_tree(Path('doc'), criteria=lambda path: True if path.name not in ('.git',  '__pycache__') else False))
from pathlib import Path
import argparse
class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path
                               for path in root.iterdir()
                               if criteria(path)),
                          key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path):
        #Ignores .git and __pycache__
        ignorelist=['.git', '__pycache__']
        return True if path.name not in ignorelist else False



    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))
myparser=argparse.ArgumentParser()
myparser.add_argument('dir',help="directory to which tree structure is displayed")
myparser.add_argument("-f","--file",help="file to which tree structure is displayed")
myparser.add_argument("-p","--print",action='store_true',help="whether to print to console or not")
args=myparser.parse_args()
input_path=Path(args.dir)
if not input_path.is_dir():
    raise Exception("Given path is not a directory")
paths = DisplayablePath.make_tree(Path(input_path))
flag=True
if args.print:
    flag=False
    for path in paths:
        print(path.displayable())
if args.file:
    flag=False
    output_path=Path(args.file)
    with open(output_path,"w",encoding="utf-8") as f:
        for path in paths:
            f.write(str(path.displayable())+"\n")
if flag:
    print("Mention whether to print or save to a text file.\n Exiciting")