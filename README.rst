papis-pyffx
=====

pyffx is a pure Python implementation of *Format-preserving, Feistel-based encryption* (FFX).

Implemented standard FF1 according to
https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-38g.pdf

Tested with FF1 test vectors
https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/FF1samples.pdf

Usage
-----

.. code-block:: python

>>> import papis_pyffx.ff1_aes import FF1_AES
>>> key1 = bytes.fromhex('2B7E151628AED2A6ABF7158809CF4F3C')
>>> clear1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> tweak1 = list(bytes.fromhex('39383736353433323130'))
>>> chiffer1No = [2, 4, 3, 3, 4, 7, 7, 4, 8, 4]
>>> cipher = FF1_AES(self.key1, 10)
>>> cipher.encrypt(self.clear1) == self.chiffer1No
True
>>> cipher.decrypt(self.chiffer1No) == self.clear1
True

>>> import papis_pyffx.

Old_functions_not_used_anymore
    >>> import pyffx
    >>> e = pyffx.Integer(b'secret-key', length=4)
    >>> e.encrypt(1234)
    6103
    >>> e.decrypt(6103)
    1234
    >>> e = pyffx.String(b'secret-key', alphabet='abc', length=6)
    >>> e.encrypt('aaabbb')
    'acbacc'
    >>> e.decrypt('acbacc')
    'aaabbb'

.. _The FFX Mode of Operation for Format-Preserving Encryption: http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/ffx/ffx-spec.pdf
.. _Addendum to “The FFX Mode of Operation for Format-Preserving Encryption”: http://csrc.nist.gov/groups/ST/toolkit/BCM/documents/proposedmodes/ffx/ffx-spec2.pdf
.. _libffx: https://github.com/kpdyer/libffx
