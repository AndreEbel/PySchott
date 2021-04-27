# PySchott
Python wrapper for serial communication with Schott microscopy light source (MC-LS)

To be used with light sources from [Schott](https://www.us.schott.com/lightingimaging)

Tested on:
- MC-LS

## Basic usage
```
import PySchott
light = PySchott.MCLS_Light()
light.set_on()
light.set_intensity(0.5)
light.set_off()
```

## Installation 

This package can be installed locally with PIP after downloading the files
