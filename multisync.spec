
#
# todo:
# - finish the spec with plugins separated into subpackages
# - irmc plugin tries to link with glib1... make a patch and send it to
#   authors
#

Summary:	PIM data synchronization program
Summary(pl):	Program do synchronizacji danych 
Name:		multisync
Version:	0.80
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	3b6fc4ea80a1b013f3cb3707f46ff5a3
URL:		http://multisync.sourceforge.net/
BuildRequires:	bluez-libs-devel >= 2.4
BuildRequires:	bluez-sdp-devel >= 1.2
BuildRequires:	evolution-devel >= 1.4.3
BuildRequires:	libgnomeui-devel >= 2.3
BuildRequires:	openldap-devel >= 2.1.12
BuildRequires:	openobex-devel >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PIM data synchronization program.

%description -l pl
Program do synchronizacji danych.

%package subpackage
Summary:	-
Summary(pl):	-
Group:		-

%description subpackage

%description subpackage -l pl

%prep
%setup -q

%build
%configure
%{__make}

# ugly hack to build evolution plugin...
sed 's#/bin/sh#/bin/bash#' < plugins/evolution_sync/configure > configure.evolution
mv configure.evolution plugins/evolution_sync/configure
chmod 755 plugins/evolution_sync/configure

# build plugins
for dir in plugins/*; do
    cd $dir
    %configure
    %{__make}
    cd -
done


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# build plugins
for dir in plugins/*; do
    cd $dir
    %{__make} install \
        DESTDIR=$RPM_BUILD_ROOT
    cd -
done

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}

%files subpackage
%defattr(644,root,root,755)
%doc extras/*.gz
%{_datadir}/%{name}-ext
