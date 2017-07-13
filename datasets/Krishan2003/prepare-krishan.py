from lingpy import *
from pystdb import load_stedt, stdb_concepts

concepts = stdb_concepts()

rong = csv2list('Darma.mapped.tsv', strip_lines=False)
wl = load_stedt('SK-TBLUP.csv')
rn2k = {wl[k, 'rn']: k for k in wl}

out = {0: ['language', 'concept', 'conceptid', 'concepticon_id', 'tbl_id',
    'gloss_in_source', 'rgen', 'tokens', 'ipa']}
idxx = 1
goods, visited = 0, []
for line in rong[1:]:
    if line[-2].strip():
        rn = line[-2].strip()
        print(rn)
        idx = rn2k[rn]
        entry = wl[idx, 'reflex']
        st = [
                ('N', 'ɳ'),
                ('D', 'ɖ'),
                ('T', 'ʈ'),
                ('R', 'ɽ'),
                ('5', '◌̺'.replace('◌', '')),
                (':', 'ː'),
                    ]
        for s, t in st:
            entry = entry.replace(s, t)
        entry = entry.split(',')[0]
        entry = entry.split('~')[0].strip()
        entry = entry.replace(' ', '_')

        if wl[idx, 'language'] == 'Darma':
            tokens = ipa2tokens(entry.replace(' ', '_'), semi_diacritics="shz",
                    merge_vowels=False)
            out[idxx] = ['Darma', line[1], line[0], line[2], line[3], wl[idx,
                'concept'], line[4], ' '.join(tokens), wl[idx, 'reflex']]
            idxx += 1

            c = wl[idx, 'concept']
            if c in visited:
                pass
            else:
                visited += [c]
                goods += 1
wl2 = Wordlist(out)
wl2.output('tsv', filename='darma', ignore='all', prettify=False)

print(goods, goods/250)
