%global __cmake_in_source_build 1

Name:             rtl-sdr
URL:              http://sdr.osmocom.org/trac/wiki/rtl-sdr
Version:          0.6.0
Release:          1
License:          GPLv2+
BuildRequires:    cmake
BuildRequires:    pkgconfig(libusb-1.0)
BuildRequires:    udev
Summary:          SDR utilities for Realtek RTL2832 based DVB-T dongles
Source0:          %{name}-%{version}.tar.gz

%description
This package can turn your RTL2832 based DVB-T dongle into a SDR receiver.

%package devel
Summary:          Development files for rtl-sdr
Requires:         %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for rtl-sdr.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
mkdir -p _build
pushd _build
%cmake -DDETACH_KERNEL_DRIVER=ON ..
%make_build
popd

%install
pushd _build
%make_install
popd

# Remove static libs
rm -f %{buildroot}%{_libdir}/*.a

# Fix udev rules and allow access only to users in rtlsdr group
sed -i 's/GROUP="plugdev"/GROUP="rtlsdr"/' ./rtl-sdr.rules
install -Dpm 644 ./rtl-sdr.rules %{buildroot}%{_prefix}/lib/udev/rules.d/10-rtl-sdr.rules

%pre
getent group rtlsdr >/dev/null || \
  %{_sbindir}/groupadd -r rtlsdr >/dev/null 2>&1
exit 0

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/*
%{_libdir}/*.so.*
%{_prefix}/lib/udev/rules.d/10-rtl-sdr.rules

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
