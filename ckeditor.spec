# NOTES:
# - check for new releases here: http://ckeditor.com/download/releases
Summary:	The text editor for Internet
Summary(pl.UTF-8):	Edytor tekstowy dla Internetu
Name:		ckeditor
Version:	4.3.2
Release:	1
License:	LGPL v2.1+ / GPL v2+ / MPL
Group:		Applications/WWW
Source0:	http://download.cksource.com/CKEditor/CKEditor/CKEditor%20%{version}/%{name}_%{version}_full.tar.gz
# Source0-md5:	650ccbfbd51153261dc9be9bdc9ef5c0
# http://ckeditor.com/addon/kama - The default CKEditor 3 skin ported to CKEditor 4.
Source1:	http://download.ckeditor.com/kama/releases/kama_%{version}.zip
# Source1-md5:	a57baab966aa228b85927cc07a7f95a1
URL:		http://www.ckeditor.com/
Source2:	apache.conf
Source3:	lighttpd.conf
Source4:	find-lang.sh
BuildRequires:	rpmbuild(macros) >= 1.553
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

%define		find_lang	sh %{SOURCE4}

%description
This HTML text editor brings to the web many of the powerful
functionalities of desktop editors like MS Word. It's lightweight and
doesn't require any kind of installation on the client computer.

%description -l pl.UTF-8
Ten edytor tekstu HTML udostępnia stronom WWW wiele potężnych funkcji
edytorów biurowych, takich jak MS Word. Jest lekki i nie wymaga żadnej
inicjalizacji na komputerze klienckim.

%prep
%setup -qc -a1
mv ckeditor/* .
mv kama skins

find -name _translationstatus.txt -print -delete

# undos the files
%undos -f js,css,txt,html,md

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}

cp -a ckeditor.js styles.js contents.css $RPM_BUILD_ROOT%{_appdir}
cp -a adapters plugins skins lang $RPM_BUILD_ROOT%{_appdir}
ln -s kama $RPM_BUILD_ROOT%{_appdir}/skins/v2

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p config.js $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_sysconfdir}/config.js $RPM_BUILD_ROOT%{_appdir}

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
%doc README.md CHANGES.md LICENSE.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.js
%dir %{_appdir}
%{_appdir}/*.js
%{_appdir}/lang/en.js
%{_appdir}/*.css

%dir %{_appdir}/adapters
%{_appdir}/adapters/jquery.js

%dir %{_appdir}/skins
%{_appdir}/skins/moono

# kama skin, and compat link to it
%{_appdir}/skins/kama
%{_appdir}/skins/v2

%dir %{_appdir}/plugins
%{_appdir}/plugins/icons.png
%{_appdir}/plugins/icons_hidpi.png

%{_appdir}/plugins/a11yhelp
%{_appdir}/plugins/about
%{_appdir}/plugins/clipboard
%{_appdir}/plugins/colordialog
%{_appdir}/plugins/dialog
%{_appdir}/plugins/div
%{_appdir}/plugins/fakeobjects
%{_appdir}/plugins/find
%{_appdir}/plugins/flash
%{_appdir}/plugins/forms
%{_appdir}/plugins/iframe
%{_appdir}/plugins/image
%{_appdir}/plugins/link
%{_appdir}/plugins/liststyle
%{_appdir}/plugins/magicline
%{_appdir}/plugins/pagebreak
%{_appdir}/plugins/pastefromword
%{_appdir}/plugins/preview
%{_appdir}/plugins/scayt
%{_appdir}/plugins/showblocks
%{_appdir}/plugins/smiley
%{_appdir}/plugins/specialchar
%{_appdir}/plugins/table
%{_appdir}/plugins/tabletools
%{_appdir}/plugins/templates
%{_appdir}/plugins/wsc

%{_examplesdir}/%{name}-%{version}
