import os

from .context import pwmodel as pwm

leak_file = os.path.join(pwm.helper.thisdir, 'data', 'phpbb-withcount.txt.gz')


class TestNgramPw(object):
    def test_ngrampw(self):
        ngpw = pwm.NGramPw(n=4, pwfilename=leak_file, freshall=True)
        for (pw1, pw2) in [('password12', 'assword12'),
                           ('1234567', '12345679'),
                           ('password', 'pasword')]:
            assert ngpw.prob(pw1) > ngpw.prob(pw2)

    def test_ngrampw_generate_in_order(self):
        ngpw = pwm.NGramPw(n=4, pwfilename=leak_file)
        for pw, p in ngpw.generate_pws_in_order(1000):
            assert abs(p - ngpw.prob(pw)) <= 1e-3

# PCFG probabilties are wrong -- TODO - will fix it later
class TestModel(object):
    def test_model_prob(self):
        pcfgpw = pwm.PcfgPw(leak_file)
        w = 'password12'
        assert pcfgpw.prob(w) > pcfgpw.prob(w[1:])


class TestHistPw(object):
    def test_ordering(self):
        pws = [l for i, l in enumerate(pwm.helper.open_get_line(leak_file)) if i < 1000]
        hm = pwm.HistPw(leak_file)
        for i, l in enumerate(hm.iterpasswords()):
            if i >= 1000: break
            assert pws[i] == l


def test_qth_pw():
    hm = pwm.HistPw(leak_file)
    L = [hm.qth_pw(q)
         for q in range(100, 120, 1)]
    print(L)
    assert all(x[1] >= y[1] for x, y in zip(L, L[1:]))


def test_cmp_ngram():
    """
    Test three models and order them
    """
    models = [pwm.NGramPw(leak_file, n=3),
              pwm.NGramPw(leak_file, n=4),
              pwm.NGramPw(leak_file, n=5),
              pwm.PcfgPw(leak_file),
              pwm.HistPw(leak_file)]
    pwlist = ["123456", "12345", "123456789", "password", "iloveyou", "princess",
              "1234567", "rockyou", "12345678", "abc123", "nicole", "daniel",
              "babygirl", "monkey", "lovely", "jessica", "654321", "michael",
              "ashley", "qwerty", "111111", "iloveu", "000000", "michelle",
              "tigger", "sunshine", "chocolate", "password1", "soccer", "anthony",
              "friends", "butterfly", "purple", "angel", "jordan", "liverpool",
              "justin"]

    pwlist = [sorted(pwlist, key=m.prob, reverse=True)
              for m in models]
    # for i in xrange(0, len(pwlist), g):
    #     assert set(pwlist3[i:i+g])==set(pwlist4[i:i+g])==set(pwlist5[i:i+g])
    print(',\t\t'.join(m.modelname for m in models))
    for pws in zip(*pwlist):
        print(',\t\t'.join(pws))
