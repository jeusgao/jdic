#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Joe Gao (jeusgao@163.com)

import os, numpy as np, time, json
import mmap
from tqdm import tqdm

@np.vectorize
def dic_lookup(d, k):
    return d.get(k)

class JmmDic(object):
    def __init__(self, name=None, path=None):
        '''[dict by matrix]
        Args:
            name ([str]): [name of dic] (default: `None`)
            path ([str]): [path of dic map file] (default: `None`)
        Raises:
            FileNotFoundError: [keys or values mmapfile not exists, cannot build a JDic]
        '''
        self.keys = None
        self.values = None
        self.fp = None
        self.shape = None
        if name:
            self.fp = os.path.join(path, name) if path else name
            self.load()

    def load(self):
        if self.fp:
            if any([not os.path.exists(f'{self.fp}_keys.dat'), not os.path.exists(f'{self.fp}_values.dat')]):
                raise FileNotFoundError(f'{self.fp}_*.dat')

            with open(f'{self.fp}_do_not_del_me.dat', 'r') as f:
                self.shape = tuple([int(l) for l in f.read().splitlines()])
            self.keys = np.load(f'{self.fp}_keys.dat', allow_pickle=True).tolist()
            self.values = np.memmap(f'{self.fp}_values.dat', dtype='int', mode='r+', shape=self.shape)

    def buildDic(self, keys, values, name, path=None):
        '''[summary]
        [description]
        Args:
            keys ([List[str]]): [description]
            values ([List[object]]): [description]
            name ([str]): [name of the dict]
            path ([str]): [path to save] (default: `None`)
        Returns:
            bool: [action result]
        '''
        maxlen = max([len(v) for v in values])
        maxlen = int(maxlen *1.5)
        if not keys: return False
        self.fp = os.path.join(path, name) if path else name
        keys = {k:i for i, k in tqdm(enumerate(keys))}

        _tmp = [[ord(_x) for _x in v] + [-1]*(maxlen-len(v)) for v in tqdm(values)]
        values = np.array(_tmp)
        np.save(f'{self.fp}_keys', keys)
        np.save(f'{self.fp}_values', values)
        with open(f'{self.fp}_do_not_del_me.dat', 'w') as f:
            f.write(f'{len(keys)}\n{maxlen}')
        os.rename(f'{self.fp}_keys.npy', f'{self.fp}_keys.dat')
        os.rename(f'{self.fp}_values.npy', f'{self.fp}_values.dat')

        self.load()

        return True

    def get(self, keys, is_get_vals=False):
        '''[summary]
        [description]
        Args:
            keys ([List[str]]): [keys list to search]
            is_get_vals(bool): [if need to get index in values] (default: `True`)
        Returns:
            dict: [keys_oov, keys_in, all keys' value]
        '''
        if not keys: return None
        if not isinstance(keys, list): keys = [keys]
        _keys = np.array(keys)

        _idxs_all = dic_lookup(self.keys, keys)
        _idxs_values = list(filter(None, _idxs_all))

        _keys_in = _keys[np.where(_idxs_all!=None)]
        _oov = _keys[np.where(_idxs_all==None)]

        _new_idx = {}

        if is_get_vals:
            _lambda = lambda x: ''.join([chr(_x) for _x in list(filter(lambda x: x not in [-1, 0, 10, 32], x))])
            _values = [_lambda(_x) for _x in self.values[_idxs_values]]

            _new_idx = {**dict(zip(_oov, [None]*len(_oov)), **dict(zip(_keys_in, _values)))}

        return {'keys_oov': _oov.tolist(), 'keys_in': _keys_in.tolist(), 'all': _new_idx}

    def add(self, keys, values):
        '''[summary]
        [Keep each value length < shape[-1]]
        Args:
            keys ([List[str]]): [description]
            values ([List[object]]): [description]

        Returns:
            bool: [action result]
        '''
        if any([not self.fp, not keys, not values]): return False

        _len_k, _len_v = len(keys), len(values)
        if _len_k != _len_v: return False

        if not isinstance(keys, list): keys = [keys]
        if not isinstance(values, list): values = [values]

        _start, _maxlen = self.shape

        _tmp = {k:i+_start for i, k in tqdm(enumerate(keys))}
        self.keys = {**self.keys, **_tmp}
        np.save(f'{self.fp}_keys', self.keys)
        os.rename(f'{self.fp}_keys.npy', f'{self.fp}_keys.dat')

        _tmp = [[ord(_x) for _x in v[:_maxlen]] + [-1]*(_maxlen-len(v[:_maxlen])) for v in tqdm(values)]
        self.values = np.row_stack((self.values, np.array(_tmp)))
        np.save(f'{self.fp}_values', self.values)
        os.rename(f'{self.fp}_values.npy', f'{self.fp}_values.dat')

        with open(f'{self.fp}_do_not_del_me.dat', 'w') as f:
            f.write(f'{_start+_len_v}\n{_maxlen}')

        del _tmp

        self.load()
        return True






