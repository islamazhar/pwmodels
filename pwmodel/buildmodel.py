from collections import defaultdict
import helper
import dawg

import models

MIN_FREQ = 0.5

def create_model(modelfunc, fname='', listw=[], outfname=''):
    """:modelfunc: is a function that takes a word and returns its
    splits.  for ngram model this function returns all the ngrams of a
    word, for PCFG it will return te split of the password. So, it
    takes a string and returns a list of strings

    """
    pws = []
    if fname:
        pws = helper.open_get_line(fname)
    def join_iterators(_pws, listw):
        for p in _pws: yield p
        for p in listw: yield p
    big_dict = defaultdict(int)
    for pw, c in join_iterators(pws, listw):
        for ng in modelfunc(pw):
            big_dict[unicode(ng)] += c
    big_dict['__TOTAL__'] = sum(big_dict.values())
    nDawg= dawg.IntCompletionDAWG(big_dict)
    if not outfname:
        outfname = 'tmpmodel.dawg'
    nDawg.save(outfname)
    return nDawg

def prob(nDawg, w, modelfunc):
    t = float(nDawg.get('__TOTAL__'))
    print '\n'.join("{} -> {}".format(ng, nDawg.get(ng, MIN_FREQ))
                       for ng in modelfunc(w))

    return helper.prod(nDawg.get(ng, MIN_FREQ)/t
                       for ng in modelfunc(w))


def read_dawg(fname):
    nDawg= dawg.IntCompletionDAWG(fname)
    nDawg.load(fname)
    return nDawg

def create_ngram_model(fname='', listw=[], outfname='', n=3):

    return create_model(fname=fame, listw=listw, outfname=outfname,
                        modelfunc=lambda w: models.ngramsofw(w, n=3))

if __name__ == "__main__":
    import sys
    w = 'password@123'
    T = create_model(fname=sys.argv[1], listw=[], outfname='',
                 modelfunc=models.pcfgtokensofw)
    print prob(T, w, modelfunc=models.pcfgtokensofw)

