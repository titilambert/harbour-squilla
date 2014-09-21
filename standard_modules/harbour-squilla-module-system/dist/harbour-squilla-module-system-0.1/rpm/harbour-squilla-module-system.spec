# Prevent brp-python-bytecompile from running.
%define __os_install_post %{___build_post}

Name: harbour-squilla-module-system
Version: 0.1
Release: 1
Summary: Squilla system module
License: GPLv3+
URL: https://github.com/titilambert/harbour-squilla
Source: %{name}-%{version}.tar.gz
BuildRequires: make
Requires: python3-base

%description
This Squilla module show informations about Jolla phone.
Also, It have basic controls on Jolla phone.

%prep
%setup -q

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=/usr install
mkdir -p %{buildroot}/%{_datadir}/%{name}/doc
cp AUTHORS COPYING NEWS README.rst TODO %{buildroot}/%{_datadir}/%{name}/doc

%files
%{_datadir}/%{name}
%{_datadir}/harbour-squilla-daemon/squilla/modules/%{name}
%docdir %{_datadir}/%{name}/doc/

%changelog
* Sat Sep 20 2014 Thibault Cohen <titilambert@gmail.com> 0.3-1
- First release
