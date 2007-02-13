Summary:	OpenSync data synchronization commandline programs
Summary(pl.UTF-8):	Programy do synchronizacji danych OpenSync
Name:		multisync
Version:	0.90.18
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.opensync.org/attachment/wiki/download/%{name}-%{version}.tar.gz?format=raw
# Source0-md5:	d55d8eaeecb825b87a25eeceaef92cb9
URL:		http://opensync.org/
BuildRequires:	libopensync-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenSync is a synchronization framework that is platform and distribution
independent.

It consists of several plugins that can be used to connect to devices,
a powerful sync-engine and the framework itself.

This package contains commandline programs to use OpenSync framework.

%description -l pl.UTF-8
OpenSync to niezależny od platformy i dystrybucji szkielet do
synchronizacji danych.

Składa się z różnych wtyczek, których można używać do łączenia z
urządzeniami, potężnego silnika synchronizacji oraz samego szkieletu.

Ten pakiet zawiera działające z linii poleceń programy do korzystania
ze szkieletu OpenSync.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
