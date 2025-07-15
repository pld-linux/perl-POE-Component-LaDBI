#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define	pdir	POE
%define	pnam	Component-LaDBI
Summary:	POE::Component::LaDBI - POE Component that spawns a perl subprocess to handle non-blocking access to the DBI API
Summary(pl.UTF-8):	POE::Component::LaDBI - komponent POE uruchamiający podproces perla obsługujący nieblokujący dostęp do API DBI
Name:		perl-POE-Component-LaDBI
Version:	1.2.1
Release:	0.1
License:	unknown
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/POE/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	5703be6ff1b6140519023c917f4b3854
Patch0:		%{name}.patch 
URL:		http://search.cpan.org/dist/POE-Component-LaDBI/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-DBI >= 1.20
BuildRequires:	perl-POE >= 0.18
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
POE::Component::LaDBI is a POE Component to allow for non-blocking
access to most of the DBI API. Each LaDBI component session started
spawns a sub-process which it communicates with via POE::Wheel::Run.
Multiple DBI database handles can be created in the sub-process, but
within the sub-process DBI calls will still block.

%description -l pl.UTF-8
POE::Component::LaDBI to komponent POE umożliwiający nieblokujący
dostęp do większości API DBI. Każda uruchomiona sesja komponentu LaDBI
tworzy podproces, z którym komunikuje się poprzez POE::Wheel::Run.
W podprocesie można utworzyć wiele uchwytów baz danych DBI, ale w
ramach podprocesu wywołania DBI będą nadal blokujące.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch -P0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{perl_vendorlib}/POE/Component/example.pl $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv $RPM_BUILD_ROOT%{perl_vendorlib}/POE/Component/ladbi_config.pl $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog Changes README
%{perl_vendorlib}/POE/Component/*.pm
%{perl_vendorlib}/POE/Component/LaDBI
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
