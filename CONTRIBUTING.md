# Contributing to SmechOS

Thanks for looking. SmechOS is an independent Linux distribution built from
scratch — not a fork of any existing distro — so contributing looks a little
different from a typical application project. This page explains how.

**This repository holds issues only.** The build system lives in
[spk-compile](https://github.com/Smech-Labs/spk-compile); that is where code
changes go.

---

## Two ways to help

### 1. Test the ISO (no build environment needed)

The most useful thing right now. Boot a release image on real hardware or in
a VM and report what breaks. You need no toolchain, no source tree, and no
prior knowledge of the codebase.

Especially valuable:

- **Real hardware.** Almost all testing so far has been under QEMU/KVM.
  Wi-Fi, GPUs, laptop function keys, suspend/resume, external displays and
  audio are effectively untested outside a VM.
- **Boot failures**, with a photo of the screen or serial output.
- **Missing components.** Several bugs were found simply by opening a menu
  and noticing something absent.

When reporting, please include: hardware (or VM and its flags), what you
expected, what happened, and relevant output from
`journalctl -b | grep -iE 'error|failed|segfault'`.

### 2. Fix a packaging bug (small change, bounded effort)

Many open issues are one line: a package that was never added to a component
list. Look for the `good first issue` label.

The catch is that verifying such a change normally means rebuilding a
distribution. It doesn't have to — `build-one.sh` compiles a single package
against a rootfs you already have:

```bash
git clone https://github.com/Smech-Labs/spk-compile
cd spk-compile
./build-one.sh spectacle 6.7.2 /path/to/rootfs
```

Requirements: `podman`, `sudo`, ~6 GB free, and an extracted rootfs. Full
setup instructions, including why builds run in a container, are in the
[spk-compile README](https://github.com/Smech-Labs/spk-compile#readme).

---

## Two things that will save you an afternoon

**KDE ships on two release tracks with different version numbers.** Plasma
packages (`kwin`, `spectacle`) use versions like `6.7.2`. KDE Gear
applications (`konsole`, `dolphin`) use versions like `25.08.3` and live
under a different URL. Guessing wrong gives a 404 that looks like the package
doesn't exist. Pass `--gear` for Gear packages.

**Test with the right QEMU flags.** Use `-device virtio-vga-gl`, not
`-device virtio-vga`. Without the `-gl` variant there is no virgl, Mesa falls
back to llvmpipe, llvmpipe currently segfaults in a loop, and you get a black
screen that looks like your change broke everything when it didn't. This has
cost real debugging time; see issue #2.

---

## Filing a good issue

The existing issues are the template. What makes them useful:

- **Evidence over description.** Paste the actual log line or command output.
- **A reproduction.** Exact steps, including VM flags.
- **Root cause if you found it** — even "this package isn't in the list in
  `spk-compile.py`" is enormously helpful.
- **What you already ruled out.** Saves the next person repeating it.

Please search open issues first; several near-identical packaging gaps are
already tracked, and issue #14 lists everything currently known to be missing.

---

## Pull requests

PRs go to [spk-compile](https://github.com/Smech-Labs/spk-compile), not here.

- Reference the issue number.
- Say how you verified it. "Built with `build-one.sh`, booted, confirmed the
  journal error is gone" is ideal. If you couldn't verify, say so — an
  unverified fix is still welcome, just label it honestly.
- Match the surrounding style. `spk-compile.py` comments explain *why* a
  workaround exists, often citing the exact error it prevents. Please keep
  that up; several of those comments have already stopped bugs from
  being reintroduced.

---

## Privacy and attribution

This project is maintained pseudonymously. Please don't include real names,
email addresses or other personal information belonging to anyone in issues,
commits or code. Contributions are attributed by whatever name you commit
under.

## License

MIT — see [LICENSE](LICENSE). By contributing you agree your work is
released under the same terms.
