%define name	dyalog
%define Name	DyALog
%define version 1.11.3
%define release %mkrel 1

%if %{mdkversion} < 1010
	%define __libtoolize /bin/true
%endif

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Compiler for tabular execution of logic programs
Summary(fr):	Compilateur pour l'execution tabulaire de programmes logiques
License:	GPL
Group:		Sciences/Computer science
Url:		http://atoll.inria.fr/~clerger
Source:		ftp://ftp.inria.fr/INRIA/Projects/Atoll/Eric.Clergerie/DyALog/%{Name}-%{version}.tar.gz
Requires:	    automake1.9
Requires:	    libgc-devel
BuildRequires:	libgc-devel
BuildRequires:	perl-Test-Cmd
BuildRequires:	perl-Test-Simple
ExclusiveArch:  %{ix86}
Buildroot:	    %{_tmppath}/%{name}-%{version}

%description
DyALog is an experimental compiler of logic programs and grammars
oriented toward a tabular execution (.i.e., where subcomputations are
shared when possible by storing traces of them in a table). It is
useful to build efficient parsers for highly ambiguous and recursive
grammars for Natural Language processing.

%description -l fr
DyALog est un compilateur experimental de grammaires et programmes
logiques concu pour assurer une evaluation tabulaire (c.a.d où les
sous-calculs sont réutilisés quand c'est possible grâce à un stockage
de traces dans une table). Ce compilateur est surtout utile pour
construire des analyseurs syntaxiques efficaces pour des grammaires
hautement ambiguës et récursives dans le cadre du traitement de la
langue naturelle.

%prep
%setup -q -n %{Name}-%{version}

%build
%configure2_5x
%make CFLAGS="$RPM_OPT_FLAGS" CCASFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
%makeinstall_std
%make check

%if %{mdkversion} >= 1010
install -d -m 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf <<EOF
%{_libdir}/DyALog
EOF
%endif

%clean
rm -rf %{buildroot}

%post
%_install_info %{name}.info
%if %{mdkversion} < 1010
cat %{_sysconfdir}/ld.so.conf<<EOF
%{_libdir}/DyALog
EOF
%endif
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%preun
%_remove_install_info %{name}.info

%postun
%if %{mdkversion} < 1010
perl -pi -e 's|^%{_libdir}/DyALog\n||' %{_sysconfdir}/ld.so.conf
%{_libdir}/DyALog
%endif
%if %mdkversion < 200900
/sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
%if %{mdkversion} >= 1010
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%endif
%{_bindir}/*
%{_infodir}/dyalog*
%{_libdir}/DyALog
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/aclocal/%{name}.m4

