%define gcj_support 0
%define section free

Name:           javacc
Version:        4.1
Release:        %mkrel 0.5
Summary:        A parser/scanner generator for java
License:        BSD
Source0:        https://javacc.dev.java.net/files/documents/17/26783/javacc-%{version}src.tar.bz2
Source1:        javacc
Source2:        jjdoc
Source3:        jjtree
#Jar used for bootstrapping
Source4:  javacc.jar
URL:            https://javacc.dev.java.net/
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       jpackage-utils
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  java-rpmbuild
BuildRequires:  jpackage-utils
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
Java Compiler Compiler (JavaCC) is the most popular parser generator for use
with Java applications. A parser generator is a tool that reads a grammar
specification and converts it to a Java program that can recognize matches to
the grammar. In addition to the parser generator itself, JavaCC provides other
standard capabilities related to parser generation such as tree building (via
a tool called JJTree included with JavaCC), actions, debugging, etc.

%package manual
Summary:        Manual for %{name}
Group:          Development/Java

%description manual
Manual for %{name}.

%package demo
Summary:        Examples for %{name}
Group:          Development/Java

%description demo
Examples for %{name}.

%prep
%setup -q -n %{name}
# Remove binary information in the source tar
find . -name "*.jar" -exec rm {} \;
find . -name "*.class" -exec rm {} \;

cp -p %{SOURCE1} bin/javacc
cp -p %{SOURCE2} bin/jjdoc
cp -p %{SOURCE3} bin/jjtree

cp -p %{SOURCE4} bootstrap/javacc.jar

%build
# Use the bootstrap javacc.jar to generate some required
# source java files. After these source files are generated we
# remove the bootstrap jar and build the binary from source.
%ant -f src/org/javacc/parser/build.xml parser-files
%ant -f src/org/javacc/jjtree/build.xml tree-files
find . -name "*.jar" -exec rm {} \;
%ant jar

%install
rm -fr $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 bin/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -d -m 755 $RPM_BUILD_ROOT/%{_bindir}
install -m 755 bin/javacc bin/jjdoc bin/jjrun bin/jjtree $RPM_BUILD_ROOT/%{_bindir}
install -d -m 755 $RPM_BUILD_ROOT/%{_datadir}/%{name}
cp -pr examples $RPM_BUILD_ROOT/%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*.jar.*
%endif
%doc LICENSE README
%defattr(0755,root,root,0755)
%{_bindir}/*

%files manual
%defattr(0644,root,root,0755)
%doc www/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
