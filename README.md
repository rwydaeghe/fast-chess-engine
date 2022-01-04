# Chess engine

I was bored during Christmas holidays, so I wrote a basic Chess engine. It supports mini-max, printing the board, eval function depending on position, the basic chess moves and a smart eval function that updates based on previous results.
Currently, reasonable depths are 3 to 4. I could use alpha-beta pruning for the algorithm to achieve a speed increase, but instead saw this as an opportunity to learn tools to speed up Python:
- Cython
- PyPy
- Numba
- Caching

All these are tested to some extent, with honestly not too great resutls. But now I know how they work and when they work. 
If you want to use the repo, it is quite large because I have added the venv to it, as I am teaching myself that too instead of the usual conda way (using PyCharm now).

