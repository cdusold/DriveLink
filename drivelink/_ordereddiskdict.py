from collections import MutableMapping
try:
    import cPickle as pickle
except:
    import pickle
from os.path import expanduser, join
from os import remove, makedirs
from glob import glob
import atexit


class _page(dict):
    pass


class OrderedDict(MutableMapping):
    """
    A dictionary class that maintains O(1) look up and write while keeping RAM usage O(1) as well.

    This is accomplished through a rudimentary (for now) hashing scheme to page the
    dictionary into parts.
    """

    def __init__(self, file_basename, size_limit=1024, max_pages=16, file_location=join(expanduser("~"), ".DriveLink")):
        if max_pages < 1:
            raise ValueError("There must be allowed at least one page in RAM.")
        self.max_pages = max_pages
        if size_limit < 1:
            raise ValueError("There must be allowed at least one item per page.")
        self.size_limit = size_limit
        if file_location:
            try:
                makedirs(file_location)
            except OSError as e:
                if e.errno != 17:
                    raise
                pass
        self._file_base = join(file_location, file_basename)
        self._file_loc = file_location
        self._file_basename = file_basename
        self.pages = _page()
        self._length = 0
        self._total = set()
        self._queue = []
        # Just in case, cache pickle.
        self._pickle = pickle
        try:
            with open(self._file_base + 'Len', 'rb') as f:
                self._length = self._pickle.load(f)
            for f in glob(self._file_base + '*'):
                try:
                    self._total.add(int(f[len(self._file_base):]))
                except ValueError:
                    pass
        except IOError:
            pass
        atexit.register(OrderedDict.close, self)

    def _guarantee_page(self, k):
        """
        Pulls up the page in question.
        """
        if k not in self.pages:
            try:
                if k in self._total:
                    self._load_page_from_disk(k)
            except:
                pass
            if k not in self.pages:
                self.pages[k] = _page()
                self._total.add(k)
                self._queue.append(k)
        while len(self._queue) > self.max_pages:
            if self._queue[0] == k:
                self._queue.append(self._queue[0])
                del self._queue[0]
            self._save_page_to_disk(self._queue[0])

    def _branchpage(self, pagenumber):
        pass

    def _finditem(self, key):
        """
        Pulls up the page containing the key in question.

        Most frequently O(1), when a page becomes too large, there's
        a O(ln(n)) search that refactors O(k ln(n)) elements
        once every O(k) insertions. A full refactor usually
        happens in strides, moving a total of O(n) elements
        split up over O(ln(n)) calls. This makes the worst
        time refactor O(n) and usual refactor approximately
        O(n/ ln(n)). Average case lookup O(n/k).
        """
        # TODO: Refactor into b-tree
        k = hash(key) // self.size_limit
        self._guarantee_page(k)
        return k, key

    def _iterpages(self):
        """
        Pulls up page after page and cycles through all of them.
        """
        for k in list(self._total):
            self._guarantee_page(k)
            yield self.pages[k]

    def __delitem__(self, key):
        '''
         Deletes the key value in question from the pages.
        '''
        i, k = self._finditem(key)
        del self.pages[i][k]
        self._length -= 1

    def __getitem__(self, key):
        '''
         Retrieves the value the key maps to.
        '''
        i, k = self._finditem(key)
        return self.pages[i][k]

    def __iter__(self):
        '''
         Iterates through all the keys stored.
        '''
        for p in self._iterpages():
            for i in p:
                yield i

    def __len__(self):
        '''
         Returns the number of key value pairs stored.
        '''
        return self._length

    def __setitem__(self, key, value):
        '''
         Sets a value that a key maps to.
        '''
        i, k = self._finditem(key)
        if k not in self.pages[i]:
            self._length += 1
        self.pages[i][k] = value

    def close(self):
        '''
        Save all the values to disk before closing.
        '''
        if (self is None or not hasattr(self, "_save_page_to_disk")
                or not hasattr(self, "_file_base") or self._file_base is None):
            return
        while len(self.pages) > 0:
            for key in set(self.pages.keys()):
                self._save_page_to_disk(key)

    def _save_page_to_disk(self, number):
        with open(self._file_base + 'Len', 'wb') as f:
            self._pickle.dump(self._length, f)
        if self._file_base:
            if number in self.pages:
                if len(self.pages[number]) > 0:
                    with open(self._file_base + str(number), 'wb') as f:
                        self._pickle.dump(self.pages[number], f)
                else:
                    self._total.remove(number)
                del self.pages[number]
            for i in range(len(self._queue)):
                if self._queue[i] == number:
                    del self._queue[i]
                    break

    def _load_page_from_disk(self, number):
        if self._file_base:
            with open(self._file_base + str(number), 'rb') as f:
                self.pages[number] = self._pickle.load(f)
            self._queue.append(number)
            remove(self._file_base + str(number))

    def __str__(self):
        return "Dictionary with values stored to " + self._file_base

    def __repr__(self):
        return "OrderedDict(" + self._file_basename + "', " + str(self.size_limit) + ', ' + str(self.max_pages) + ", '" + self._file_loc + "')"

    def __contains__(self, item):
        i, k = self._finditem(item)
        return k in self.pages[i]

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        self.close()
