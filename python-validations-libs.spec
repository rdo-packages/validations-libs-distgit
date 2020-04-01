# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name validations-libs
%global sum A collection of python libraries for the Validation Framework

Name:           python-%{upstream_name}
Summary:        %{sum}
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://opendev.org/openstack/validations-libs
Source0:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
A collection of python libraries for the Validation Framework

%package -n     python%{pyver}-%{upstream_name}
Summary:        %{sum}
%{?python_provide:%python_provide python%{pyver}-%{upstream_name}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr >= 3.1.1
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-ansible-runner >= 1.2.0

Requires:       python%{pyver}-pbr >= 3.1.1
Requires:       python%{pyver}-six >= 1.11.0
Requires:       python%{pyver}-ansible-runner >= 1.2.0
%if %{pyver} == 2
Requires:       PyYAML
%else
Requires:       python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{upstream_name}
A collection of python libraries for the Validation Framework

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pyver_build}

%install
%{pyver_install}

%check
PYTHON=%{pyver_bin} %{pyver_bin} setup.py test

%files -n python%{pyver}-%{upstream_name}
%license LICENSE
%doc README* AUTHORS ChangeLog
%{pyver_sitelib}/validations_libs
%{pyver_sitelib}/validations_libs-*.egg-info
%exclude %{pyver_sitelib}/validations_libs/test*

%changelog
