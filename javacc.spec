# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           javacc
Version:        5.0
Release:        4
Summary:        A parser/scanner generator for java
License:        BSD
Source0:        https://javacc.dev.java.net/files/documents/17/142527/%{name}-%{version}src.tar.gz
Source1:        javacc.sh
Source2:        jjdoc
Source3:        jjtree
#Jar used for bootstrapping
Source4:        javacc.jar
URL:            https://javacc.dev.java.net/
Group:          Development/Java
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:       java, jpackage-utils >= 0:1.5
BuildRequires:  ant, ant-junit, junit >= 0:3.8.1
BuildRequires:  java-devel, jpackage-utils >= 0:1.5

BuildArch:      noarch

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
Requires:       %{name} = %{version}-%{release}

%description manual
Manual for %{name}.

%package demo
Summary:        Examples for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}

%description demo
Examples for %{name}.

%prep
%setup -q -n %{name}

# Remove binary information in the source tar
find . -name "*.jar" -exec rm {} \;
find . -name "*.class" -exec rm {} \;

find ./examples -type f -exec sed -i 's/\r//' {} \;

cp -p %{SOURCE4} bootstrap/javacc.jar

%build
# Use the bootstrap javacc.jar to generate some required
# source java files. After these source files are generated we
# remove the bootstrap jar and build the binary from source.
ant -f src/org/javacc/parser/build.xml parser-files
ant -f src/org/javacc/jjtree/build.xml tree-files
find . -name "*.jar" -exec rm {} \;
ant jar

%install
rm -fr $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 bin/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
install -d -m 755 $RPM_BUILD_ROOT/%{_bindir}
install -pD -T -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}/javacc.sh
install -pD -T -m 755 %{SOURCE2} $RPM_BUILD_ROOT/%{_bindir}/jjdoc
install -pD -T -m 755 %{SOURCE3} $RPM_BUILD_ROOT/%{_bindir}/jjtree

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}.pom

%add_to_maven_depmap net.java.dev.javacc %{name} %{version} JPP %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*.jar
%doc LICENSE README
%{_bindir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files manual
%defattr(-,root,root,-)
%doc www/*

%files demo
%defattr(-,root,root,-)
%doc examples

