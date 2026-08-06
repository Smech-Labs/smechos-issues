# How to file a good SmechOS issue

A good issue is one someone else can act on without asking you follow-up
questions. This page shows what that looks like for SmechOS specifically.

**You do not need to know how to fix a bug to report it well.** Testing the
ISO and reporting precisely what happened is the single most useful
contribution right now — the project has had almost no testing outside a VM.

Templates are provided when you open a new issue. This page explains what to
put in them and why.

---

## Before you file

**Search open issues.** Many packaging gaps are already tracked, and
[#14](https://github.com/Smech-Labs/smechos-issues/issues/14) lists every
component currently known to be missing. If your bug is "X is not
installed", check there first.

**Note which image you are on.** Include the release (e.g. `1.0-RC2`) and,
ideally, the SHA256 you downloaded.

---

## What to include

### 1. What you did, what you expected, what happened

Three short sentences beat three paragraphs.

> Opened System Settings and looked for "About this System". Expected a page
> showing the distro version. There is no such entry in the sidebar.

### 2. How you booted it

This matters more for SmechOS than for most projects, because the wrong
QEMU flags produce a black screen that looks like total failure but isn't.

- **Real hardware**: make, model, CPU, GPU, and how you booted (USB, UEFI or
  BIOS, Secure Boot on/off)
- **VM**: the full command line

> ```
> qemu-system-x86_64 -enable-kvm -m 4096 -smp 4 -machine q35 \
>     -cdrom SmechOS-1.0-RC2.iso \
>     -device virtio-vga-gl -display egl-headless,gl=on -vnc :1
> ```

If you used `-device virtio-vga` **without** `-gl`, say so — Mesa then falls
back to llvmpipe, which currently segfaults in a loop
([#2](https://github.com/Smech-Labs/smechos-issues/issues/2)), and that alone
explains a black screen.

### 3. Evidence — the part that matters most

Paste the actual output. A log line is worth more than a paragraph
describing it.

```bash
journalctl -b --no-pager | grep -iE 'error|failed|segfault' | tail -40
```

Useful specifics depending on the bug:

| Symptom | Useful command |
|---|---|
| Graphics / black screen | `dmesg \| grep -iE 'drm\|virgl\|cap sets'` |
| A component seems missing | `ls /usr/bin/<name>` and `journalctl -b \| grep -i <name>` |
| Desktop doesn't appear | `journalctl -b \| grep -i plasmashell` |
| Crash | `journalctl -b \| grep -i segfault` |

Log in on the live image with `root` / `smech` (documented debug credentials
— see the release notes for scope).

**Photos are fine.** If it fails before you can get a shell, a phone photo of
the screen is genuinely useful. Don't skip reporting because you couldn't
capture text.

### 4. Root cause, if you found one

Optional, and very welcome. Even "this package isn't in the list in
`spk-compile.py`" saves the next person an hour.

### 5. What you already ruled out

Saves others repeating your work. "Also happens with `nomodeset`" or "same on
a second machine" is valuable.

---

## A worked example

Compare:

> **Bad:** "Desktop doesn't work, just black."

with:

> **Good:** Booted RC2 in QEMU with `-device virtio-vga-gl -display
> egl-headless,gl=on -vnc :1`. Reached a cursor on a black screen; the cursor
> moves but no panel or wallpaper ever appears.
>
> `journalctl -b | grep -i plasmashell` shows:
>
> ```
> kde.plasmashell: Aborting shell load: The activity manager daemon
>                  (kactivitymanagerd) is not running.
> ```
>
> `find /usr -name '*kactivitymanagerd*'` returns nothing, though
> `libPlasmaActivities.so.6.7.2` is present. Graphics look fine —
> `[drm] features: +virgl` and no segfaults — so this seems to be a missing
> package rather than a GPU problem.

The second one contains the diagnosis. That was
[#1](https://github.com/Smech-Labs/smechos-issues/issues/1), and it was fixed
directly from that evidence.

---

## What is especially wanted

- **Real hardware reports.** Wi-Fi, GPUs, suspend/resume, function keys,
  external displays, audio — essentially untested outside QEMU.
- **Boot failures**, with a photo or serial output.
- **Missing components.** Several bugs were found simply by opening a menu
  and noticing something absent. That is a legitimate and useful way to
  contribute.
- **Installer results** — Calamares has had far less testing than the live
  session.

## What is not a bug

- Missing packages already listed in
  [#14](https://github.com/Smech-Labs/smechos-issues/issues/14) — comment
  there instead of opening a duplicate
- The `root` / `smech` debug login: deliberate and documented for RC images
- Anything on the release notes' known-issues list, unless you have new
  detail

---

## Privacy

Please don't include real names, email addresses, serial numbers, MAC
addresses, IPs or other personal information in issues or logs — yours or
anyone else's. Redact before pasting.

---

## Want to fix it too?

See [CONTRIBUTING.md](CONTRIBUTING.md). Most open issues are one-line changes
to a component list, and
[`build-one.sh`](https://github.com/Smech-Labs/spk-compile) verifies such a
change in minutes rather than a full distribution rebuild.
