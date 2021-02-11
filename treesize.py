import os, re, csv
path = '/Volumes/lpasync/9_not_MIable/Staged_BornDigital_Excel/2013_224_silversodfy1311/data'
def subdirs(path):
    """Yield directory names not starting with '.' under given path."""
    for entry in os.scandir(path):
        if not entry.name.startswith('.') and entry.is_dir():
            yield entry.name
            print (entry.name)
def get_tree_size(path):
    """Return total size of files in path and subdirs. If
    is_dir() or stat() fails, print an error message to stderr
    and assume zero size (for example, file has been deleted).
    """
    total = 0
    for entry in os.scandir(path):
        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError as error:
            print('Error calling is_dir():', error, file=sys.stderr)
            continue
        if is_dir:
            total += get_tree_size(entry.path)
            #print(entry, get_tree_size(entry.path))
        else:
            try:
                total += entry.stat(follow_symlinks=False).st_size
            except OSError as error:
                print('Error calling stat():', error, file=sys.stderr)
    return total
bag = open('/Volumes/lpasync/9_not_MIable/Staged_BornDigital_Excel/2013_224_silversodfy1311/bag-info.txt', 'r')
def payload(path):
    for line in bag:
        if re.match('Payload-Oxum', line):
            return line
parent = os.path.dirname(path) 
dirname=os.path.split(parent)[1]
with open('acc.csv', 'w', newline='') as csvfile:
    fieldnames = ['collection', 'bytes', 'tree']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'collection': dirname, 'bytes': payload(path), 'tree': get_tree_size(path)})




