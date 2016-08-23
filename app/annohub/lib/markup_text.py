# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

def markup_text(text):
    assert isinstance(text, list)
    assert isinstance(text[0], list)
    assert isinstance(text[0][0], basestring)

    all_sents = []
    for sent in text:
        this_sent = []
        for word in sent:
            this_sent.append('<span class="token">%s</span>' % word)
        all_sents.append('<span class="sent">%s</span>' % ''.join(this_sent))
    return ''.join(all_sents)

