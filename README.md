Simple library for handling spherical trigonometry math, primarily denominated in degrees (so watch those floats!).

Various functionality enclosed. Major groupings:

- a class DMS (degrees, minutes, seconds) which handles data in that format.
- various simple wrappers on math functions which allow easy use of degree-based values as opposed to radian values. (and alternate versions of some of the above which allow mathematically valid but less human-digestible values to be converted to relevant values: think compass headings, or longitude.)
- functions designed to help complete the problem set found on the Stonybrook spherical trig page (https://www.math.stonybrook.edu/~tony/archive/336f06/spher-trig.html)
- functions for parsing string-based inputs in DMS and decimal degree formats.
- a suite of functions using the spherical laws of sine and cosine to allow for calculation of various latitudes, longitudes, central angle distances, and heading values from different pieces of that information
- further functions based on compositions and derivations of the above which allow users to calculate key data points about a great circle route
- functions built to automate unit tests for certain parts of the library

Also included are a variety of test suites yours truly used when writing this library.

Sources:

I primarily used the following two pages. I developed my intuition by grinding against that Stonybrook page for a day. Some of the more advanced identities (Clairaut's, vector-based circle identification) come from Aviation Formulary. It's a great resource.

Aviation Formulary: https://edwilliams.org/avform147.htm
Stonybrook spherical trig: https://www.math.stonybrook.edu/~tony/archive/336f06/spher-trig.html

I have also used these for reference.

Wikipedia on spherical trig: https://en.wikipedia.org/wiki/Spherical_trigonometry
Wikipedia on great circles: https://en.wikipedia.org/wiki/Great-circle_navigation
