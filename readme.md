
# About
- ## quick load and less mem
Load data quickly in less mem cache(2GB size matrix load in 0.5s~1.2s, 400MB mem only.)
<br>
[test in: mac i5-4core-2.3GHZ/8g]

<br>

- ## speed-up search effi:
  * get values: 5000/s
  * in-dic only: 500000/s

<br>

# Install
python >= 3.7

```bash
# setup with setuptools to get a wheel first.
pip3 install your_wheels_path/jdic-0.0.1-py3-none-any.whl
```

<br>

# Import

```python
from jdic.j_dic_mm import JmmDic
jDic = JmmDic(name=None, path=None)
'''
  Args:
    name ([str]): [name of dic] (default: `None`)
    path ([str]): [path of dic map file] (default: `None`)
    Raises:
    FileNotFoundError: [keys or values mmapfile not exists, cannot build a JDic]
'''
```

<br>

# Dict.build
`JmmDic.buildDic(keys, values, name, path=None)`
* cac and gen shape inside, do not worry about the shape of matrix.

```python
'''
  Args:
    keys ([str]): [List of keys]
    values ([object]): [List of values]
    name ([str]): [name of the dict]
    path ([str]): [path to save] (default: `None`)
  Returns:
    bool: [action result]
'''
with open('data/keys.txt', 'r') as fk, open('data/values.txt', 'r') as fv:
    keys = fk.read().splitlines()
    values = fv.read().splitlines()
jDic = JmmDic()
jDic.buildDic(keys, values, 'test_jdic_1', path='data')

'''
after Build dict, dat files created in the specific path.
{path}
    |_ {name}_values.dat
    |_ {name}_keys.dat
    |_ {name}_do_not_del_me.dat
'''
```

<br>

# Dict.get
`JmmDic.get(keys, is_get_vals=False)`

```python
'''
  Args:
    keys ([str]): [keys list to search]
    is_get_vals(bool): [if need to get index in values] (default: `True`)
  Returns:
    dict: [keys_oov(list), keys_in(list), all(dict(key:value))]
'''
# Load a JmmDic
jDic = JmmDic('test_jdic_1', path='data')

# search keys
_keys = ['美丽__城市', '测试__测试', '龚琳娜__起来']

# get in-dict or not only, "is_get_vals=False"
r = jDic.get(_keys, is_get_vals=False)

# get both in-dict or not and in-dict values, "is_get_vals=True"
r = jDic.get(_keys, is_get_vals=True)

keys_oov = r.get('keys_oov')  # list
keys_in = r.get('keys_in')    # list
values_all = r.get('all')   # dict

print(keys_oov)
print(keys_in)
print(values_all)
```

<br>

# Dict.add
`JmmDic.add(keys, values)`

```python
'''
  Args:
    keys ([str]): [List of keys]
    values ([object]): [List of values]
  Returns:
    bool: [action result]
'''
# Load a JmmDic
jDic = JmmDic('test_jdic_1', path='data')

# search keys
_keys = ['test1', 'test2', 'test3', '测试4']
_values = ['value1', 'value2', 'test3_values_测试三', 'test4_values_测试四']
jDic.add(_keys, _values)

```
