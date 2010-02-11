# TODO
# - handle plugin languages
Summary:	The text editor for Internet
Summary(pl.UTF-8):	Edytor tekstowy dla Internetu
Name:		ckeditor
Version:	3.1
Release:	0.16
License:	LGPL v2.1
Group:		Applications/WWW
Source0:	http://download.cksource.com/CKEditor/CKEditor/CKEditor%20%{version}/%{name}_%{version}.tar.gz
# Source0-md5:	9c4a9e54f756e24c6aac24888c4599d0
URL:		http://www.ckeditor.com/
Source1:	find-lang.sh
BuildRequires:	rpmbuild(macros) > 1.268
BuildRequires:	sed >= 4.0
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{name}

%define		find_lang	sh %{SOURCE1}

%description
This HTML text editor brings to the web many of the powerful
functionalities of desktop editors like MS Word. It's lightweight and
doesn't require any kind of installation on the client computer.

%description -l pl.UTF-8
Ten edytor tekstu HTML udostępnia stronom WWW wiele potężnych funkcji
edytorów biurowych, takich jak MS Word. Jest lekki i nie wymaga żadnej
inicjalizacji na komputerze klienckim.

%prep
%setup -qc
mkdir config
mv ckeditor/* .
mv ckeditor/.htaccess config/htaccess
rmdir ckeditor
mv _samples samples

# force php5 only
rm ckeditor_php4.php
mv ckeditor_php5.php ckeditor.php

find -name _source | xargs rm -rf
rm -f *_source.js

rm lang/_translationstatus.txt

# undos the files
%{__sed} -i -e 's,\r$,,' ckeditor*
find '(' -name '*.js' -o -name '*.css' -o -name '*.txt' -o -name '*.html' -o -name '*.php' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

# apache1/apache2 conf
cat > config/apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# lighttpd conf
cat > config/lighttpd.conf <<'EOF'
alias.url += (
	"/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}

cp -a ckeditor.js $RPM_BUILD_ROOT%{_appdir}
cp -a plugins skins themes lang $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a config/apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a config/apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a config/lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%find_lang %{name}.lang

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/*.js
%{_appdir}/skins
%{_appdir}/themes
%{_appdir}/plugins
%{_appdir}/lang/_languages.js

%{_examplesdir}/%{name}-%{version}
