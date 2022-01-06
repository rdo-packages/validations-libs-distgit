# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver 3
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name validations-libs
%global sum A collection of python libraries for the Validation Framework

Name:           python-%{upstream_name}
Summary:        %{sum}
Version:        1.0.4
Release:        0.1%{?dist}
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
<<<<<<< HEAD   (674fb6 Add configparser as requires for python2.7 on centos7 builds)
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr >= 3.1.1
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-ansible-runner >= 1.2.0
%if %{pyver} == 2
BuildRequires:  python2-mock
BuildRequires:  python-pathlib2
BuildRequires:  python-configparser
%endif
BuildRequires:  python%{pyver}-cliff >= 2.16.0
=======
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 3.1.1
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-ansible-runner >= 1.4.4
BuildRequires:  python3-oslotest >= 3.2.0
BuildRequires:  python3-cliff >= 2.16.0
>>>>>>> CHANGE (746f17 Move Cliff requirements to 2.16.0)

<<<<<<< HEAD   (674fb6 Add configparser as requires for python2.7 on centos7 builds)
Requires:       python%{pyver}-pbr >= 3.1.1
Requires:       python%{pyver}-six >= 1.11.0
Requires:       python%{pyver}-ansible-runner >= 1.2.0
%if %{pyver} == 2
Requires:       PyYAML
Requires:       python-pathlib2
Requires:       python-configparser
%else
Requires:       python%{pyver}-PyYAML
%endif
Requires:       python%{pyver}-cliff >= 2.16.0
=======
Requires:       python3-pbr >= 3.1.1
Requires:       python3-six >= 1.11.0
Requires:       python3-ansible-runner >= 1.4.4
Requires:       python3-PyYAML
BuildRequires:  python3-cliff >= 2.16.0
>>>>>>> CHANGE (746f17 Move Cliff requirements to 2.16.0)

%description -n python%{pyver}-%{upstream_name}
A collection of python libraries for the Validation Framework

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%if %{pyver} == 2
find validations_libs -name \*.py -exec sed -i "1i\# -*- coding: utf-8 -*-" {} +
%endif

%build
%{pyver_build}

%install
%{pyver_install}

# Cleanup once https://review.opendev.org/#/c/755311/ is in tag release
if [ ! -d "%{buildroot}%{_datadir}/ansible" ]; then
mkdir -p %{buildroot}%{_datadir}/ansible
fi

# TODO remove this when https://review.opendev.org/c/openstack/validations-libs/+/792460 merged
if [ ! -d "%{buildroot}%{_sysconfdir}" ]; then
mkdir -p %{buildroot}%{_sysconfdir}
fi

if [ -f "%{buildroot}/usr/etc/validation.cfg" ]; then
mv %{buildroot}/usr/etc/validation.cfg %{buildroot}%{_sysconfdir}/validation.cfg
fi

if [ ! -f "%{buildroot}%{_sysconfdir}/validation.cfg" ]; then
cat <<EOF >%{buildroot}%{_sysconfdir}/validation.cfg
[default]
ansible_base_dir = /usr/share/ansible/
EOF
fi

%check

# Workaround py27 tests due to:
# https://bugs.launchpad.net/tripleo/+bug/1956751
%if %{pyver} == 2
PYTHON=%{pyver_bin} %{pyver_bin} setup.py test ||:
%else
PYTHON=%{pyver_bin} %{pyver_bin} setup.py test
%endif

%files -n python%{pyver}-%{upstream_name}
%license LICENSE
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/validation.cfg
%if 0%{?dlrn} > 0
%{_bindir}/validation
%endif
%doc README* AUTHORS ChangeLog
%{pyver_sitelib}/validations_libs
%{pyver_sitelib}/validations_libs-*.egg-info
%exclude %{pyver_sitelib}/validations_libs/test*

%changelog
* Fri Sep 25 2020 RDO <dev@lists.rdoproject.org> 1.0.4-0.1
- Update to 1.0.4
