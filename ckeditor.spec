# NOTES:
# - check for new releases here: http://ckeditor.com/download/releases
Summary:	The text editor for Internet
Summary(pl.UTF-8):	Edytor tekstowy dla Internetu
Name:		ckeditor
Version:	4.3.1
Release:	1
License:	LGPL v2.1+ / GPL v2+ / MPL
Group:		Applications/WWW
Source0:	http://download.cksource.com/CKEditor/CKEditor/CKEditor%20%{version}/%{name}_%{version}_full.tar.gz
# Source0-md5:	42c63f02f77daa21e9b5447f170bfa0f
URL:		http://www.ckeditor.com/
Source1:	find-lang.sh
Source2:	apache.conf
Source3:	lighttpd.conf
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
mv ckeditor/* .

find -name _translationstatus.txt -print -delete

# undos the files
%undos -f js,css,txt,html,md

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}

cp -a ckeditor.js config.js styles.js contents.css $RPM_BUILD_ROOT%{_appdir}
cp -a adapters plugins skins lang $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

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
%dir %{_appdir}
%{_appdir}/*.js
%{_appdir}/lang/en.js
%{_appdir}/*.css

%dir %{_appdir}/adapters
%{_appdir}/adapters/jquery.js

%dir %{_appdir}/skins
%{_appdir}/skins/moono

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
