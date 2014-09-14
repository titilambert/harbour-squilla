# Prevent brp-python-bytecompile from running.
%define __os_install_post %{___build_post}

Name: harbour-squilla-daemon
Version: 0.3
Release: 1
Summary: SMS/XMPP Bridge application for Sailfish OS
License: GPLv3+
URL: https://github.com/titilambert/harbour-squilla
Source: %{name}-%{version}.tar.gz
BuildRequires: make
Requires: python3-base

%description
Squilla is a application to control your Jolla device from a web interface.
Squilla uses modules to add more features

%prep
%setup -q

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=/usr install
mkdir -p %{buildroot}/%{_datadir}/%{name}/doc
cp AUTHORS COPYING NEWS README.rst TODO %{buildroot}/%{_datadir}/%{name}/doc

%preun
if /sbin/pidof harbour-squilla-daemon > /dev/null; then
    killall harbour-squilla-daemon
fi

%postun
rm -f %{_bindir}/harbour-squilla-daemon

%pre
if /sbin/pidof harbour-squilla-daemon > /dev/null; then
    killall harbour-squilla-daemon
fi

%post
ln -f -s %{_datadir}/%{name}/run_squilla_daemon.py  %{_bindir}/harbour-squilla-daemon

%files
%{_datadir}/%{name}
%docdir %{_datadir}/%{name}/doc/

%changelog
* Sat Sep 20 2014 Thibault Cohen <titilambert@gmail.com> 0.3-1
- First release
