Name:           pcn-calculator
Version:        1.0.1
Release:        1%{?dist}
Summary:        Advanced calculator with modern style

License:        MIT
URL:            https://github.com/pacanekk/PCN-Calculator
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       python3
Requires:       python3-pillow

%description
PCN Calculator is an advanced desktop calculator application
with modern style. Features include:
- Standard and Scientific modes
- Calculation history
- Keyboard support
- Modern dark theme UI

%prep
%autosetup

%build
# No build step needed for Python script

%install
rm -rf %{buildroot}

# Create directories
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/pcn-calculator
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
mkdir -p %{buildroot}%{_docdir}/%{name}

# Install main script
install -m 755 calculator_app.py %{buildroot}%{_bindir}/pcn-calculator

# Install supporting files
install -m 644 calculator_engine.py %{buildroot}%{_datadir}/pcn-calculator/
install -m 644 history_manager.py %{buildroot}%{_datadir}/pcn-calculator/
install -m 644 theme_manager.py %{buildroot}%{_datadir}/pcn-calculator/
install -m 644 icon.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/pcn-calculator.png

# Install desktop entry
install -m 644 pcn-calculator.desktop %{buildroot}%{_datadir}/applications/

# Install documentation
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/ 2>/dev/null || true

%files
%{_bindir}/pcn-calculator
%{_datadir}/pcn-calculator/
%{_datadir}/applications/pcn-calculator.desktop
%{_datadir}/icons/hicolor/256x256/apps/pcn-calculator.png
%doc %{_docdir}/%{name}

%changelog
* %(date "+%%a %%b %%d %%Y") Pacan <pacan@example.com> - 1.0.1-1
- Fix icon loading to check system location for RPM installation
- Remove python3-customtkinter from RPM dependencies (install via pip)
- Update all references from Windows 11 style to modern style
- Fix changelog date warning in RPM spec

* %(date "+%%a %%b %%d %%Y") Pacan <pacan@example.com> - 1.0.0-1
- Initial release
