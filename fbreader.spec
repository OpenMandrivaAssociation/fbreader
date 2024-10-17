# empty debug
%define debug_package %{nil}
%define _disable_ld_no_undefined 1

%define major 0.99
%define libzlcore %mklibname zlcore %{major}
%define libzltext %mklibname zltext %{major}
%define libzlui %mklibname zlui %{major}

Summary:	Reader for e-books in various formats
Name:		fbreader
Version:	0.99.5
Release:	0.3
License:	GPLv2+
Group:		Office
Url:		https://www.fbreader.org
#Source0:	http://fbreader.org/files/desktop/%{name}-sources-%{version}.tgz
# from git this time
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	bzip2-devel
BuildRequires:	jpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	linebreak-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(fribidi)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	desktop-file-utils
# force explicit Requires because of library packages being messed up in past
Requires:	%{libzlcore} = %{EVRD}
Requires:	%{libzltext} = %{EVRD}
Requires:	%{libzlui} = %{EVRD}
Obsoletes:	%{_lib}zlibrary-devel < 0.99.5

%description
FBReader is an e-book reader for various platforms.
Supported formats include: fb2, HTML, chm, plucker, palmdoc,
zTxt, TCR, RTF, OEB, OpenReader, mobipocket, plain text.

%files
%doc fbreader/LICENSE
%{_bindir}/FBReader
%{_datadir}/FBReader/
%{_datadir}/pixmaps/FBReader/
%{_datadir}/pixmaps/FBReader.png
%{_datadir}/applications/FBReader.desktop
%{_mandir}/man1/FBReader.1.*

#----------------------------------------------------------------------------

%package -n %{libzlcore}
Summary:	Cross-platform GUI library
Group:		System/Libraries
Requires:	zlibrary-common = %{EVRD}
Conflicts:	%{_lib}zlibrary < 0.99.5
Obsoletes:	%{_lib}zlibrary < 0.99.5

%description -n %{libzlcore}
ZLibrary is a cross-platform library to build applications running on
desktop Linux, Windows, and different Linux-based PDAs.

This package provides ZLibrary core.

%files -n %{libzlcore}
%{_libdir}/libzlcore.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libzltext}
Summary:	Cross-platform GUI library
Group:		System/Libraries
Requires:	zlibrary-common = %{EVRD}
Conflicts:	%{_lib}zlibrary < 0.99.5

%description -n %{libzltext}
ZLibrary is a cross-platform library to build applications running on
desktop Linux, Windows, and different Linux-based PDAs.

This package provides ZLibrary text.

%files -n %{libzltext}
%{_libdir}/libzltext.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libzlui}
Summary:	Cross-platform GUI library
Group:		System/Libraries
Requires:	zlibrary-common = %{EVRD}
Conflicts:	%{_lib}zlibrary < 0.99.5

%description -n %{libzlui}
ZLibrary is a cross-platform library to build applications running on
desktop Linux, Windows, and different Linux-based PDAs.

This package provides ZLibrary ui.

%files -n %{libzlui}
%{_libdir}/libzlui.so.%{major}*

#----------------------------------------------------------------------------

%package -n zlibrary-common
Summary:	Cross-platform GUI library
Group:		System/Libraries
BuildArch:	noarch
Conflicts:	%{_lib}zlibrary < 0.99.5

%description -n zlibrary-common
ZLibrary is a cross-platform library to build applications running on
desktop Linux, Windows, and different Linux-based PDAs.

This package provides ZLibrary common files.

%files -n zlibrary-common
%{_datadir}/zlibrary/

#----------------------------------------------------------------------------

%prep
%setup -q

# fix icon extension in the .desktop file
perl -pi -e 's,FBReader.png,FBReader,' fbreader/desktop/desktop

# fix qt4 build
perl -pi -e 's,moc-qt4,%{qt4bin}/moc,' makefiles/arch/desktop.mk
perl -pi -e 's,CC = .*,CC = gcc,' makefiles/arch/desktop.mk
perl -pi -e 's,QTINCLUDE = -I /usr/include/qt4,QTINCLUDE = -I %{qt4include},' makefiles/arch/desktop.mk
perl -pi -e 's,UILIBS = -lQtGui,UILIBS = -lQtGui -lQtCore,' makefiles/arch/desktop.mk
perl -pi -e 's,-lunibreak,-llinebreak,' makefiles/config.mk zlibrary/text/Makefile

echo "CFLAGS = %{optflags}" >> makefiles/arch/desktop.mk
echo "LDFLAGS = %{ldflags}" >> makefiles/arch/desktop.mk

%build
make -C zlibrary/core TARGET_ARCH=desktop UI_TYPE=dummy

make -C zlibrary/text TARGET_ARCH=desktop UI_TYPE=dummy

make -C zlibrary/ui TARGET_ARCH=desktop UI_TYPE=qt4

make -C fbreader TARGET_ARCH=desktop UI_TYPE=dummy

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
	--add-mime-type="application/vnd.ms-htmlhelp;" \
	%{buildroot}%{_datadir}/applications/FBReader.desktop --dir=%{buildroot}%{_datadir}/applications/

# man
mkdir -p %{buildroot}%{_mandir}/man1
install -m644 fbreader/desktop/FBReader.1 %{buildroot}%{_mandir}/man1

# remove useless .so files (there are no includes to use them)
rm -f %{buildroot}%{_libdir}/*.so
