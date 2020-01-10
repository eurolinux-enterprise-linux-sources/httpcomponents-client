%global base_name httpcomponents

Name:              httpcomponents-client
Summary:           HTTP agent implementation based on httpcomponents HttpCore
Version:           4.2.5
Release:           3%{?dist}
Group:             Development/Libraries
License:           ASL 2.0
URL:               http://hc.apache.org/
Source0:           http://archive.apache.org/dist/httpcomponents/httpclient/source/%{name}-%{version}-src.tar.gz

BuildArch:         noarch

BuildRequires:     maven-local
BuildRequires:     mvn(commons-codec:commons-codec)
BuildRequires:     mvn(commons-logging:commons-logging)
BuildRequires:     mvn(org.apache.httpcomponents:httpcore)
BuildRequires:     mvn(org.apache.httpcomponents:project)
%if 0%{?fedora}
# Test dependencies
BuildRequires:     mvn(org.mockito:mockito-core)
BuildRequires:     mvn(junit:junit)
%endif

%description
HttpClient is a HTTP/1.1 compliant HTTP agent implementation based on
httpcomponents HttpCore. It also provides reusable components for
client-side authentication, HTTP state management, and HTTP connection
management. HttpComponents Client is a successor of and replacement
for Commons HttpClient 3.x. Users of Commons HttpClient are strongly
encouraged to upgrade.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Documentation

%description    javadoc
%{summary}.


%prep
%setup -q

# Remove optional build deps not available in Fedora
%pom_disable_module httpclient-cache
%pom_disable_module httpclient-osgi
%pom_disable_module fluent-hc
%pom_remove_plugin :maven-notice-plugin
%pom_remove_plugin :docbkx-maven-plugin
%pom_remove_plugin :clirr-maven-plugin
%pom_remove_plugin :maven-clover2-plugin httpclient
%if !0%{?fedora}
%pom_remove_dep :mockito-core httpclient
%endif

# Add proper Apache felix bundle plugin instructions
# so that we get a reasonable OSGi manifest.
for module in httpclient httpmime; do
    %pom_xpath_remove "pom:project/pom:packaging" $module
    %pom_xpath_inject "pom:project" "<packaging>bundle</packaging>" $module
done

# Make httpmime into bundle
%pom_xpath_inject pom:build/pom:plugins "
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <extensions>true</extensions>
    </plugin>" httpmime

# Make httpclient into bundle
%pom_xpath_inject pom:reporting/pom:plugins "
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <configuration>
        <instructions>
          <Export-Package>*</Export-Package>
          <Private-Package></Private-Package>
          <Import-Package>!org.apache.avalon.framework.logger,!org.apache.log,!org.apache.log4j,*</Import-Package>
        </instructions>
      </configuration>
    </plugin>" httpclient
%pom_xpath_inject pom:build/pom:plugins "
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <extensions>true</extensions>
      <configuration>
        <instructions>
          <Export-Package>org.apache.http.*,!org.apache.http.param</Export-Package>
          <Private-Package></Private-Package>
          <_nouses>true</_nouses>
          <Import-Package>!org.apache.avalon.framework.logger,!org.apache.log,!org.apache.log4j,*</Import-Package>
        </instructions>
        <excludeDependencies>true</excludeDependencies>
      </configuration>
    </plugin>" httpclient



%build
%mvn_file ":{*}" httpcomponents/@1

# Build with tests enabled on Fedora
%if 0%{?fedora}
%mvn_build
%else
%mvn_build -f
%endif


%install
%mvn_install


%files -f .mfiles
%doc LICENSE.txt NOTICE.txt
%doc README.txt RELEASE_NOTES.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.5-3
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Jun 10 2013 Michal Srb <msrb@redhat.com> - 4.2.5-2
- Enable tests on Fedora

* Thu Apr 25 2013 Michal Srb <msrb@redhat.com> - 4.2.5-1
- Update to upstream version 4.2.5

* Thu Apr 11 2013 Michal Srb <msrb@redhat.com> - 4.2.4-1
- Update to upstream version 4.2.4

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 4.2.3-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Fri Jan 25 2013 Michal Srb <msrb@redhat.com> - 4.2.3-2
- Build with xmvn
- Disable fluent-hc module

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.3-1
- Update to upstream version 4.2.3

* Thu Oct 25 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.2-1
- Update to upstream version 4.2.2

* Wed Aug  1 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-3
- Fix OSGi manifest in httpmime

* Fri Jul 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-2
- Install NOTICE.txt file
- Fix javadir directory ownership
- Fix directory permissions
- Preserve timestamps
- Replace add_to_maven_depmap with add_maven_depmap

* Fri Jul 27 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 4.2.1-1
- Update to upstream version 4.2.1
- Convert patches to POM macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 2 2012 Alexander Kurtakov <akurtako@redhat.com> 4.1.3-3
- Do not export org.apache.http.param in osgi.

* Mon Mar 26 2012 Alexander Kurtakov <akurtako@redhat.com> 4.1.3-2
- Do not export * but only org.apache.http.* .
- Do not generate uses clauses in the manifest.

* Thu Mar  1 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> 4.1.3-1
- Update to latest upstream bugfix

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.2-1
- Update to latest upstream (4.1.2)
- Minor tweaks according to guidelines

* Fri Jul 15 2011 Severin Gehwolf <sgehwolf@redhat.com> 4.1.1-3
- Fix for RH Bz#718830. Add instructions so as to not
  Import-Package optional dependencies.

* Thu Apr 7 2011 Severin Gehwolf <sgehwolf@redhat.com> 4.1.1-2
- Add BR/R apache-commons-codec, since httpcomponents-client's
  MANIFEST.MF has an Import-Package: org.apache.commons.codec
  header.

* Tue Mar 29 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.1.1-1
- New upstream bugfix version (4.1.1)

* Tue Mar 15 2011 Severin Gehwolf <sgehwolf@redhat.com> 4.1-6
- Explicitly set PrivatePackage to the empty set, so as to
  export all packages.

* Thu Mar 10 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-5
- OSGi export more packages.

* Fri Feb 25 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-4
- Build httpmime module.

* Fri Feb 18 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-3
- Don't use basename as an identifier.

* Fri Feb 18 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-2
- OSGify properly.
- Install into %{_javadir}/%{basename}.

* Thu Feb 17 2011 Alexander Kurtakov <akurtako@redhat.com> 4.1-1
- Update to latest upstream version.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.0.3-2
- Added license to javadoc subpackage

* Mon Dec 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 4.0.3-1
- Initial version
