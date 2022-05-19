%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

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
BuildRequires:  python3-stestr
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-ansible-runner >= 1.4.0
BuildRequires:  python3-cliff >= 2.16.0
BuildRequires:  (python3dist(ansible) >= 2.8 or ansible-core)
BuildRequires:  python3-oslotest >= 3.2.0
BuildRequires:  python3-docutils
BuildRequires:  gzip

Requires:       python3-pbr >= 3.1.1
Requires:       python3-six >= 1.11.0
Requires:       python3-ansible-runner >= 1.4.0
Requires:       python3-PyYAML >= 3.13
Requires:       python3-cliff >= 2.16.0
Requires:       (python3dist(ansible) >= 2.8 or ansible-core)

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
#Man pages build
grep -v "\(image::\)\|\(:target:\)" README.rst | rst2man > vf.1 
gzip -c vf.1 > vf.1.gz

%install
%{py3_install}
if [ ! -d "%{buildroot}%{_sysconfdir}" ]; then
mkdir -p %{buildroot}%{_sysconfdir}
fi

if [ -f "%{buildroot}/usr/etc/validation.cfg" ]; then
mv %{buildroot}/usr/etc/validation.cfg %{buildroot}%{_sysconfdir}/validation.cfg
fi

# TODO(jpodivin) until callbacks are moved to validations-libs
# https://review.opendev.org/c/openstack/validations-libs/+/820551
if [ ! -d "%{buildroot}%{_datadir}/ansible/callback_plugins" ]; then
mkdir -p %{buildroot}%{_datadir}/ansible/callback_plugins
fi

# Install man pages
mkdir -p %{_mandir}/man1/
mv vf.1.gz %{_mandir}/man1/vf.1.gz

%check
PYTHON=%{__python3} stestr run

%files -n python3-%{upstream_name}
%license LICENSE
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/validation.cfg
%{_bindir}/validation
%doc README.rst AUTHORS ChangeLog
%doc %{_mandir}/man1/vf.1.gz
%{python3_sitelib}/validations_libs
%{python3_sitelib}/validations_libs-*.egg-info
%{_datadir}/ansible/callback_plugins/
%exclude %{python3_sitelib}/validations_libs/test*

%changelog
