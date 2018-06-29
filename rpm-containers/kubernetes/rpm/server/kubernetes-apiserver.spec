Summary: DLS4E Kubernetes Apiserver v%{_dls4e_version} package
Name: dls4e-kubernetes-apiserver
Version: %{_dls4e_version}
Release: %{_dls4e_release}
License: Apache-2.0
Group: Tools
SOURCE0 : kubernetes.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: dls4e-commons

%define  debug_package %{nil}

%description
%{summary}

%prep
%setup -q -n kubernetes

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}

mkdir -p %{buildroot}/opt/dls4e/kubernetes
cp -a kube-apiserver %{buildroot}/opt/dls4e/kubernetes/kube-apiserver


%clean
rm -rf %{buildroot}


%files
%defattr(0755,root,root,-)
/opt/dls4e/kubernetes/kube-apiserver