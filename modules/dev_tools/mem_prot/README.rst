Memory Protection
=================

内存访问保护测试
protect the first 4KiB so that NULL pointer accesses will get caught.
As Canon's own code often causes NULL pointers to be dereferenced, 
this will happen quite often - especially in LV mode.

:License: GPL
:Summary: 内存保护
:Authors: g3gg0
