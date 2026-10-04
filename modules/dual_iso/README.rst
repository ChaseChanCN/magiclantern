
Dual ISO
========

:Author: a1ex
:License: GPL
:Summary: 双ISO
:Forum: http://www.magiclantern.fm/forum/index.php?topic=7139.0

Quick start
-----------

* Start at ISO 100 in Canon menu
* Expose to the right by changing shutter and aperture
* If the image is still dark, enable dual ISO
* Adjust alternate ISO: higher values = cleaner shadows, but more artifacts
* Try not to go past ISO 1600; you will not see any major improvements, 
  but you will get more interpolation artifacts and hot pixels.

Tips and tricks
---------------

* Do not use dual ISO for regular scenes that don't require a very high dynamic range.
* Raw zebras are aware of dual ISO: weak zebras are displayed where only the high ISO is overexposed,
  strong (solid) zebras are displayed where both ISOs are overexposed.
* Raw histogram will display only the low-ISO half of the image (since the high-ISO data is used
  for cleaning up shadow noise).
* For optimal exposure (minimal noise without clipped highlights), try both dual ISO and ETTR.
* Do not be afraid of less aggressive settings like 100/400. They are almost as good as 100/1600 
  regarding shadow noise, but with much less aliasing artifacts.
* Be careful with long exposures, you may get lots of hot pixels.

