#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	libvirt binding for OCaml
Summary(pl.UTF-8):	Wiązania libvirt dla OCamla
Name:		ocaml-libvirt
Version:	0.6.1.4
Release:	4
License:	LGPL v2+
Group:		Libraries
Source0:	ftp://libvirt.org/libvirt/ocaml/%{name}-%{version}.tar.gz
# Source0-md5:	92723c155c009880475f3c9a093d1fe6
Patch0:		%{name}-virDomainCreateXML.patch
URL:		http://libvirt.org/ocaml/
BuildRequires:	libvirt-devel >= 0.2.1
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-findlib
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ocaml-libvirt is a complete set of OCaml bindings around libvirt,
exposing all known libvirt functionality to OCaml programs.

This package contains files needed to run bytecode executables using
the library.

%description -l pl.UTF-8
ocaml-libvirt to kompletny zestaw wiązań OCamla do libvirt,
udostępniający całą znaną funkcjonalność libvirt programom w OCamlu.

Ten pakiet zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	libvirt binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania libvirt dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
ocaml-libvirt is a complete set of OCaml bindings around libvirt,
exposing all known libvirt functionality to OCaml programs.

This package contains files needed to develop OCaml programs using
the library.

%description devel -l pl.UTF-8
ocaml-libvirt to kompletny zestaw wiązań OCamla do libvirt,
udostępniający całą znaną funkcjonalność libvirt programom w OCamlu.

Ten pakiet zawiera pliki niezbędne do tworzenia programów używających
biblioteki.

%prep
%setup -q
%patch0 -p1

%build
%configure

# parallel build triggers makefile races
%{__make} -j1 all %{?with_ocaml_opt:opt} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib,stublibs}

%{__make} install%{?with_ocaml_opt:-opt}%{!?with_ocaml_opt:-byte} \
	OCAMLFIND_INSTFLAGS="-destdir $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib"

%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib/libvirt,stublibs}/dllmllibvirt.so

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/libvirt/*.mli

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/*.ml $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO.libvirt
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllmllibvirt.so

%files devel
%defattr(644,root,root,755)
%doc libvirt/libvirt*.mli
%dir %{_libdir}/ocaml/site-lib/libvirt
%{_libdir}/ocaml/site-lib/libvirt/META
%{_libdir}/ocaml/site-lib/libvirt/libvirt*.cmi
%{_libdir}/ocaml/site-lib/libvirt/libmllibvirt.a
%{_libdir}/ocaml/site-lib/libvirt/mllibvirt.cma
%if %{with ocaml_opt}
%{_libdir}/ocaml/site-lib/libvirt/libvirt*.cmx
%{_libdir}/ocaml/site-lib/libvirt/mllibvirt.a
%{_libdir}/ocaml/site-lib/libvirt/mllibvirt.cmxa
%endif
%{_examplesdir}/%{name}-%{version}
