#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Filesystem abstraction layer for Python 2
Summary(pl.UTF-8):	Warstwa abstrakcji systemu plików dla Pythona 2
Name:		python-fs
Version:	2.4.16
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/fs/
Source0:	https://files.pythonhosted.org/packages/source/f/fs/fs-%{version}.tar.gz
# Source0-md5:	2c9dae3d52950407fe265c3576396c33
URL:		https://pypi.org/project/fs/
%if %{with tests} && %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:38.3.0
%if %{with tests}
BuildRequires:	python-appdirs >= 1.4.3
BuildRequires:	python-backports.os >= 0.1
BuildRequires:	python-enum34 >= 1.1.6
BuildRequires:	python-mock >= 3.0
BuildRequires:	python-parameterized >= 0.8
BuildRequires:	python-psutil >= 5.0
BuildRequires:	python-pyftpdlib >= 1.5
BuildRequires:	python-pysendfile >= 2.0
BuildRequires:	python-pytest >= 4.6
BuildRequires:	python-pytest-randomly >= 1.2
BuildRequires:	python-pytz
BuildRequires:	python-scandir >= 1.5
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-typing >= 3.6
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools >= 1:38.3.0
%if %{with tests}
BuildRequires:	python3-appdirs >= 1.4.3
BuildRequires:	python3-parameterized >= 0.8
BuildRequires:	python3-psutil >= 5.0
BuildRequires:	python3-pyftpdlib >= 1.5
BuildRequires:	python3-pytest >= 4.6
BuildRequires:	python3-pytest-randomly >= 1.2
BuildRequires:	python3-pytz
%if "%{ver_lt '%{py3_ver}' '3.5'}" == "1"
BuildRequires:	python3-scandir >= 1.5
%endif
BuildRequires:	python3-six >= 1.10.0
%if "%{ver_lt '%{py3_ver}' '3.6'}" == "1"
BuildRequires:	python3-typing >= 3.6
%endif
%endif
%endif
%if %{with doc}
BuildRequires:	python3-recommonmark >= 0.6
BuildRequires:	python3-sphinx_rtd_theme >= 0.5.1
BuildRequires:	sphinx-pdg-3 >= 3.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A filesystem abstraction library, successor to PyFilesystem.

%description -l pl.UTF-8
Biblioteka abstrakcji systemu plików, następca PyFilesystem.

%package -n python3-fs
Summary:	Filesystem abstraction layer for Python 3
Summary(pl.UTF-8):	Warstwa abstrakcji systemu plików dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-fs
A filesystem abstraction library, successor to PyFilesystem.

%description -n python3-fs -l pl.UTF-8
Biblioteka abstrakcji systemu plików, następca PyFilesystem.

%package apidocs
Summary:	API documentation for Python fs module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona fs
Group:		Documentation

%description apidocs
API documentation for Python fs module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona fs.

%prep
%setup -q -n fs-%{version}

# relies on pyftpdlib tests
%{__rm} tests/test_ftpfs.py

%build
%if %{with python2}
%py_build

%if %{with tests}
# 3 tests apparently fail with python2.7
LC_ALL=C.UTF-8 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python} -m pytest tests \
	-k 'not test_move_file_same_fs_read_only_source and not test_move_dir and not test_move_file'
#	-k 'not TestMove.test_move_file_same_fs_read_only_source and not TestWrapReadOnlySyspath.test_move_dir and not TestWrapReadOnlySyspath.test_move_file'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py_sitescriptdir}/fs
%{py_sitescriptdir}/fs-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-fs
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/fs
%{py3_sitescriptdir}/fs-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,reference,*.html,*.js}
%endif
