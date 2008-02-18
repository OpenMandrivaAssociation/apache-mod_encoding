#Module-Specific definitions
%define snapshot 20021209
%define mod_name mod_encoding
%define mod_conf 44_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.0.%{snapshot}
Release:	%mkrel 6
Group:		System/Servers
License:	GPL
URL:		http://webdav.todo.gr.jp/
Source0: 	mod_encoding-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
# (fc) 0.0.20021209-1mdk apache2 port
Patch0:		mod_mod_encoding-0.0.20021209-apache220.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mod Encoding is an Apache module for non-ascii filename interoperability

This module improves non-ascii filename interoperability of apache
(and mod_dav).

%prep

%setup -q -n mod_encoding-%{snapshot}
%patch0 -p0 -b .apache220

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

cd lib
[ -r iconv.h ] && rm -f iconv.h
%configure --enable-shared=no
%make CFLAGS="%{optflags} -fPIC"
ln -s -f  iconv.h.replace iconv.h
cd -

%{_sbindir}/apxs -c -I$PWD/lib -L$PWD/lib/ -liconv_hook %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


