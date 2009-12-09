%define version 0.12.0
%define release %mkrel 1

Name: fbreader
Version: %{version}
Release: %{release}
Summary: Reader for e-books in various formats
License: GPL
Group:  Office
URL: http://www.fbreader.org
Source: http://www.fbreader.org/%{name}-sources-%{version}.tgz
BuildRequires: gtk+2-devel
BuildRequires: jpeg-devel
BuildRequires: libstdc++-devel
BuildRequires: libexpat-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: linebreak-devel
BuildRequires: curl-devel
BuildRequires: fribidi-devel
BuildRequires: sqlite3-devel
Buildroot: %{_tmppath}/%{name}-%{version}

%description
FBReader is an e-book reader for various platforms.
Supported formats include: fb2, HTML, chm, plucker, palmdoc, zTxt,
TCR, RTF, OEB, OpenReader, mobipocket, plain text.

%prep
%setup -q
perl -pi -e 's/moc-qt4/moc/' makefiles/arch/desktop.mk

%build
make TARGET_ARCH="desktop" \
    UI_TYPE="gtk" \
    DESTDIR=%{buildroot} \
    INSTALLDIR=%{_prefix} \
    LIBDIR=%{_libdir}

%install
%make TARGET_ARCH="desktop" \
    UI_TYPE="gtk" \
    DESTDIR=%{buildroot} \
    INSTALLDIR=%{_prefix} \
    LIBDIR=%{_libdir} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/FBReader
%{_libdir}/libzlcore.so.*
%{_libdir}/libzltext.so.*
%{_libdir}/zlibrary/ui/zlui-gtk.so
%{_datadir}/FBReader/
%{_datadir}/pixmaps/
%{_datadir}/zlibrary/
%{_datadir}/applications/FBReader.desktop

