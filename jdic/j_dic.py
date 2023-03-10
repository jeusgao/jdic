#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Joe Gao (jeusgao@163.com)

import os, numpy as np, time, json
import mmap
from tqdm import tqdm

@np.vectorize
def dic_lookup(d, k):
    return d.get(k)

class JDic(object):
    def __init__(self, name=None, path=None):
        self.keys = None
        self.values = None
        if name:
            fp = os.path.join(path, name) if path else name
            if any([not os.path.exists(f'{fp}_keys.dat'), not os.path.exists(f'{fp}_values.dat')]):
                raise FileNotFoundError(f'{fp}_*.dat')
            self.keys = np.load(f'{fp}_keys.dat', allow_pickle=True).tolist()
            self.values = np.load(f'{fp}_values.dat', allow_pickle=True)

    def buildDic(self, keys, values, name, path=None):
        if not keys: return False
        fp = os.path.join(path, name) if path else name
        self.keys = {k:i for i, k in tqdm(enumerate(keys))}
        self.values = np.array([_x.encode('utf-8') for _x in tqdm(values)])
        np.save(f'{fp}_keys.dat', self.keys)
        np.save(f'{fp}_values.dat', self.values)
        os.rename(f'{fp}_keys.dat.npy', f'{fp}_keys.dat')
        os.rename(f'{fp}_values.dat.npy', f'{fp}_values.dat')
        return True

    def get(self, keys):
        if not keys: return None
        if not isinstance(keys, list): keys = [keys]

        _keys = np.array(keys)
        _idxs_all = dic_lookup(self.keys, keys)
        _idxs_values = list(filter(None, _idxs_all))

        idxs_in = np.where(_idxs_all!=None)
        _keys_in = _keys[idxs_in]
        idxs_oov = np.where(_idxs_all==None)
        _oov = _keys[idxs_oov]

        _values = [json.loads(_x.decode('utf-8')) for _x in self.values[_idxs_values]]
        _new_idx = {**dict(zip(_oov, [None]*len(_oov)), **dict(zip(_keys_in, _values)))}

        return {'keys_oov': _oov, 'keys_in': _keys_in, 'all': _new_idx}
