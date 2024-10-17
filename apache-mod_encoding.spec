#Module-Specific definitions
%define snapshot 20040616
%define mod_name mod_encoding
%define mod_conf 44_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.0.%{snapshot}
Release:	10
Group:		System/Servers
License:	GPL
URL:		https://webdav.todo.gr.jp/
Source0: 	mod_encoding-0.0.20021209.tar.bz2
Source1:	%{mod_conf}
Source2:	http://webdav.todo.gr.jp/download/experimental/mod_encoding.c.apache2.%{snapshot}
Patch0:		mod_encoding.c.apache2.20040616-apache220.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1

%description
Mod Encoding is an Apache module for non-ascii filename interoperability

This module improves non-ascii filename interoperability of apache
(and mod_dav).

%prep

%setup -q -n mod_encoding-20021209

cp %{SOURCE1} %{mod_conf}
cp %{SOURCE2} %{mod_name}.c

%patch0 -p0 -b .apache220

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

cd lib
[ -r iconv.h ] && rm -f iconv.h
rm -f configure
autoreconf -fis
%configure --enable-shared=no
%make CFLAGS="%{optflags} -fPIC"
ln -s -f  iconv.h.replace iconv.h
cd -

%{_bindir}/apxs -c -I$PWD/lib -L$PWD/lib/ -liconv_hook %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean

%files
%doc AUTHORS ChangeLog README COPYING
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-9mdv2012.0
+ Revision: 772623
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-8
+ Revision: 678309
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-7mdv2011.0
+ Revision: 587967
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-6mdv2010.1
+ Revision: 516095
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-5mdv2010.0
+ Revision: 406928
- fix build
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-4mdv2009.1
+ Revision: 325698
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-3mdv2009.0
+ Revision: 234941
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-2mdv2009.0
+ Revision: 215574
- fix rebuild

* Fri May 16 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20040616-1mdv2009.0
+ Revision: 208086
- use their latest snapshot 20040616 (thanks Adam Williamson)
- rediffed P0

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20021209-7mdv2008.1
+ Revision: 181722
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.0.20021209-6mdv2008.1
+ Revision: 170719
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20021209-5mdv2008.0
+ Revision: 82568
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.0.20021209-4mdv2007.1
+ Revision: 140671
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20021209-3mdv2007.0
+ Revision: 79414
- Import apache-mod_encoding

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20021209-3mdv2007.0
- rebuild

* Sun Apr 16 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20021209-2mdk
- fix build against apache-2.2.0 (P0)

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.0.20021209-1mdk
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.0.20021209-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.0.20021209-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.0.20021209-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.0.20021209-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.0.20021209-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.0.20021209-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.0.20021209-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.0.20021209-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.0.20021209-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.0.20021209-1mdk
- built for apache 2.0.49

