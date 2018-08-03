# -*- rpm-spec -*-
# XCP-ng: release suffix for 'extras' section
%if "%{?xcp_ng_section}" == "extras"
%define rel_suffix .extras
%endif

Summary: Command-line tools for manipulating and streaming .vhd format files
Name:    vhd-tool
Version: 0.20.0
Release: 4.2.xcp%{?dist}%{?rel_suffix}
License: LGPL+linking exception
URL:  https://github.com/xapi-project/vhd-tool
Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/%{name}/archive?at=v%{version}&format=tar.gz&prefix=%{name}-%{version}#/%{name}-%{version}.tar.gz
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/vhd-tool/archive?at=v0.20.0&format=tar.gz&prefix=vhd-tool-0.20.0#/vhd-tool-0.20.0.tar.gz) = 76a543f11ea62aa2e56c4ba55c2bb898f121d2b2
Source1: vhd-tool-sparse_dd-conf
BuildRequires: ocaml-camlp4-devel
BuildRequires: xs-opam-repo
BuildRequires: ocaml-xcp-idl-devel
BuildRequires: ocaml-tapctl-devel
BuildRequires: openssl-devel

# XCP-ng patches
%if "%{?xcp_ng_section}" == "extras"
Patch1000: vhd-tool-0.20.0-remove_o_direct.XCP-ng.patch
%endif
Patch1001: vhd-tool-0.20.0-wait-for-actual-data-before-retrying-sendfile.XCP-ng.patch

%description
Simple command-line tools for manipulating and streaming .vhd format file.

%prep
%autosetup -p1
cp %{SOURCE1} vhd-tool-sparse_dd-conf

%build
eval $(opam config env --root=/usr/lib/opamroot)
make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}/xapi
mkdir -p %{buildroot}/etc
install -m 755 _build/install/default/bin/sparse_dd     %{buildroot}%{_libexecdir}/xapi/sparse_dd
install -m 755 _build/install/default/bin/vhd-tool      %{buildroot}%{_bindir}/vhd-tool
install -m 644 cli/sparse_dd.conf                       %{buildroot}/etc/sparse_dd.conf
install -m 755 _build/install/default/bin/get_vhd_vsize %{buildroot}%{_libexecdir}/xapi/get_vhd_vsize

%files
%{_bindir}/vhd-tool
/etc/sparse_dd.conf
%{_libexecdir}/xapi/sparse_dd
%{_libexecdir}/xapi/get_vhd_vsize

%changelog
* Thu Aug 02 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.20.0-4.2.xcp
- Try better fix for EAGAIN exception, with upstream advice

* Wed Aug 01 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 0.20.0-4.1.xcp
- Rebuild with patched ocaml-vhd to fix large VDI import error
- Cf. https://bugs.xenserver.org/browse/XSO-868

* Tue Jul 31 2018 Nicolas Raynaud <nraynaud@gmail.com> - 0.20.0-4
- Fix VHD export regression due to VDI I/O error on EAGAIN exception

* Tue Jul 31 2018 Nicolas Raynaud <nraynaud@gmail.com> - 0.20.0-3
- set unbuffered to false in 'extras' build (for ZFS support)

* Thu Mar 22 2018 Marcello Seri <marcello.seri@citrix.com> - 0.20.0-1
- Catch EAGAIN from sendfile and retry

* Thu Feb 22 2018 Christian Lindig <christian.lindig@citrix.com> - 0.19.0-1
- Remove redundant pipe definition of (|>)

* Wed Jan 31 2018 Christian Lindig <christian.lindig@citrix.com> - 0.18.0-1
- CA-280242: Open destination VDI O_DIRECT (as well as source).

* Fri Jan 26 2018 Christian Lindig <christian.lindig@citrix.com> - 0.17.0-1
- Updates to make xs-opam build on next

* Thu Jan 11 2018 Christian Lindig <christian.lindig@citrix.com> - 0.16.0-1
- CP-24605: Renamed library after porting to jbuilder.

* Fri Oct 13 2017 Rob Hoes <rob.hoes@citrix.com> - 0.15.0-1
- Temporarily add missing is_tls field to nbd channel record

* Fri Sep 22 2017 Rob Hoes <rob.hoes@citrix.com> - 0.14.0-1
- Ported build from oasis to jbuilder.

* Thu Sep 21 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 0.13.0-2
- Build simplification due to porting to jbuilder.

* Fri Jun 16 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.13.0-1
- Sync opam file with xs-opam

* Thu Jun 01 2017 Rob Hoes <rob.hoes@citrix.com> - 0.12.0-1
- Makefile: fix conditional syntax
- make build: don't try to create sparse_dd man page
- configure.ml: fix generated install file

* Fri May 12 2017 Rob Hoes <rob.hoes@citrix.com> - 0.11.0-1
- CA-229038: Allow upload of data that is not an integer number of sectors
- CA-229038: Make zero size an error

* Mon Mar 13 2017 Marcello Seri <marcello.seri@citrix.com> - 0.10.0-2
- Update OCaml dependencies and build/install script after xs-opam-repo split

* Thu Mar 09 2017 Rob Hoes <rob.hoes@citrix.com> - 0.10.0-1
- Fix oasis for PPX world
- Update to PPX-based NBD library
- Fix: multiply write offset by 512 (sector size)

* Wed Feb 22 2017 Rob Hoes <rob.hoes@citrix.com> - 0.9.1-1
- CP-20761 Remove use of camlp4 lwt syntax extension

* Thu Jan 19 2017 Rob Hoes <rob.hoes@citrix.com> - 0.9.0-1
- CA-236851: Experimental: Aggresively close VHDs after reading the BAT

* Tue Jan 10 2017 Rob Hoes <rob.hoes@citrix.com> - 0.8.1-1
- git: Add metadata to the result of `git archive`

* Fri Jun 24 2016 Christian Lindig <christian.lindig@citrix.com> 0.8.0-3
- This release is built against an updated ocaml-vhd 0.7.3-4 library that
  corrects a bug handling lseek(2) SEEK_DATA, SEEK_HOLE.

* Thu Jun 23 2016 Thomas Sanders <thomas.sanders@citrix.com> - 0.8.0
- BuildRequires oasis, to do oasis autogeneration at build-time.
- Update to 0.8.0

* Thu Oct 1 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.7.5-2
- Add get_vhd_vsize

* Fri Jun 6 2014 Jonathan Ludlam <jonathan.ludlam@citrix.com> - 0.7.5-1
- Update to 0.7.5

* Wed Apr 9 2014 Euan Harris <euan.harris@citrix.com> - 0.7.4-1
- Update to 0.7.4 - fix handling of tar file prefixes

* Wed Apr 2 2014 Euan Harris <euan.harris@citrix.com> - 0.7.3-1
- Update to 0.7.3

* Thu Nov 21 2013 David Scott <dave.scott@eu.citrix.com> - 0.6.4-1
- Update to 0.6.4

* Fri Oct 25 2013 David Scott <dave.scott@eu.citrix.com> - 0.6.1-1
- Update to 0.6.1

* Wed Oct 02 2013 David Scott <dave.scott@eu.citrix.com> - 0.6.0-1
- Update to 0.6.0

* Fri Sep 27 2013 David Scott <dave.scott@eu.citrix.com> - 0.5.1-1
- Update to 0.5.1

* Mon Sep 23 2013 David Scott <dave.scott@eu.citrix.com> - 0.5.0-1
- Initial package
