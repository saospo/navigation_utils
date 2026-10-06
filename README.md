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

In the age of "AI", I imagine that a reader may be asking themselves "Why? Surely an LLM could do this all, and better!". They're probably right, but there are still a few reasons. 

First, as they say in Full Metal Jacket: there are many like it, but this one is mine. I have libraries downstream of this one, which I'm using to build further projects. There's more coming... and this is exactly what I need to do it. 

Second, though, I derived every formula in this library. I know exactly what each function does, why it does that, where it came from, and why I need it. I think it was worthwhile to do the work to produce this product, and experience *why* you need good error handling, and what a robust architecture for a library like this looks like. What functions do you need? Where do they fail? What is an intelligent way to organize yourself and what you're doing?

Third, criticism of "should have used an LLM" isn't quite accurate: I did. Liberally... BUT, I used it as a second reviewer and a verifier rather than a developer. I wanted to see if I could use the machine to help me build up a deep and intuitive understanding that was mine alone. And... I think I succeeded. There are still hurdles to cross (I'm still not quite ironclad on how to work with a unit vector and how to use that to identify a great circle based on two arbitrary points on its line... thanks, Aviation Formulary!) but everything else here was my idea, and/or my keystrokes. Sometimes, the machine did well, but I think I did better. Certainly, it was a solid editor and rubber duck to spitball with.

Finally, the machine couldn't do this. It got the math wrong, routinely, and in devastating ways. I found myself reviewing and correcting output for almost every function in here. This is a tricky, concept-heavy field that is deeply rewarding but one which is tough to move in without building up your own knowledge.

So, in short: LLMs couldn't do exactly what I did, at least in my experience. Now I've made something that I am now using in turn, and I know a lot about why all that works. I know how I like to consort with the Robot Gods, and I learned a lot either way. That's why I did this.