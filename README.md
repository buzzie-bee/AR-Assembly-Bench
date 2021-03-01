AR Assembly Bench Demo

Created using python, kivy, pyserial

Proof of concept demo showing how  we can use a Keyence CV-X / XG-X vision
system to identify the location of parts  on an assembly bench and 
project the location of the part and assembly instructions as an overlay
ontop of the component.

Much of the code in here is hardcoded calibration (i.e. the scaling
function takes the mm length of the scaling line as a hardcoded variable rather
than being part of a 'settings' page) and is not intended for general use or 
distribution.

If this project had progressed I would probably rewrite it using a different gui library.
