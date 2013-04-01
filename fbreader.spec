
# empty debug
%define debug_package %{nil}
%define libname %mklibname  zlibrary 

Name:		fbreader
Version:	0.99.4
Release:	2
Summary:	Reader for e-books in various formats
License:	GPLv2
Group:		Office
URL:		http://www.fbreader.org
Source:		http://fbreader.org/files/desktop/%{name}-sources-%{version}.tgz
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(gdk-2.0)
BuildRequires:	jpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	linebreak-devel
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	desktop-file-utils
BuildRequires:	qt4-devel
Requires:	%{libname}

%description
FBReader is an e-book reader for various platforms.
Supported formats include: fb2, HTML, chm, plucker, palmdoc, zTxt,
TCR, RTF, OEB, OpenReader, mobipocket, plain text.

%package -n  %{libname}
Summary:        Cross-platform GUI library
Group:          Development/C

%package -n  %{libname}-devel
Summary:        Development files for %{libname}
Group:          Development/C

%description -n %{libname}
ZLibrary is a cross-platform library to build applications running on
desktop Linux, Windows, and different Linux-based PDAs.

%description -n %{libname}-devel
Fake devel package provided for backward compatibility
####


%prep
%setup -q

# fix icon extension in the .desktop file
perl -pi -e 's,FBReader.png,FBReader,' fbreader/desktop/desktop

# fix qt4 build
perl -pi -e 's,moc-qt4,%qt4bin/moc,' makefiles/arch/desktop.mk
perl -pi -e 's,CC = .*,CC = gcc,' makefiles/arch/desktop.mk
perl -pi -e 's,QTINCLUDE = -I /usr/include/qt4,QTINCLUDE = -I %qt4include,' makefiles/arch/desktop.mk
perl -pi -e 's,UILIBS = -lQtGui,UILIBS = -lQtGui -lQtCore,' makefiles/arch/desktop.mk
perl -pi -e 's,-lunibreak,-llinebreak,' makefiles/config.mk zlibrary/text/Makefile

%define _disable_ld_no_undefined 1
echo "CFLAGS = %optflags" >> makefiles/arch/desktop.mk
echo "LDFLAGS = %ldflags" >> makefiles/arch/desktop.mk

%build
make -C zlibrary/core TARGET_ARCH=desktop UI_TYPE=dummy \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir}

make -C zlibrary/text TARGET_ARCH=desktop UI_TYPE=dummy \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir}

make -C zlibrary/ui TARGET_ARCH=desktop UI_TYPE=qt4 \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir}

make -C fbreader TARGET_ARCH=desktop UI_TYPE=dummy \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir}

%install
make -C zlibrary/core TARGET_ARCH=desktop UI_TYPE=dummy \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir} do_install

make -C zlibrary/text TARGET_ARCH=desktop UI_TYPE=dummy \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir} do_install

make -C zlibrary/ui TARGET_ARCH=desktop UI_TYPE=qt4 \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir} do_install

make -C fbreader TARGET_ARCH=desktop UI_TYPE=dummy \
	DESTDIR=%{buildroot} INSTALLDIR=%{_prefix} LIBDIR=%{_libdir} do_install

# add mimetypes
desktop-file-install \
	--vendor="" \
	--add-mime-type="application/epub+zip;application/rtf;" \
	--add-mime-type="application/x-mobipocket-ebook;application/x-fictionbook+xml;" \
	--add-mime-type="text/html;application/xhtml+xml;" \
	%{buildroot}%{_datadir}/applications/FBReader.desktop --dir=%{buildroot}%{_datadir}/applications/

# man   
mkdir -p %{buildroot}%{_mandir}/man1
install -m644 fbreader/desktop/FBReader.1 %{buildroot}%{_mandir}/man1  

%files 
%doc fbreader/LICENSE
%{_bindir}/FBReader
%{_datadir}/FBReader/
%{_datadir}/pixmaps/
%{_datadir}/applications/FBReader.desktop
%{_mandir}/man1/FBReader.1.xz

%files -n  %{libname}
%doc fbreader/LICENSE
%{_libdir}/libzlcore.*
%{_libdir}/libzlui.*
%{_libdir}/libzltext.*
%{_datadir}/zlibrary/

%files -n  %{libname}-devel

