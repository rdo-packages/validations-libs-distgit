%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x4c29ff0e437f3351fd82bdf47c5a3bc787dc7035

%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name validations-libs
%global sum A collection of python libraries for the Validation Framework

Name:           python-%{upstream_name}
Summary:        %{sum}
Version:        1.3.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://opendev.org/openstack/validations-libs
Source0:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
A collection of python libraries for the Validation Framework

%package -n     python3-%{upstream_name}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{upstream_name}}

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 3.1.1
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-ansible-runner >= 1.4.4
BuildRequires:  python3-cliff >= 3.2.0

Requires:       python3-pbr >= 3.1.1
Requires:       python3-six >= 1.11.0
Requires:       python3-ansible-runner >= 1.4.4
Requires:       python3-PyYAML
Requires:       python3-cliff >= 3.2.0

%description -n python3-%{upstream_name}
A collection of python libraries for the Validation Framework

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}

%check
PYTHON=%{__python3} %{__python3} setup.py test

%files -n python3-%{upstream_name}
%license LICENSE
%{_bindir}/validation
%doc README* AUTHORS ChangeLog
%{python3_sitelib}/validations_libs
%{python3_sitelib}/validations_libs-*.egg-info
%exclude %{python3_sitelib}/validations_libs/test*

%changelog
* Mon Aug 16 2021 Jiri Podivin <jpodivin@redhat.com> 1.3.0-1
- Update to 1.3.0

* Mon Aug 16 2021 Jiri Podivin <jpodivin@redhat.com> 1.2.0-1
- Update to 1.2.0

* Thu May 06 2021 RDO <dev@lists.rdoproject.org> 1.1.0-1
- Update to 1.1.0

