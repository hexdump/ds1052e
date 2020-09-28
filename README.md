# ds1052e

A programatic python interface for controlling and collecting data
from the Rigol DS1052E oscilloscope.

# Usage

First, initialize a `DS1052E` object:

```
from ds1052e import DS1052E

scope = DS1052E()
```

Then, to sample data from a channel (the default of `CHAN1`, or
`CHAN2` or `MATH`), use `.sample()`:

```
time, data = scope.sample()
```

# Credits

My code is heavily based on Ken Shiriff's
[code](http://righto.com/rigol) which was in turn based on
[code](https://www.cibomahto.com/2010/04/controlling-a-rigol-oscilloscope-using-linux-and-python/)
by Cibo Mahto.
