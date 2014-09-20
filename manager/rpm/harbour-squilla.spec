# Prevent brp-python-bytecompile from running.
%define __os_install_post %{___build_post}

Name: harbour-squilla
Version: 0.3
Release: 1
Summary: SMS/XMPP Bridge application for Sailfish OS
License: GPLv3+
URL: https://github.com/titilambert/harbour-squilla
Source: %{name}-%{version}.tar.gz
BuildRequires: make
Requires: libsailfishapp-launcher
Requires: pyotherside-qml-plugin-python3-qt5 >= 1.2
Requires: python3-base
Requires: sailfishsilica-qt5

%description
Squilla is a application to control your Jolla device from a web interface.
Squilla uses modules to add more features

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
* Sat Sep 20 2014 Thibault Cohen <titilambert@gmail.com> 0.3-1
- First release of the new squilla

* Tue Sep 09 2014 Thibault Cohen <titilambert@gmail.com> 0.2-1
- Fix send sms message
- Fix USB 
- Wifi seems fixed

* Fri Jul 25 2014 Thibault Cohen <titilambert@gmail.com> 0.1-1
- First alpha release
