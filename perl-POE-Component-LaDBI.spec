#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	POE
%define	pnam	Component-LaDBI
Summary:	POE::Component::LaDBI - POE Component that spawns a perl subprocess to handle non-blocking access to the DBI API.
#Summary(pl):	
Name:		perl-POE-Component-LaDBI
Version:	1.2.1
Release:	0.1
# same as perl (REMOVE THIS LINE IF NOT TRUE)
#License:	GPL v1+ or Artistic
# no license information in package (or i didnt saw any)
License:	-
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	5703be6ff1b6140519023c917f4b3854
# that diff contain various fixes,
Patch0:		perl-POE-Component-LaDBI.patch 
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(DBI) >= 1.20
BuildRequires:	perl(POE) >= 0.18
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
All request events have the same handler. This is because the handler merely
creates a request message and sends it to the perl sub-process which is doing
the actuall DBI calls.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{perl_vendorlib}/POE/Component/example.pl $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/
mv $RPM_BUILD_ROOT%{perl_vendorlib}/POE/Component/ladbi_config.pl $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog Changes README
%{perl_vendorlib}/POE/Component/*.pm
%{perl_vendorlib}/POE/Component/LaDBI
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
