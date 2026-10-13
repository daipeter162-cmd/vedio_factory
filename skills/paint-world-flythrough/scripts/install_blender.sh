#!/usr/bin/env bash
# Isolated Debian/Ubuntu portable Blender. No global package installation.
set -euo pipefail
dest="$(realpath -m "${1:?Pass a runtime output directory}")"
command -v apt-get >/dev/null
command -v dpkg-deb >/dev/null
mkdir -p "$dest/archives/partial" "$dest/root"
# NoLocking applies only to a download-only operation, never a package mutation.
apt-get -o APT::Sandbox::User="$(id -un)" -o Debug::NoLocking=true \
  -o Dir::Cache::archives="$dest/archives" --download-only install -y blender
for package in "$dest"/archives/*.deb; do dpkg-deb -x "$package" "$dest/root"; done
cat > "$dest/blender" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
runtime="$(cd "$(dirname "$0")" && pwd)"
# Restore the executable from the package if a workspace snapshot truncates it.
for package in "$runtime"/archives/blender_[0-9]*.deb; do dpkg-deb -x "$package" "$runtime/root"; done
export LD_LIBRARY_PATH="$runtime/root/usr/lib:$runtime/root/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export BLENDER_SYSTEM_SCRIPTS="$runtime/root/usr/share/blender/scripts"
export BLENDER_SYSTEM_DATAFILES="$runtime/root/usr/share/blender/datafiles"
exec "$runtime/root/usr/bin/blender" "$@"
SH
chmod +x "$dest/blender"
"$dest/blender" --version
