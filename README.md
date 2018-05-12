# Memristor Read/Write Analysis

This repo generates output for inverter circuit using FinFET models provided by PTM. This output is used for analysis of Read/Write behaviour with respect of various parameters. Monte Carlo simulation is executed on certain parameters to widen its input for vast analysis on output results.

## What does it do?

- Generate Read/Write output for inverter circuit

## Instructions

For single files

```bash
# Run single file
{path-to-exec} -Run -b read_write_01.cir

# Windows
> /mnt/c/Program Files/LTC/LTSpice/XVII.exe -Run -b read_write_01.cir

# OSX
$ /Applications/LTspice.app/Contents/MacOS/LTspice -Run -b read_write_01.cir
```

For all libs

```bash
$ python vth-variation.py
```

## Prequisites

```
$ pip install numpy
```

## Equations to plot

```
(V(x)-V(bl))/Ix(u1:2)
```