
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
BuildRequires:	evolution-static >= 1.4.3
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

%package %{name}-evolution
Summary:	A Ximian Evolution plugin for MultiSync
Summary(pl):	Wtyczka do Evolution
Group:		X11/Applications

%description %{name}-evolution
This is a plugin to enable synchronization of Ximian Evolution data
using MultiSync.

%description %{name}-evolution -l pl
Wtyczka do Evolution

%package %{name}-backup
Summary:	A Ximian Evolution plugin for backup
Summary(pl):	Wtyczka do kopii zapasowych
Group:		X11/Applications

%description %{name}-backup
This is a plugin to enable synchronization of backup
using MultiSync.

%description %{name}-backup -l pl
Wtyczka do kopii zapasowych

%package %{name}-irmc
Summary:	A Ximian Evolution plugin for IrMC
Summary(pl):	Wtyczka do IrMC
Group:		X11/Applications

%description %{name}-irmc
This is a plugin to enable synchronization of IrMC
using MultiSync.

%description %{name}-irmc -l pl
Wtyczka do IrMC 

%package %{name}-irmc-bluetooth
Summary:	A Ximian Evolution plugin for IrMC Bluetooth
Summary(pl):	Wtyczka do IrMC Bluetooth
Group:		X11/Applications

%description %{name}-irmc-bluetooth
This is a plugin to enable synchronization of IrMC Bluetooth
using MultiSync.

%description %{name}-irmc-bluetooth -l pl
Wtyczka do IrMC Bluetooth

%package %{name}-ldap
Summary:	A Ximian Evolution plugin for LDAP
Summary(pl):	Wtyczka do LDAP
Group:		X11/Applications

%description %{name}-ldap
This is a plugin to enable synchronization of LDAP
using MultiSync.

%description %{name}-ldap -l pl
Wtyczka do LDAP

%package %{name}-syncml
Summary:	A Ximian Evolution plugin for SynCML
Summary(pl):	Wtyczka do 
Group:		X11/Applications

%description %{name}-syncml
This is a SyncML 1.1 plugin for the MultiSync synchronization engine. It
allows synchronization of SyncML-enabled devices, such as the SonyEricsson
P800, as well as remote MultiSync to MultiSync synchronization over the
internet.

%description %{name}-syncml -l pl
Wtyczka do SyncML

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
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}

%files subpackage
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext

%files %{name}-evolution
%defattr(644,root,root,755)
%{_libdir}/%{name}/libevolution_sync.so*

%files %{name}-backup
%defattr(644,root,root,755)
%{_libdir}/%{name}/libbackup_plugin.so*

%files %{name}-irmc-bluetooth
%defattr(644,root,root,755)
%{_libdir}/%{name}/libirmc_bluetooth.so*

%files %{name}-irmc
%defattr(644,root,root,755)
%{_libdir}/%{name}/libirmc_sync.so*

%files %{name}-ldap
%defattr(644,root,root,755)
%{_libdir}/%{name}/libldap_plugin.so*

%files %{name}-syncml
%defattr(644,root,root,755)
%{_libdir}/%{name}/libsyncml_plugin.so*
