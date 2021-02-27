#
# Conditional build:
%bcond_with	tests	# unit tests (some failing)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Filesystem abstraction layer for Python 2
Summary(pl.UTF-8):	Warstwa abstrakcji systemu plików dla Pythona 2
Name:		python-fs
Version:	2.4.11
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/fs/
Source0:	https://files.pythonhosted.org/packages/source/f/fs/fs-%{version}.tar.gz
# Source0-md5:	01b2e57b3622aa49cbaa668c81a87cb7
Patch0:		%{name}-py3-requires.patch
URL:		https://pypi.org/project/fs/
%if %{with tests} && %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-appdirs >= 1.4.3
BuildRequires:	python-backports.os >= 0.1
BuildRequires:	python-enum34 >= 1.1.6
BuildRequires:	python-mock
BuildRequires:	python-pyftpdlib
BuildRequires:	python-pytz
BuildRequires:	python-scandir >= 1.5
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-typing >= 3.6
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-appdirs >= 1.4.3
BuildRequires:	python3-pyftpdlib
BuildRequires:	python3-pytz
%if "%{py3_ver}" < "3.5"
BuildRequires:	python3-scandir >= 1.5
%endif
BuildRequires:	python3-six >= 1.10.0
%if "%{py3_ver}" < "3.6"
BuildRequires:	python3-typing >= 3.6
%endif
%endif
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

%prep
%setup -q -n fs-%{version}
%patch0 -p1

# relies on pyftpdlib tests
%{__rm} tests/test_ftpfs.py

%build
%if %{with python2}
%py_build

%if %{with tests}
LC_ALL=C.UTF-8 PYTHONPATH=$(pwd) \
%{__python} -m unittest discover -s tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
LC_ALL=C.UTF-8 PYTHONPATH=$(pwd) \
%{__python3} -m unittest discover -s tests
%endif
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
