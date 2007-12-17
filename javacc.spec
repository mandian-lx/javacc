%bcond_without bootstrap

%define section free
%define gcj_support 1

Name:           javacc
Version:        4.0
Release:        %mkrel 3.6
Epoch:          0
Summary:        A parser/scanner generator for java
License:        BSD
#Vendor:         JPackage Project
#Distribution:   JPackage
# Re-zipped with jars removed
Source0:        https://javacc.dev.java.net/files/documents/17/26783/javacc-%{version}src.tar.bz2
Source1:        javacc
Source2:        jjdoc
Source3:        jjtree
Patch0:         javacc-build.patch
Patch1:         javacc-generated-files.patch
URL:            https://javacc.dev.java.net/
Group:          Development/Java
Requires:       jpackage-utils
BuildRequires:  ant
%if %without bootstrap
BuildRequires:  javacc
%endif
BuildRequires:  java-devel
BuildRequires:  junit
BuildRequires:  java-rpmbuild
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
%patch0 -p1
%if %without bootstrap
%{__ln_s} %{_javadir}/javacc.jar bootstrap/javacc.jar
%else
%patch1 -p1
%endif
%{__ln_s} %{_javadir}/junit.jar lib/junit3.8.1/junit.jar

%{__cp} -a %{SOURCE1} javacc
%{__cp} -a %{SOURCE2} jjdoc
%{__cp} -a %{SOURCE3} jjtree
%{__mv} www/doc .

%build
export CLASSPATH=
export OPT_JAR_LIST=
%ant -Dversion=%{version} jar

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a bin/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a javacc jjdoc jjtree %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
%{__cp} -a examples %{buildroot}%{_datadir}/%{name}

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
%doc doc/*

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}


