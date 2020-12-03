# ds1052e

A Python interface for controlling and collecting data from the Rigol DS1052E oscilloscope.

## Usage

First, initialize a `DS1052E` object:

```python
from ds1052e import DS1052E
scope = DS1052E()
```

Then, to collect data, we must temporarily stop continuous sampling. This can be done with the `.stop()` method:

```python
scope.stop()
```

Now that we've paused sampling, we have a short segment of data from right when we stopped the oscilloscope. We can retrieve this data with the `.sample()` method, passing to it a channel name:

```python
time, voltage = scope.sample("CHAN1")
```

Or, to sample channel 1, we may also omit a channel name:

```python
time, voltage = scope.sample()
```

Valid channel names are `"CHAN1"`, `"CHAN2"`, and `"MATH"`. In order for one of these channels to be sampled, it must be activated on the oscilloscope. The raw channels can be activated and deactivated with the `CH1` and `CH2` buttons; the math channel may be activated and deactivated by the `MATH` button.

Then, to resume sampling, we simply use the `.resume()` method:

```python
scope.resume()
```

## Notes

The time axis is measured in seconds, and the voltage axis is measured in volts, regardless of the scale chosen on the oscilloscope.

# Credits

My code is heavily based on Ken Shiriff's
[code](http://righto.com/rigol) which was in turn based on
[code](https://www.cibomahto.com/2010/04/controlling-a-rigol-oscilloscope-using-linux-and-python/)
by Cibo Mahto.
