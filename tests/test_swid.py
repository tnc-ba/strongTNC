# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from apps.swid import utils
from tncapp import models as tncapp_models

import pytest


### FIXTURES ###

@pytest.fixture
def swidtag(request, transactional_db):
    """
    Create and return a apps.swid.models.Tag instance based on the specified file.

    This requires the test using this fixture to be parametrized with a
    'filename' argument that specifies the filename of the SWID tag test file
    inside `tests/test_tags/`.

    """
    filename = request.getfuncargvalue('filename')
    with open('tests/test_tags/%s' % filename, 'r') as f:
        tag_xml = f.read()
        return utils.process_swid_tag(tag_xml)


### SWID XML PROCESSING TESTS ###

@pytest.mark.parametrize(['filename', 'package_name'], [
    ('strongswan.short.swidtag', 'strongswan'),
    ('strongswan.full.swidtag', 'strongswan'),
    ('cowsay.short.swidtag', 'cowsay'),
    ('cowsay.full.swidtag', 'cowsay'),
    ('strongswan-tnc-imcvs.short.swidtag', 'strongswan-tnc-imcvs'),
    ('strongswan-tnc-imcvs.full.swidtag', 'strongswan-tnc-imcvs'),
])
def test_tag_name(swidtag, filename, package_name):
    assert swidtag.package_name == package_name


@pytest.mark.parametrize(['filename', 'unique_id'], [
    ('strongswan.short.swidtag', 'debian_7.4-x86_64-strongswan-4.5.2-1.5+deb7u3'),
    ('strongswan.full.swidtag', 'debian_7.4-x86_64-strongswan-4.5.2-1.5+deb7u3'),
    ('cowsay.short.swidtag', 'debian_7.4-x86_64-cowsay-3.03+dfsg1-4'),
    ('cowsay.full.swidtag', 'debian_7.4-x86_64-cowsay-3.03+dfsg1-4'),
    ('strongswan-tnc-imcvs.short.swidtag', 'fedora_19-x86_64-strongswan-tnc-imcvs-5.1.2-4.fc19'),
    ('strongswan-tnc-imcvs.full.swidtag', 'fedora_19-x86_64-strongswan-tnc-imcvs-5.1.2-4.fc19'),
])
def test_tag_unique_id(swidtag, filename, unique_id):
    assert swidtag.unique_id == unique_id


@pytest.mark.parametrize(['filename', 'version'], [
    ('strongswan.short.swidtag', '4.5.2-1.5+deb7u3'),
    ('strongswan.full.swidtag', '4.5.2-1.5+deb7u3'),
    ('cowsay.short.swidtag', '3.03+dfsg1-4'),
    ('cowsay.full.swidtag', '3.03+dfsg1-4'),
    ('strongswan-tnc-imcvs.short.swidtag', '5.1.2-4.fc19'),
    ('strongswan-tnc-imcvs.full.swidtag', '5.1.2-4.fc19'),
])
def test_tag_version(swidtag, filename, version):
    assert swidtag.version == version


@pytest.mark.parametrize('filename', [
    'strongswan.short.swidtag',
    'strongswan.full.swidtag',
    'cowsay.short.swidtag',
    'cowsay.full.swidtag',
    'strongswan-tnc-imcvs.short.swidtag',
    'strongswan-tnc-imcvs.full.swidtag',
])
def test_tag_xml(swidtag, filename):
    assert swidtag.swid_xml == open('tests/test_tags/%s' % filename, 'r').read()


@pytest.mark.parametrize(['filename', 'directories', 'files', 'filecount'], [
    ('strongswan.full.swidtag', ['/usr/share/doc/strongswan'], [
        'README.gz',
        'CREDITS.gz',
        'README.Debian.gz',
        'NEWS.Debian.gz',
        'changelog.gz',
    ], 7),
    ('cowsay.full.swidtag', ['/usr/share/cowsay/cows', '/usr/games'], [
        'cowsay',
        'cowthink',
        'vader-koala.cow',
        'elephant-in-snake.cow',
        'ghostbusters.cow',
    ], 61),
    ('strongswan-tnc-imcvs.full.swidtag', ['/usr/lib64/strongswan', '/usr/lib64/strongswan/imcvs'], [
        'libradius.so.0',
        'libtnccs.so.0.0.0',
        'imv-attestation.so',
        'imv-test.so',
    ], 35),
])
def test_tag_files(swidtag, filename, directories, files, filecount):
    assert tncapp_models.File.objects.filter(name__in=files).count() == len(files)
    assert tncapp_models.Directory.objects.filter(path__in=directories).count() == len(directories)
    assert swidtag.files.count() == filecount
