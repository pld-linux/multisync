
#
# TODO:
# - devel subpackage
# - -avoid-version patch for plugins and send it to authors
# - review pl translations
#

Summary:	PIM data synchronization program
Summary(pl):	Program do synchronizacji danych
Name:		multisync
Version:	0.81
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	e9091a2a1a364f2afb71149928a26c78
URL:		http://multisync.sourceforge.net/
BuildRequires:	bluez-libs-devel >= 2.4
BuildRequires:	bluez-sdp-devel >= 1.2
BuildRequires:	evolution-devel >= 1.4.3
BuildRequires:	libgnomeui-devel >= 2.3
BuildRequires:	openldap-devel >= 2.1.12
BuildRequires:	openobex-devel >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MultiSync is a program to synchronize calendars, addressbooks and
other PIM data between programs on your computer and other computers,
mobile devices, PDAs or cell phones. Currently it has (in separate
packages) plugins for Ximian Evolution, IrMC mobile devices, SyncML,
and for backup.
%if 0
and Opie / Zaurus PDAs.
%endif

%description -l pl
Program do synchronizacji kalendarzy, ksi��ek adresowych i innych
danych odobistych pomi�dzy r�nymi programami w ramach jednego
komputera, jak te� pomi�dzy r�nymi komputerami i urz�dzeniami
przeno�nymi. Aktualnie posiada wtyczki (w osobnych pakietach) do:
Evolution Ximiana, przeno�nych urz�dze� IrMC, SyncML i kopii
zapasowych.

%package evolution
Summary:	A Ximian Evolution plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do Evolution Ximiana
Group:		X11/Applications
Requires:	%{name} = %{version}

%description evolution
This is a plugin to enable synchronization of Ximian Evolution data
using MultiSync.

%description evolution -l pl
Jest to wtyczka umo�liwiaj�ca synchronizacj� Evolution Ximiana za
pomoc� MultiSync.

%package backup
Summary:	A backup plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do kopii zapasowych
Group:		X11/Applications
Requires:	%{name} = %{version}

%description backup
This is a MultiSync plugin which backs up your calendar/phonebook/etc.
data.

%description backup -l pl
Jest to wtyczka MultiSynca tworz�ca kopie zapasowe kalendarza/ksi��ki
adresowej/itp.

%package irmc
Summary:	An IrMC (SonyEricsson T39/T68i/T610, Siemens S55) plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do IrMC (SonyEricsson T39/T68i/T610, Siemens S55)
Group:		X11/Applications
Requires:	%{name} = %{version}

%description irmc
This is a MultiSync plugin for IrMC mobile clients (cell phones
such as SonyEricsson T39/T68/T610 and Siemens S55) connected via
Bluetooth, IR or cable.

%description irmc -l pl
Jest to wtyczka MultiSynca do wsp�pracy z przeno�nymi klientami IrMC
(telefony kom�rkowe takie jak SonyEricsson T39/T68/T610 i Siemens S55)
pod��czonymi za pomoc� Bluetooth, ��cza na podczerwie� (IR) lub kabla.

%package irmc-bluetooth
Summary:	Bluetooth support for the IrMC plugin for MultiSync
Summary(pl):	Wsparcie dla Bluetooth dla wtyczki MultiSynca do IrMC
Group:		X11/Applications
Requires:	%{name}-irmc = %{version}

%description irmc-bluetooth
This package adds Bluetooth support to the IrMC (mobile device) plugin
for MultiSync.

%description irmc-bluetooth -l pl
Ten pakiet dodaje wsparcie dla Bluetooth do wtyczki MultiSynca do IrMC
(dla urz�dze� przeno�nych). 

%package ldap
Summary:	A LDAP plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do LDAP
Group:		X11/Applications
Requires:	%{name} = %{version}

%description ldap
This is a MultiSync plugin which synchronizes LDAP data

%description ldap -l pl
Jest to wtyczka MultiSynca do synchronizacji danych LDAP.

%package syncml
Summary:	A SyncML plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do SynCML
Group:		X11/Applications
Requires:	%{name} = %{version}

%description syncml
This is a SyncML 1.1 plugin for the MultiSync synchronization engine.
It allows synchronization of SyncML-enabled devices, such as the
SonyEricsson P800, as well as remote MultiSync to MultiSync
synchronization over the Internet.

%description syncml -l pl
Wtyczka do SyncML 1.1 dla mechanizmu synchronizacji MultiSync.
Umo�liwia ona synchronizacj� urz�dze� z w��czonym SyncML, takich jak
SonyEricsson P800, a tak�e zdaln� synchronizacj� pomi�dzy MultiSyncami
poprzez Internet.

%package opie
Summary:	Opie/Zaurus Synchronization Plugin for MultiSync
Group:		X11/Applications
Requires:	%{name} = %{version}

%description opie
Opie/Zaurus Synchronization Plugin for MultiSync.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

# ugly hack to build evolution plugin...
sed 's#/bin/sh#/bin/bash#' < plugins/evolution_sync/configure > configure.evolution
mv configure.evolution plugins/evolution_sync/configure
chmod 755 plugins/evolution_sync/configure

# libnvpair library
# pi_socket library
SKIP_PLUGINS="-e csa_plugin -e palm_sync"
export SKIP_PLUGINS

# build plugins
for dir in $(ls plugins/ | grep -v $SKIP_PLUGINS); do
	cd plugins/$dir
	%configure
	%{__make}
	cd -
done

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

SKIP_PLUGINS="-e csa_plugin -e palm_sync"
export SKIP_PLUGINS

# build plugins
for dir in $(ls plugins/ | grep -v $SKIP_PLUGINS); do
	cd plugins/$dir
	%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
	cd -
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}

%files evolution
%defattr(644,root,root,755)
%{_libdir}/%{name}/libevolution_sync.so*

%files backup
%defattr(644,root,root,755)
%{_libdir}/%{name}/libbackup_plugin.so*

%files irmc-bluetooth
%defattr(644,root,root,755)
%{_libdir}/%{name}/libirmc_bluetooth.so*

%files irmc
%defattr(644,root,root,755)
%{_libdir}/%{name}/libirmc_sync.so*

%files ldap
%defattr(644,root,root,755)
%{_libdir}/%{name}/libldap_plugin.so*

%files syncml
%defattr(644,root,root,755)
%{_libdir}/%{name}/libsyncml_plugin.so*

%files opie
%defattr(644,root,root,755)
%{_libdir}/%{name}/libopie_sync.so*
