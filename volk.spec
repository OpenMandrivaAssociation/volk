%define major	3
%define libvolk %mklibname %{name} %{major}
%define devvolk %mklibname %{name} -d

Name:		volk
Version:	3.2.0
Release:	2
Summary:	Vector-Optimized Library of Kernels
Group:		Communications/Radio
License:	LGPL-3.0-or-later
URL:		https://libvolk.org
Source0:	https://github.com/gnuradio/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
## NOTE The upstream tarball includes git submodule cpu_features, however OMLx packages cpu_features separately-
## NOTE and the VOLK CmakeLists script checks for and prioritise the distro version of cpu_features over the-
## NOTE included submodule version when supplied via the BuildRequires:cpu_features-devel line below.
## NOTE This is now the recommended way to handle cpu_features by upstream - https://github.com/gnuradio/volk#missing-submodule


BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	cpu_features-devel
BuildRequires:	doxygen
BuildRequires:	git
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-mako
BuildRequires:	python-six
Requires:	%{libvolk} = %{version}-%{release}
Conflicts:	python-gnuradio < 3.9.0.0
Conflicts:	gnuradio-devel < 3.9.0.0

%description
VOLK stands for Vector-Optimized Library of Kernels.
It is a library that was introduced into GNU Radio in December 2010.
This is now packaged independently of GNU Radio.

############################
%package -n %{libvolk}
Summary:	Volk libraries
Group:		System/Libraries
Obsoletes:	%{_lib}gnuradio-volk0 < 3.8
Conflicts:	%{_lib}gnuradio-volk0 < 3.8

%description -n %{libvolk}
VOLK stands for Vector-Optimized Library of Kernels.
It is a library that was introduced into GNU Radio in December 2010.

############################
%package -n %{devvolk}
Summary:	Volk devel files
Group:		Development/Other
Requires:	%{libvolk} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}gnuradio-volk-devel < 3.8
Conflicts:	%{_lib}gnuradio-volk-devel < 3.8

%description -n %{devvolk}
This package contains header files needed by developers.

###########################
%package doc
Summary:	Documentation files for VOLK
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
Documentation files for VOLK.

###########################
%prep
%autosetup -p1

%build
%cmake \
	-DPYTHON_EXECUTABLE=%{__python} \
	-DVOLK_PYTHON_DIR:PATH=%{python_sitelib} \
	-DENABLE_PROFILING=OFF
%make_build
# Build docs
%make_build volk_doc

%install
%make_install -C build
mkdir -p %{buildroot}%{_docdir}/%{name}/html
mv %{builddir}/%{name}-%{version}/build/html %{buildroot}%{_docdir}/%{name}/

%files
%{_bindir}/volk_modtool
%{_bindir}/volk_profile
%{_bindir}/volk-config-info
%{python3_sitelib}/volk_modtool/
%doc README.md
%doc docs/CHANGELOG.md
%exclude %doc %{_docdir}/%{name}/html/*
%license COPYING

%files -n %{libvolk}
%{_libdir}/libvolk.so.%{major}{,.*}


%files -n %{devvolk}
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/volk.pc
%{_libdir}/libvolk.so
%{_libdir}/cmake/volk

%files doc
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/html/*

%changelog
