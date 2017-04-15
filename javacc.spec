%{?_javapackages_macros:%_javapackages_macros}
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

%global releasename release_%(tr . _ <<< %{version})

Name:           javacc
Version:        7.0.2
Release:        2%{?dist}
Epoch:          0
Summary:        A parser/scanner generator for java
License:        BSD
URL:            http://javacc.org
Source0:        https://github.com/javacc/javacc/archive/%{releasename}.tar.gz

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  javacc

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

%description manual
Manual for %{name}.

%package demo
Summary:        Examples for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
Examples for %{name}.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{releasename}

# Remove binary information in the source tar
find . -name "*.jar" -delete
find . -name "*.class" -delete

find ./examples -type f -exec sed -i 's/\r//' {} \;

build-jar-repository -p bootstrap javacc

%mvn_file : %{name}

%build
# There is maven pom which doesn't really work for building. The tests don't
# work either (even when using bundled jars).
ant jar javadoc

# The pom dependencies are also wrong
%mvn_artifact --skip-dependencies pom.xml target/javacc-%{version}.jar

%install
%mvn_install -J target/javadoc

%jpackage_script javacc '' '' javacc javacc true
ln -s %{_bindir}/javacc %{buildroot}%{_bindir}/javacc.sh
%jpackage_script jjdoc '' '' javacc jjdoc true
%jpackage_script jjtree '' '' javacc jjtree true

%files -f .mfiles
%doc LICENSE
%doc README
%{_bindir}/javacc
%{_bindir}/javacc.sh
%{_bindir}/jjdoc
%{_bindir}/jjtree

%files manual
%doc www/*

%files demo
%doc examples

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:7.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Michael Simacek <msimacek@redhat.com> - 0:7.0.2-1
- Update to upstream version 7.0.2

* Mon Jan 02 2017 Michael Simacek <msimacek@redhat.com> - 0:7.0.1-1
- Update to upstream version 7.0.1

* Tue Sep 06 2016 Michael Simacek <msimacek@redhat.com> - 0:6.1.3-1
- Update to upstream version 6.1.3
- Use new upstream location
- Generate scripts with jpackage_script

* Tue Aug 23 2016 Michael Simacek <msimacek@redhat.com> - 0:6.1.2-1
- Update to upstream version 6.1.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:5.0-11
- Use .mfiles generated during build

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:5.0-10
- Use Requires: java-headless rebuild (#1067528)

* Tue Jul 30 2013 Michal Srb <msrb@redhat.com> - 0:5.0-9
- Generate javadoc
- Drop group tag

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Jaromir Capik <jcapik@redhat.com> 0:5.0-6
- Fixing #835786 - javacc: Invalid upstream URL
- Minor spec file changes according to the latest guidelines

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-3
- Fix examples line endings.

* Fri Jun 4 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-2
- Apply changes requested in review bug (rhbz#225940).

* Thu Feb 11 2010 Alexander Kurtakov <akurtako@redhat.com> 0:5.0-1
- Update to upstream 5.0 release.

* Tue Nov 24 2009 Alexander Kurtakov <akurtako@redhat.com> 0:4.1-0.6
- Use standard permissions and fix unowned directories.

* Tue Nov 24 2009 Alexander Kurtakov <akurtako@redhat.com> 0:4.1-0.5
- Fix rpmlint warnings.
- Drop gcj support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:4.1-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 03 2008 Matt Wringe <mwringe@redhat.com> - 0:4.1-0.2
- Update to remove packaged jars in source tar
- Build with bootstrap jar so that required java source 
  files get generated

* Wed Oct 22 2008 Jerry James <loganjerry@gmail.com> - 0:4.1-0.1
- Update to 4.1
- Also ship the jjrun script
- Own the appropriate gcj directory
- Minor spec file changes to comply with latest Fedora guidelines
- Include the top-level index.html file in the manual

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:4.0-4.5
- drop repotag

* Fri Feb 22 2008 Matt Wringe <mwringe at redhat.com> - 0:4.0-4jpp.4
- Rename javacc script file to javacc.sh as this confuses the makefile

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:4.0-4jpp.3
- Autorebuild for GCC 4.3

* Thu Aug 10 2006 Matt Wringe <mwringe at redhat.com> - 0:4.0-3jpp.3
- Rebuilt with new naming convention

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:4.0-3jpp_2fc
- Rebuilt

* Tue Jul 18 2006 Matthew Wringe <mwringe at redhat.com> - 0:4.0-3jpp_1fc
- Merged with upstream version
- Changed directory locations to rpm macros
- Added conditional native compiling

* Thu Apr 20 2006 Fernando Nasser <fnasser@redhat.com> - 0:4.0-2jpp
- First JPP 1.7 build

* Fri Mar 31 2006 Sebastiano Vigna <vigna at acm.org> - 0:4.0-1jpp
- Updated to 4.0

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.2-2jpp
- Rebuild with ant-1.6.2

* Fri Jan 30 2004 Sebastiano Vigna <vigna at acm.org> 0:3.2-1jpp
- First JPackage version
