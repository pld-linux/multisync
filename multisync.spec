
#
# TODO:
# - devel subpackage
# - -avoid-version patch for plugins and send it to authors
# - review pl translations
#

Summary:	PIM data synchronization program
Summary(pl):	Program do synchronizacji danych
Name:		multisync
Version:	0.82
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	499aaa3d41e33276ab162db1d1912a16
Patch0:		%{name}-install.patch
Patch1:		%{name}-top.patch
URL:		http://multisync.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bluez-libs-devel >= 2.6
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
Program do synchronizacji kalendarzy, ksi±¿ek adresowych i innych
danych osobistych pomiêdzy ró¿nymi programami w ramach jednego
komputera, jak te¿ pomiêdzy ró¿nymi komputerami i urz±dzeniami
przeno¶nymi. Aktualnie posiada wtyczki (w osobnych pakietach) do:
Evolution Ximiana, przeno¶nych urz±dzeñ IrMC, SyncML i kopii
zapasowych.

%package evolution
Summary:	A Ximian Evolution plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do Evolution Ximiana
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description evolution
This is a plugin to enable synchronization of Ximian Evolution data
using MultiSync.

%description evolution -l pl
Jest to wtyczka umo¿liwiaj±ca synchronizacjê Evolution Ximiana za
pomoc± MultiSync.

%package backup
Summary:	A backup plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do kopii zapasowych
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description backup
This is a MultiSync plugin which backs up your calendar/phonebook/etc.
data.

%description backup -l pl
Jest to wtyczka MultiSynca tworz±ca kopie zapasowe kalendarza/ksi±¿ki
adresowej/itp.

%package irmc
Summary:	An IrMC (SonyEricsson T39/T68i/T610, Siemens S55) plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do IrMC (SonyEricsson T39/T68i/T610, Siemens S55)
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description irmc
This is a MultiSync plugin for IrMC mobile clients (cell phones
such as SonyEricsson T39/T68/T610 and Siemens S55) connected via
Bluetooth, IR or cable.

%description irmc -l pl
Jest to wtyczka MultiSynca do wspó³pracy z przeno¶nymi klientami IrMC
(telefony komórkowe takie jak SonyEricsson T39/T68/T610 i Siemens S55)
pod³±czonymi za pomoc± Bluetooth, ³±cza na podczerwieñ (IR) lub kabla.

%package irmc-bluetooth
Summary:	Bluetooth support for the IrMC plugin for MultiSync
Summary(pl):	Wsparcie dla Bluetooth dla wtyczki MultiSynca do IrMC
Group:		X11/Applications
Requires:	%{name}-irmc = %{version}-%{release}

%description irmc-bluetooth
This package adds Bluetooth support to the IrMC (mobile device) plugin
for MultiSync.

%description irmc-bluetooth -l pl
Ten pakiet dodaje wsparcie dla Bluetooth do wtyczki MultiSynca do IrMC
(dla urz±dzeñ przeno¶nych). 

%package ldap
Summary:	A LDAP plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do LDAP
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description ldap
This is a MultiSync plugin which synchronizes LDAP data

%description ldap -l pl
Jest to wtyczka MultiSynca do synchronizacji danych LDAP.

%package syncml
Summary:	A SyncML plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do SynCML
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description syncml
This is a SyncML 1.1 plugin for the MultiSync synchronization engine.
It allows synchronization of SyncML-enabled devices, such as the
SonyEricsson P800, as well as remote MultiSync to MultiSync
synchronization over the Internet.

%description syncml -l pl
Wtyczka do SyncML 1.1 dla mechanizmu synchronizacji MultiSync.
Umo¿liwia ona synchronizacjê urz±dzeñ z w³±czonym SyncML, takich jak
SonyEricsson P800, a tak¿e zdaln± synchronizacjê pomiêdzy MultiSyncami
poprzez Internet.

%package opie
Summary:	Opie/Zaurus synchronization plugin for MultiSync
Summary(pl):	Wtyczka MultiSynca do synchronizacji z Opie/Zaurus
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description opie
Opie/Zaurus synchronization plugin for MultiSync.

%description opie -l pl
Wtyczka MultiSynca do synchronizacji z Opie/Zaurus.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

# libnvpair library
# pi_socket library
SKIP_PLUGINS="-e csa_plugin -e palm_sync"
export SKIP_PLUGINS

# build plugins
for dir in $(ls plugins/ | grep -v $SKIP_PLUGINS); do
    cd plugins/$dir
    %{__libtoolize}
    cp ../../libtool .
    cp ../../ltmain.sh .   # due to aux dir this scripts are copied into ../.., where to fix it?
    %{__aclocal}
    %{__autoconf}
    %{__automake}
    sed -i 's#/bin/sh#/bin/bash#' configure # ugly hack to avoid bashism :-\
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
	%{__make} -C plugins/$dir install \
		DESTDIR=$RPM_BUILD_ROOT
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%{_datadir}/%{name}

%files evolution
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libevolution_sync.so*

%files backup
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libbackup_plugin.so*

%files irmc-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libirmc_bluetooth.so*

%files irmc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libirmc_sync.so*

%files ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libldap_plugin.so*

%files syncml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libsyncml_plugin.so*

%files opie
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/libopie_sync.so*
