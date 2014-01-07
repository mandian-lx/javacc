
<<<cause rebuild failure on purpose to not overwrite bootstraped packages>>>
%undefine _compress
%undefine _extension
%global _duplicate_files_terminate_build 0
%global _files_listed_twice_terminate_build 0
%global _unpackaged_files_terminate_build 0
%global _nonzero_exit_pkgcheck_terminate_build 0
%global _use_internal_dependency_generator 0
%global __find_requires /bin/sed -e 's/.*//'
%global __find_provides /bin/sed -e 's/.*//'

Name:		javacc
Version:	5.0
Release:	9.0
License:	GPLv3+
Source0:	javacc-5.0-9.0-omv2014.0.noarch.rpm

URL:		https://abf.rosalinux.ru/openmandriva/javacc
BuildArch:	noarch
Summary:	javacc bootstrap version
Requires:	javapackages-bootstrap
Requires:	java
Requires:	jpackage-utils
Provides:	javacc = 0:5.0-9.0:2014.0
Provides:	mvn(net.java.dev.javacc:javacc) = 4.2

%description
javacc bootstrap version.

%files
/usr/bin/javacc.sh
/usr/bin/jjdoc
/usr/bin/jjtree
/usr/share/doc/javacc
/usr/share/doc/javacc/LICENSE
/usr/share/doc/javacc/README
/usr/share/java/javacc.jar
/usr/share/maven-fragments/javacc
/usr/share/maven-poms/JPP-javacc.pom

#------------------------------------------------------------------------
%prep

%build

%install
cd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -id
