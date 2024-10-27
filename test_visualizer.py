import pytest

from visualizer import *


@pytest.mark.parametrize("input, expected", [
    ("lib1(>=1.0)", "lib1"),
    ("lib2<=2.0", "lib2"),
    ("package_name", "package_name"),
    ("example_package(=1.5)", "example_package")
])
def test_trim_package(input, expected):
    assert trim_package(input) == expected


@pytest.mark.parametrize("dependency_text, expected", [
    ("lib1,lib2", ["lib1", "lib2"]),
])
def test_extract_dependencies(dependency_text, expected):
    assert extract_dependencies(dependency_text) == expected


@pytest.mark.parametrize("pack_desc, expected", [
    ('''
    Standards-Version: 3.9.1
Build-Depends: debhelper (>= 7.0.50)
Checksums-Sha1: 
 3f3603302c524e2ce1462c282e0033a5d2e644f2 86877 nanoblogger_3.4.2.orig.tar.gz
 5398b16b7693a545474c5f8c0e82e085148310e3 6890 nanoblogger_3.4.2-3.debian.tar.gz
    ''', "debhelper(>=7.0.50)"),
    ('''
    Vcs-Git: https://anonscm.debian.org/git/pkg-security/backdoor-factory.git
Testsuite: autopkgtest
Testsuite-Triggers: openssh-client
Build-Depends-Indep: go-md2man, dh-python, pkg-config, curl, debhelper (>= 10), python (>= 2.7)''',
     "go-md2man,dh-python,pkg-config,curl,debhelper(>=10),python(>=2.7)")
])
def test_get_dependency_text(pack_desc, expected):
    assert get_dependency_text(pack_desc) == expected


@pytest.mark.parametrize("repo, package, dict, expected", [
    ("http://archive.ubuntu.com/ubuntu/ubuntu/pool/universe/", "nano", {}, None),
    ("http://archive.ubuntu.com/ubuntu/ubuntu/pool/universe/", "somethingdasdad", {}, None),
("http://archive.ubuntu.com/ubuntu/ubuntu/pool/universe/", "obsession", {},
 ['debhelper(>=9)', 'libglib2.0-dev', 'libdbus-1-dev', 'libx11-dev', 'libgtk2.0-dev', 'valac']),
])
def test_get_dependencies(repo, package, dict, expected):
    assert get_dependencies(repo, package, dict) == expected
