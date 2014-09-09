# Prevent brp-python-bytecompile from running.
%define __os_install_post %{___build_post}

Name: harbour-squilla
Version: 0.2
Release: 1
Summary: SMS/XMPP Bridge application for Sailfish OS
License: GPLv3+
URL: https://github.com/titilambert/harbour-squilla
Source: %{name}-%{version}.tar.gz
#BuildArch: armv7l
BuildRequires: make
Requires: libsailfishapp-launcher
Requires: pyotherside-qml-plugin-python3-qt5 >= 1.2
Requires: python3-base
Requires: sailfishsilica-qt5

%description
SeaDevil is a Wake on Lan application for sailfish OS. With SeaDevil you can wake your computers using your Jolla device. You can also save your favorite computers to wake them more quickly.

%prep
%setup -q

%install
make DESTDIR=%{buildroot} PREFIX=/usr install
mkdir -p %{buildroot}/%{_datadir}/%{name}/doc
cp AUTHORS COPYING NEWS README.rst TODO %{buildroot}/%{_datadir}/%{name}/doc

%files
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%docdir %{_datadir}/%{name}/doc/

%changelog
* Tue Sep 09 2014 Thibault Cohen <titilambert@gmail.com> 0.2-1
- Fix send sms message
- Fix USB 
- Wifi seems fixed

* Fri Jul 25 2014 Thibault Cohen <titilambert@gmail.com> 0.1-1
- First alpha release
