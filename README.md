# plot-py4vasp
A re-capsuled version of [py4vasp](https://github.com/vasp-dev/py4vasp) for specific application 

## How to Use

One can install this by

```bash
git clone hhttps://github.com/russell-samuel/plot-py4vasp
```

then use this module simply via modifing `user_one.py` 
```bash
# adapting tasks to your needs
vim user_one.py   # using vim
code user_one.py  # using VS Code

# then run your pre-defined task
python user_one.py
```

> [!IMPORTANT]
> The code is implemented on `python 3.9.13`, `py4vas 0.4.0`. 
> 
> Because of the API changed, the newer versions of `py4vasp` (at least start from`0.7.3`) have already broke this code and may cause some unexpected behavior. 
> 
> The compatibility fix is in progress. 

## Math Formula Support

[Plotly](https://github.com/plotly/plotly.py) (`plotly.offline.plot`) support renderring $\LaTeX$ with [MathJax](https://github.com/mathjax/MathJax). 

You can install MathJax by clone MathJax project to the root directory (see details on the README of [MathJax Project](https://github.com/mathjax/MathJax)):

```bash
# go to root directory
cd path/to/this_project

# clone mathjax project 
git clone https://github.com/mathjax/MathJax
```

then you can invoke MathJax by:

```python
from vasp_h5 import Result
result = Result(path_to_h5file='path/to/vasp.h5', mathjax_path= './mj-tmp/es5/tex-svg.js')  
# using tex-svg.js in this example, you can change to a desired one
```
