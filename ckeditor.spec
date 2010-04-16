# TODO
# - separate packages for plugins?
# - uicolor for example bundles yui framework (30% of the whole plugins dir)
Summary:	The text editor for Internet
Summary(pl.UTF-8):	Edytor tekstowy dla Internetu
Name:		ckeditor
Version:	3.2.1
Release:	1
License:	LGPL v2.1+ / GPL v2+ / MPL
Group:		Applications/WWW
Source0:	http://download.cksource.com/CKEditor/CKEditor/CKEditor%20%{version}/%{name}_%{version}.tar.gz
# Source0-md5:	793ad3d32b15f88b71db72573710a926
URL:		http://www.ckeditor.com/
Source1:	find-lang.sh
Source2:	apache.conf
Source3:	lighttpd.conf
BuildRequires:	lynx
BuildRequires:	rpmbuild(macros) > 1.268
BuildRequires:	sed >= 4.0
Requires:	webapps
Requires:	webserver
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

%package -n php-%{name}
Summary:	PHP class to create editors instances
Group:		Development/Languages/PHP

%description -n php-%{name}
CKEditor class that can be used to create editor instances in PHP
pages on server side.

%prep
%setup -qc
mkdir config
mv ckeditor/* .
mv ckeditor/.htaccess config/htaccess
rmdir ckeditor

# force php5 only
rm ckeditor_php4.php
mv ckeditor_php5.php ckeditor.php

# collect source for reference
mv *_source.js _source

rm lang/_translationstatus.txt

# used only in samples
mv lang/_languages.js _samples
%{__sed} -i -e 's,\.\./lang/_languages\.js,_languages.js,' _samples/ui_languages.html

# undos the files
%{__sed} -i -e 's,\r$,,' ckeditor*
find '(' -name '*.js' -o -name '*.css' -o -name '*.txt' -o -name '*.html' -o -name '*.php' ')' -print0 | xargs -0 sed -i -e 's,\r$,,'

%build
lynx -dump -nolist -width 1024 CHANGES.html | sed -e '/___/,$d' > CHANGES

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}

cp -a ckeditor.js config.js contents.css $RPM_BUILD_ROOT%{_appdir}
cp -a plugins skins themes lang $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{php_data_dir}
cp -a ckeditor.php $RPM_BUILD_ROOT%{php_data_dir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a _samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%find_lang %{name}.lang

# always include
%{__sed} -i -e '/en\.js/d' %{name}.lang

# already listed by plugin dir
%{__sed} -i -e '/plugins/d' %{name}.lang

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
%doc CHANGES
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/*.js
%{_appdir}/lang/en.js
%{_appdir}/*.css
%dir %{_appdir}/themes
%{_appdir}/themes/default

%dir %{_appdir}/skins
%{_appdir}/skins/kama
%{_appdir}/skins/office2003
%{_appdir}/skins/v2

%dir %{_appdir}/plugins
%{_appdir}/plugins/a11yhelp
%{_appdir}/plugins/about
%{_appdir}/plugins/clipboard
%{_appdir}/plugins/colordialog
%{_appdir}/plugins/dialog
%{_appdir}/plugins/div
%{_appdir}/plugins/find
%{_appdir}/plugins/flash
%{_appdir}/plugins/forms
%{_appdir}/plugins/iframedialog
%{_appdir}/plugins/image
%{_appdir}/plugins/link
%{_appdir}/plugins/pagebreak
%{_appdir}/plugins/pastefromword
%{_appdir}/plugins/pastetext
%{_appdir}/plugins/scayt
%{_appdir}/plugins/showblocks
%{_appdir}/plugins/smiley
%{_appdir}/plugins/specialchar
%{_appdir}/plugins/styles
%{_appdir}/plugins/table
%{_appdir}/plugins/tabletools
%{_appdir}/plugins/templates
%{_appdir}/plugins/uicolor
%{_appdir}/plugins/wsc

%{_examplesdir}/%{name}-%{version}

%files -n php-%{name}
%defattr(644,root,root,755)
%{php_data_dir}/ckeditor.php
