
%{!?upstream_version: %global upstream_version %{version}}
%global upstream_name validations-libs
%global sum A collection of python libraries for the Validation Framework

Name:           python-%{upstream_name}
Summary:        %{sum}
Version:        1.7.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://opendev.org/openstack/validations-libs
Source0:        https://tarballs.opendev.org/openstack/%{upstream_name}/%{upstream_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
A collection of python libraries for the Validation Framework

%package -n     python3-%{upstream_name}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{upstream_name}}

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 3.1.1
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-ansible-runner >= 1.4.4
BuildRequires:  python3-oslotest >= 3.2.0
BuildRequires:  python3-cliff >= 2.16.0

Requires:       python3-pbr >= 3.1.1
Requires:       python3-six >= 1.11.0
Requires:       python3-ansible-runner >= 1.4.4
Requires:       python3-PyYAML
BuildRequires:  python3-cliff >= 2.16.0

%description -n python3-%{upstream_name}
A collection of python libraries for the Validation Framework

%prep
%autosetup -n %{upstream_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}

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

# TODO(jpodivin) until callbacks are moved to validations-libs
# https://review.opendev.org/c/openstack/validations-libs/+/820551
if [ ! -d "%{buildroot}%{_datadir}/ansible/callback_plugins" ]; then
mkdir -p %{buildroot}%{_datadir}/ansible/callback_plugins
fi

%check
PYTHON=%{__python3} %{__python3} setup.py test

%files -n python3-%{upstream_name}
%license LICENSE
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/validation.cfg
%if 0%{?dlrn} > 0
%{_bindir}/validation
%endif
%doc README* AUTHORS ChangeLog
%{python3_sitelib}/validations_libs
%{python3_sitelib}/validations_libs-*.egg-info
%{_datadir}/ansible/callback_plugins/
%exclude %{python3_sitelib}/validations_libs/test*

%changelog
* Mon Jun 22 2020 RDO <dev@lists.rdoproject.org> 1.0.1-1
- Update to 1.0.1

* Mon May 18 2020 RDO <dev@lists.rdoproject.org> 1.0.0-1
- Update to 1.0.0


