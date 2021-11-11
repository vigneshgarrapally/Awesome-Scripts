import filetype

def main(path):
    kind = filetype.guess(path)
    if kind is None:
        print('Cannot guess file type!')
        return
    typ=kind.mime
    ans=typ.find("video")
    print(typ)
    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)

if __name__ == '__main__':
    main(input())
