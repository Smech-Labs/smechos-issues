# smechos-issues

Bug tracker and feature request tracker for **SmechOS**.

## SmechOS is independent

SmechOS is an independent Linux distribution, built from scratch by
Smech Labs through the `spk-compile` pipeline — a systemd/glibc base, a
custom kernel, KDE Plasma as the desktop, and `spk` as its own package
manager. It is not a fork or derivative of ChromiumOS, Ubuntu, Fedora, or
any other distribution, and it is not affiliated with, endorsed by, or
sponsored by any of those projects or their vendors.

This repository exists **only** to track bug reports and feature requests for
SmechOS. There is no code, no build tooling, and no documentation here beyond
this README.

## Where everything else lives

- Build tooling and source: [Smech-Labs/spk-compile](https://github.com/Smech-Labs/spk-compile) (SmechDeploy is EoL, superseded by spk-compile)
- Binary packages: [Smech-Labs/spk-repo-gun](https://gerrithub.io/) (GerritHub)
- Build-reference rootfs export: [Smech-Labs/smechdeploy-build-reference](https://github.com/Smech-Labs/smechdeploy-build-reference)
- Documentation: [docs.smech.xyz](https://docs.smech.xyz)
- Downloads: [os.smech.xyz](https://os.smech.xyz)
- Mailing list (SLML): `smechlabs@googlegroups.com` — open, public conversation archive; subscribe for development discussion and release announcements

## Reporting a bug or requesting a feature

Open an issue here using one of the provided templates.

For **security vulnerabilities** specifically (a suspected deliberate
backdoor, an obfuscated change, or similar) — do **not** open a public
issue. See [CONTRIBUTING.md](https://github.com/Smech-Labs/.github/blob/main/CONTRIBUTING.md)
for the private reporting process.

## Want to contribute code?

Issues labeled [`good first issue`](https://github.com/Smech-Labs/smechos-issues/labels/good%20first%20issue)
are scoped specifically for newcomers — start there.
