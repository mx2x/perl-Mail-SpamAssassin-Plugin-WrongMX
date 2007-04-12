Summary:	The WrongMX Plugin for SpamAssassin
Name:		perl-Mail-SpamAssassin-Plugin-WrongMX
Version:	0
Release:	%mkrel 2
License:	Apache License
Group:		Development/Perl
URL:		http://people.apache.org/~dos/sa-plugins/3.0/
Source0:	http://people.apache.org/~dos/sa-plugins/3.0/wrongmx.cf.bz2
Source1:	http://people.apache.org/~dos/sa-plugins/3.0/wrongmx.pm.bz2
Patch0:		WrongMX-fix-module-path.patch
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  spamassassin-spamd >= 3.1.1
Requires:	spamassassin-spamd >= 3.1.1
BuildArch:	noarch
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
WrongMX determines if an email was sent to a lower preference MX when a higher
preference MX was likely available.

 o How To Use It:
   Save the two files above in your local configuration directory 
   (/etc/mail/spamassassin/) and set the score in wrongmx.cf to whatever you
   desire, based on your confidence in your primary MX server stability.

  o How NOT To Use It:
    Do not use this plugin on overloaded mail systems that frequently stop
    accepting connections on the primary MX servers due to system load since
    it will cause some false positives if you set the score too high.

%prep

%setup -q -T -c -n %{name}-%{version}

bzcat %{SOURCE0} > WrongMX.cf
bzcat %{SOURCE1} > WrongMX.pm

%patch0

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -d %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin

install -m0644 WrongMX.cf %{buildroot}%{_sysconfdir}/mail/spamassassin/
install -m0644 WrongMX.pm %{buildroot}%{perl_vendorlib}/Mail/SpamAssassin/Plugin/

%post
if [ -f %{_var}/lock/subsys/spamd ]; then
    %{_initrddir}/spamd restart 1>&2;
fi
    
%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/spamd ]; then
        %{_initrddir}/spamd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mail/spamassassin/WrongMX.cf
%{perl_vendorlib}/Mail/SpamAssassin/Plugin/WrongMX.pm


