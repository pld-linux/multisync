Summary:	OpenSync data synchronization commandline programs
Name:		multisync
Version:	0.90.18
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/multisync/%{name}-%{version}.tar.gz?format=raw
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
