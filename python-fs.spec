#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Filesystem abstraction layer for Python 2
Summary(pl.UTF-8):	Warstwa abstrakcji systemu plików dla Pythona 2
Name:		python-fs
Version:	2.0.1
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/fs/
Source0:	https://files.pythonhosted.org/packages/source/f/fs/fs-%{version}.tar.gz
# Source0-md5:	7e2c2d22b96ca0b0fbf8c0d1c8e5fd81
Patch0:		%{name}-py3-requires.patch
URL:		https://pypi.python.org/pypi/fs/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-appdirs >= 1.4.0
BuildRequires:	python-enum34 >= 1.1.6
BuildRequires:	python-mock
BuildRequires:	python-pyftpdlib
BuildRequires:	python-pytz
BuildRequires:	python-scandir >= 1.5
BuildRequires:	python-six >= 1.10.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-appdirs >= 1.4.0
%if "%{py3_ver}" < "3.4"
BuildRequires:	python3-enum34 >= 1.1.6
%endif
#BuildRequires:	python3-mock
BuildRequires:	python3-pyftpdlib
BuildRequires:	python3-pytz
%if "%{py3_ver}" < "3.5"
BuildRequires:	python3-scandir >= 1.5
%endif
BuildRequires:	python3-six >= 1.10.0
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
Requires:	python3-modules >= 1:3.3

%description -n python3-fs
A filesystem abstraction library, successor to PyFilesystem.

%description -n python3-fs -l pl.UTF-8
Biblioteka abstrakcji systemu plików, następca PyFilesystem.

%prep
%setup -q -n fs-%{version}
%patch0 -p1 -b .orig

%build
# for tests
export PYTHONPATH=$(pwd)

%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
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
%doc README.txt
%{py_sitescriptdir}/fs
%{py_sitescriptdir}/fs-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-fs
%defattr(644,root,root,755)
%doc README.txt
%{py3_sitescriptdir}/fs
%{py3_sitescriptdir}/fs-%{version}-py*.egg-info
%endif
