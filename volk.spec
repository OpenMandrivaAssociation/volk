%define major	2
%define libvolk %mklibname %{name} %{major}
%define devvolk %mklibname %{name} -d

Name:		volk
Version:	2.5.0
Release:	1
Summary:	Vector-Optimized Library of Kernels
Group:		Communications/Radio
License:	GPLv3+
URL:		http://libvolk.org
Source0:	https://github.com/gnuradio/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
## NOTE Do not use upstream tarball as it does not include git submodules
## NOTE Edit the version in mk-tar script and run it in SOURCES to build tarball
Source1:	mk-tar

BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	git
BuildRequires:	pkgconfig(orc-0.4)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python-mako
BuildRequires:	python-six
Requires:	%{libvolk} = %{version}-%{release}

%description
VOLK stands for Vector-Optimized Library of Kernels.
It is a library that was introduced into GNU Radio in December 2010.
This is now packaged independently of GNU Radio.

%files
%{_bindir}/volk_modtool
%{_bindir}/volk_profile
%{_bindir}/volk-config-info
%{_bindir}/list_cpu_features
%{python3_sitelib}/volk_modtool/

############################
%package -n %{libvolk}
Summary:	Volk libraries
Group:		System/Libraries
Obsoletes:	%{_lib}gnuradio-volk0 < 3.8
Conflicts:	%{_lib}gnuradio-volk0 < 3.8

%description -n %{libvolk}
VOLK stands for Vector-Optimized Library of Kernels.
It is a library that was introduced into GNU Radio in December 2010.

%files -n %{libvolk}
%{_libdir}/libvolk.so.%{major}{,.*}

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

%files -n %{devvolk}
%{_includedir}/%{name}/
%{_includedir}/cpu_features/
%{_libdir}/pkgconfig/volk.pc
%{_libdir}/libvolk.so
%{_libdir}/cmake/volk
%{_libdir}/cmake/CpuFeatures/

###########################
%prep
%autosetup -p1

%build
%cmake \
	-DPYTHON_EXECUTABLE=%{__python} \
	-DVOLK_PYTHON_DIR:PATH=%{python_sitelib} \
	-DENABLE_PROFILING=OFF
%make_build

%install
%make_install -C build
rm %{buildroot}%{_libdir}/*.a
