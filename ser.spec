%define _disable_ld_no_undefined 1

%define EXCLUDED_MODULES	mysql jabber auth_radius group_radius uri_radius avp_radius postgress snmp cpl cpl-c ext extcmd
%define JABBER_MODULES		jabber
%define MYSQL_MODULES		mysql
%define RADIUS_MODULES		auth_radius group_radius uri_radius avp_radius
%define RADIUS_MOD_PATH		modules/auth_radius modules/group_radius modules/uri_radius modules/avp_radius

Summary:	SIP Express Router, very fast and flexible SIP Proxy
Name:		ser
Version:	0.9.6
Release:	14
License:	GPLv2+
Group:		System/Servers
URL:		https://iptel.org/ser
Source0:	http://iptel.org/ser/stable/%{name}-%{version}_src.tar.bz2
Patch1:		ser-0.8.14-errno.diff
Patch2:		ser-0.9.6-str-fmt.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	bison
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	radiusclient-ng-devel
BuildRequires:	libxml2-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Ser or SIP Express Router is a very fast and flexible SIP (RFC3621)
proxy server. Written entirely in C, ser can handle thousands calls
per second even on low-budget hardware. A C Shell like scripting language
provides full control over the server's behaviour. It's modular
architecture allows only required functionality to be loaded.
Currently the following modules are available: digest authentication,
CPL scripts, instant messaging, MySQL support, a presence agent, radius
authentication, record routing, an SMS gateway, a jabber gateway, a 
transaction module, registrar and user location.

%package	mysql
Summary:	MySQL connectivity for the SIP Express Router
Group:		System/Servers
Requires:	ser = %{version}

%description	mysql
The ser-mysql package contains MySQL database connectivity that you
need to use digest authentication module or persistent user location
entries.

%package	jabber
Summary:	SIP jabber message translation support for the SIP Express Router
Group:		System/Servers
Requires:	ser = %{version}

%description	jabber
The ser-jabber package contains a sip to jabber message translator.

%package	radius
Summary:	Ser radius authentication, group and uri check modules
Group:		System/Servers
Requires:	ser = %{version}

%description	radius
The ser-radius package contains modules for radius authentication, group
membership and uri checking.

%prep

%setup -q
%patch1 -p0
%patch2 -p0 -b .str

# lib64 fixes
find -type f | xargs perl -pi -e 's|/usr/lib|%{_libdir}|g'
find -type f | xargs perl -pi -e 's|\-L\$\(LOCALBASE\)/lib|\-L\$\(LOCALBASE\)/%{_lib}|g'

%build
make CFLAGS="%{optflags} -fPIC" all skip_modules="%EXCLUDED_MODULES" cfg-target=%{_sysconfdir}/ser/ modules-dir=%{_lib}/ser/modules/
make CFLAGS="%{optflags} -fPIC" modules modules="modules/%MYSQL_MODULES" cfg-target=%{_sysconfdir}/ser/ modules-dir=%{_lib}/ser/modules/
make CFLAGS="%{optflags} -fPIC" modules modules="modules/%JABBER_MODULES" cfg-target=%{_sysconfdir}/ser/ modules-dir=%{_lib}/ser/modules/
make CFLAGS="%{optflags} -fPIC" modules modules="%RADIUS_MOD_PATH" cfg-target=%{_sysconfdir}/ser/ modules-dir=%{_lib}/ser/modules/
make CFLAGS="%{optflags} -fPIC" modules modules="modules/pa" cfg-target=%{_sysconfdir}/ser/ modules-dir=%{_lib}/ser/modules/

%install
[ "%{buildroot}" != "/" ] && rm -rf "%{buildroot}"

make install skip_modules="%EXCLUDED_MODULES" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

make install-modules modules="modules/%MYSQL_MODULES" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

make install-modules modules="modules/%JABBER_MODULES" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

make install-doc modules="modules/%JABBER_MODULES" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

make install-modules modules="%RADIUS_MOD_PATH" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

make install-doc modules="%RADIUS_MOD_PATH" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

make install-modules modules="modules/pa" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

make install-doc modules="modules/pa" \
    basedir=%{buildroot} \
    prefix=%{_prefix} \
    cfg-prefix=%{buildroot} \
    cfg-target=%{_sysconfdir}/ser/ \
    modules-dir=%{_lib}/ser/modules/ \
    doc-prefix=$PWD \
    doc-dir=installed_docs

mkdir -p %{buildroot}%{_initrddir}
install -m755 rpm/ser.init %{buildroot}%{_initrddir}/ser

%post
%_post_service ser

%preun
%_preun_service ser

