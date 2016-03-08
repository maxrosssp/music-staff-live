================
music-staff-live
================

Overview
========

music-staff-live works with a real life model of a two-measure music staff, like the one seen `here <http://imgur.com/I9dHWCS>`_, and is able to dynamically play notes (including chords) that a user places on the staff in person.

This software requires a webcam to be constantly be watching the staff. It will recognize when a user is done rearranging notes, and only then will it attempt to analyze and play aloud the given melody.


Use
===

To use this software, make sure you have OpenCV installed as well as the other dependencies listed in requirements.txt. Then just import the module to your project, create an mslive = msl.core.MSLive() object, and then run mslive.start().
If you want to calibrate certain variables that will make it run much better, call mslive.start(calibrate=True).