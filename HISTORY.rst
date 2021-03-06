=======
History
=======

0.1.0 (2017-07-01)
------------------

* First release on PyPI.

0.7.0 (2017-07-28)
------------------

* Implement :code:`VersionedSerializer`
* Implement :code:`view_config`
* Make the library an installable Django app

0.8.0 (2017-07-28)
------------------

* Some minor fixes to make sure it works on generic project
* Add examples

0.8.1 (2017-07-28)
------------------

* Fix bug when parsing empty docstring of the serializer

0.9.0 (2017-07-28)
------------------

* Rename base :code:`VersionedSerializer` into :code:`VersionedSerializers`

0.9.1 (2017-07-28)
------------------

* Fix import issue after renaming

0.9.3 (2017-08-05)
------------------

* Add support for different response status codes (`Issue 27 <https://github.com/limdauto/drf_openapi/issues/27>`_)

0.9.5 (2017-08-12)
------------------

* Add Python 2.7 compatibility (thanks `tuffnatty <https://github.com/limdauto/drf_openapi/pull/35>`_)
* Add support for ModelViewSet (thanks `tuffnatty <https://github.com/limdauto/drf_openapi/pull/36>`_)

0.9.6 (2017-08-12)
------------------

* Fix type display for child of ListSerializer/ListField (`Issue 28 <https://github.com/limdauto/drf_openapi/issues/28>`_)

0.9.7 (2017-09-12)
------------------

* Improve permission for schema view (`Issue 31 <https://github.com/limdauto/drf_openapi/issues/31>`_)