%clean
[ "%{buildroot}" != "/" ] && rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%doc installed_docs/AUTHORS installed_docs/NEWS installed_docs/INSTALL installed_docs/README installed_docs/README-MODULES
%doc installed_docs/README.acc installed_docs/README.auth installed_docs/README.auth_db installed_docs/README.auth_diameter
%doc installed_docs/README.dbtext installed_docs/README.domain installed_docs/README.enum installed_docs/README.exec
%doc installed_docs/README.group installed_docs/README.mangler installed_docs/README.maxfwd installed_docs/README.msilo
%doc installed_docs/README.nathelper installed_docs/README.pa installed_docs/README.pdt installed_docs/README.permissions
%doc installed_docs/README.pike installed_docs/README.print installed_docs/README.registrar installed_docs/README.rr
%doc installed_docs/README.sl installed_docs/README.sms installed_docs/README.textops installed_docs/README.tm installed_docs/README.uri
%doc installed_docs/README.usrloc installed_docs/README.xlog
%attr(0755,root,root) %{_initrddir}/ser
%dir %{_sysconfdir}/ser
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ser/*
%dir %{_libdir}/ser
%dir %{_libdir}/ser/modules
%{_libdir}/ser/modules/acc.so
%{_libdir}/ser/modules/auth.so
%{_libdir}/ser/modules/auth_db.so
%{_libdir}/ser/modules/auth_diameter.so
%{_libdir}/ser/modules/dbtext.so
%{_libdir}/ser/modules/domain.so
%{_libdir}/ser/modules/enum.so
%{_libdir}/ser/modules/exec.so
%{_libdir}/ser/modules/group.so
%{_libdir}/ser/modules/mangler.so
%{_libdir}/ser/modules/maxfwd.so
%{_libdir}/ser/modules/msilo.so
%{_libdir}/ser/modules/nathelper.so
%{_libdir}/ser/modules/pa.so
%{_libdir}/ser/modules/pdt.so
%{_libdir}/ser/modules/permissions.so
%{_libdir}/ser/modules/pike.so
%{_libdir}/ser/modules/print.so
%{_libdir}/ser/modules/registrar.so
%{_libdir}/ser/modules/rr.so
%{_libdir}/ser/modules/sl.so
%{_libdir}/ser/modules/sms.so
%{_libdir}/ser/modules/textops.so
%{_libdir}/ser/modules/tm.so
%{_libdir}/ser/modules/uri.so
%{_libdir}/ser/modules/usrloc.so
%{_libdir}/ser/modules/xlog.so
%{_libdir}/ser/modules/avp.so
%{_libdir}/ser/modules/avp_db.so
%{_libdir}/ser/modules/avpops.so
%{_libdir}/ser/modules/dispatcher.so
%{_libdir}/ser/modules/diversion.so
%{_libdir}/ser/modules/flatstore.so
%{_libdir}/ser/modules/gflags.so
%{_libdir}/ser/modules/mediaproxy.so
%{_libdir}/ser/modules/options.so
%{_libdir}/ser/modules/speeddial.so
%{_libdir}/ser/modules/uri_db.so
%{_sbindir}/gen_ha1
%{_sbindir}/ser
%{_sbindir}/serunix
%{_sbindir}/serctl
%{_mandir}/man5/*
%{_mandir}/man8/*

%files mysql
%defattr(-,root,root)
%{_libdir}/ser/modules/mysql.so
%{_sbindir}/ser_mysql.sh

%files jabber
%defattr(-,root,root)
%doc installed_docs/README.jabber
%{_libdir}/ser/modules/jabber.so

%files radius
%defattr(-,root,root)
%doc installed_docs/README.auth_radius installed_docs/README.group_radius installed_docs/README.uri_radius
%doc installed_docs/README.avp_radius
%{_libdir}/ser/modules/auth_radius.so
%{_libdir}/ser/modules/group_radius.so
%{_libdir}/ser/modules/uri_radius.so
%{_libdir}/ser/modules/avp_radius.so




%changelog
* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-12mdv2011.0
+ Revision: 645879
- relink against libmysqlclient.so.18

* Sun Jan 02 2011 Funda Wang <fwang@mandriva.org> 0.9.6-11mdv2011.0
+ Revision: 627606
- fix str fmt

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt against mysql-5.5.8 libs, again
    - rebuilt against mysql-5.5.8 libs
    - rebuild
    - use lowercase mysql-devel

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-6mdv2009.1
+ Revision: 311318
- rebuilt against mysql-5.1.30 libs

* Sat Aug 02 2008 Thierry Vignaud <tv@mandriva.org> 0.9.6-5mdv2009.0
+ Revision: 260626
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 0.9.6-4mdv2009.0
+ Revision: 252333
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Dec 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.9.6-2mdv2008.1
+ Revision: 138593
- rebuild for new expat (ser-jabber depends on libexpat.so.0)
- new license policy

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Wed Jan 03 2007 Stefan van der Eijk <stefan@mandriva.org> 0.9.6-1mdv2007.0
+ Revision: 103845
- Import ser

* Thu Feb 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.9.6-1mdk
- 0.9.6
- drop P0 as another approach is implemented upstream

* Mon Apr 25 2005 Oden Eriksson <oeriksson@mandriva.com> 0.9.0-1mdk
- 0.9.0 (x86_64 fixes)
- build against new radiusclient-ng libs (P0)
- added a missing errno header incusion (P1)

* Thu Feb 10 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.8.12-2mdk
- rebuilt against new mysql libs
- misc spec file fixes

* Mon Jun 07 2004 Stefan van der Eijk <stefan@mandrake.org> 0.8.12-1mdk
- Mandrake adaptions

