%define debug_package %{nil}
%define libname %mklibname  zlibrary 
%define develname %mklibname zlibrary -d

%define	version	0.12.10
%define	release	2

Name:		fbreader
Version:	%{version}
Release:	%{release}
Summary:	Reader for e-books in various formats
License:	GPLv2
Group:		Office
URL:		http://www.fbreader.org
Source:		http://www.fbreader.org/%{name}-sources-%{version}.tgz
Source1:		FBReader.desktop
Patch0:		fbreader-0.12.10-iconext.patch
Patch1:		fbreader-0.12.10-gcc45.patch
Patch2:		fbreader-0.12.10-xdgopen.patch
Patch3:		fbreader-0.12.10-linking.patch
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
Requires:       %{libname} = %{version}

%description
FBReader is an e-book reader for various platforms.
Supported formats include: fb2, HTML, chm, plucker, palmdoc, zTxt,
TCR, RTF, OEB, OpenReader, mobipocket, plain text.


%package -n  %{libname}
Summary:        Cross-platform GUI library
Group:          Development/C
Requires:       %{libname}-ui-gtk = %{version}

%description -n %{libname}
ZLibrary is a cross-platform library to build applications running on
desktop Linux, Windows, and different Linux-based PDAs.
####
%package -n     %{develname}
Summary:        Development files for zlibrary
Group:          Development/C
Requires:	%{libname} = %{version}

%description -n %{develname}
This package contains the libraries amd header files that are needed
for writing applications with Zlibrary.
####
%package -n     %{libname}-ui-gtk
Summary:        GTK+ interface module for ZLibrary
Group:          Development/GNOME and GTK+

%description -n %{libname}-ui-gtk
This package provides a GTK+-based UI for ZLibrary.



%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0

echo "CFLAGS = %optflags" >> makefiles/arch/desktop.mk
echo "LDFLAGS = %ldflags" >> makefiles/arch/desktop.mk

%build
%make -C zlibrary/core TARGET_ARCH=desktop LIBDIR=%{_libdir} UI_TYPE=dummy
%make -C zlibrary/text TARGET_ARCH=desktop LIBDIR=%{_libdir} UI_TYPE=dummy
%make -C zlibrary/ui TARGET_ARCH=desktop LIBDIR=%{_libdir} UI_TYPE=gtk
%make -C fbreader TARGET_ARCH=desktop LIBDIR=%{_libdir} UI_TYPE=dummy


%install
make -C zlibrary/core do_install do_install_dev DESTDIR=%{buildroot} TARGET_ARCH=desktop LIBDIR=%{_libdir} UI_TYPE=dummy
make -C zlibrary/text do_install do_install_dev DESTDIR=%{buildroot} TARGET_ARCH=desktop LIBDIR=%{_libdir} UI_TYPE=dummy
make -C zlibrary/ui do_install DESTDIR=%{buildroot} TARGET_ARCH=desktop LIBDIR=%{_libdir} UI_TYPE=gtk
make -C fbreader do_install DESTDIR=%{buildroot} TARGET_ARCH=desktop UI_TYPE=dummy
touch %{buildroot}%{_libdir}/zlibrary/ui/zlui-active.so  

#man   
mkdir -p %{buildroot}%{_mandir}/man1
install -m644 fbreader/desktop/FBReader.1 %{buildroot}%{_mandir}/man1  

#menu entry
rm -rf %{buildroot}%{_datadir}/applications/FBReader.desktop
desktop-file-install %SOURCE1 %{buildroot}%{_datadir}/applications/FBReader.desktop
#### rpmlint
mkdir -p %{buildroot}%{_datadir}/zlibrary-%{version}
mv -f %{buildroot}%{_datadir}/zlibrary/ %{buildroot}%{_datadir}/zlibrary-%{version}
rm -rf %{buildroot}%{_datadir}/zlibrary






%post -n %{libname}-ui-gtk
%{_sbindir}/update-alternatives --install \
    %{_libdir}/zlibrary/ui/zlui-active.so \
    zlibrary-ui \
    %{_libdir}/zlibrary/ui/zlui-gtk.so \
    2
    
%preun -n %{libname}-ui-gtk
if [ "$1" = 0 ] ; then
    %{_sbindir}/update-alternatives --remove \
        zlibrary-ui \
        %{_libdir}/zlibrary/ui/zlui-gtk.so
fi   
    
  
    
%files 
%doc fbreader/LICENSE
%{_bindir}/FBReader
%{_datadir}/applications/FBReader.desktop
%{_datadir}/pixmaps/
%{_mandir}/man1/FBReader.1.xz
%{_datadir}/FBReader/

%files -n %{libname}
%doc fbreader/LICENSE
%{_libdir}/libzlcore.so.*
%{_libdir}/libzltext.so.*
%{_datadir}/zlibrary-%{version}
%dir %{_libdir}/zlibrary
%dir %{_libdir}/zlibrary/ui

%files -n %{develname}
%doc fbreader/LICENSE
%{_includedir}/*
%{_libdir}/lib*.so

%files -n %{libname}-ui-gtk
%doc fbreader/LICENSE
%dir %{_libdir}/zlibrary
%dir %{_libdir}/zlibrary/ui
%ghost %{_libdir}/zlibrary/ui/zlui-active.so
%{_libdir}/zlibrary/ui/zlui-gtk.so

