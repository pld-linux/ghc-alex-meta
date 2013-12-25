#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	alex-meta
Summary:	Quasi-quoter for Alex lexers
Summary(pl.UTF-8):	Quasi-quoter dla analizatorów leksykalnych narzędzia Alex
Name:		ghc-%{pkgname}
Version:	0.3.0.5
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/alex-meta
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	a2c39f21b06d2c186ff5b66f53dffc17
URL:		http://hackage.haskell.org/package/alex-meta
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-QuickCheck >= 2
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 4.2
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-containers
BuildRequires:	ghc-haskell-src-meta >= 0.5.1.2
BuildRequires:	ghc-haskell-src-meta < 1.0
BuildRequires:	ghc-template-haskell >= 2.5
BuildRequires:	ghc-template-haskell < 2.9
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-QuickCheck-prof >= 2
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 4.2
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-haskell-src-meta-prof >= 0.5.1.2
BuildRequires:	ghc-haskell-src-meta-prof < 1.0
BuildRequires:	ghc-template-haskell-prof >= 2.5
BuildRequires:	ghc-template-haskell-prof < 2.9
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_releq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 4.2
Requires:	ghc-base < 5
Requires:	ghc-containers
Requires:	ghc-haskell-src-meta >= 0.5.1.2
Requires:	ghc-haskell-src-meta < 1.0
Requires:	ghc-template-haskell >= 2.5
Requires:	ghc-template-haskell < 2.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Quasi-quoter for Alex lexers.

%description -l pl.UTF-8
Quasi-quoter dla analizatorów leksykalnych narzędzia Alex.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 4.2
Requires:	ghc-base-prof < 5
Requires:	ghc-containers-prof
Requires:	ghc-haskell-src-meta-prof >= 0.5.1.2
Requires:	ghc-haskell-src-meta-prof < 1.0
Requires:	ghc-template-haskell-prof >= 2.5
Requires:	ghc-template-haskell-prof < 2.9

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSalex-meta-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSalex-meta-%{version}.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Ranged
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Ranged/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Alex.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Alex
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Alex/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSalex-meta-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Ranged/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Alex.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Alex/*.p_hi
