# Jeolinux Question Bank - MVP

## Q001 [basic] [fill-blank]
**Question:** List files in long format with human-readable sizes:

```bash
ls -__ /var/log
```

**Answer:** lh
**Explanation:** `-l` for long format (permissions, owner, size), `-h` for human-readable sizes (1K, 234M, 2G). Combine: `ls -lh` or `ls -l -h`.

---

## Q002 [basic] [multiple-choice]
**Question:** What does `chmod 755` mean?

**Options:**
A) Owner: rwx, Group: rx, Others: rx
B) Owner: rw, Group: r, Others: r
C) Owner: rwx, Group: rwx, Others: rwx
D) Owner: r, Group: rx, Others: rx

**Answer:** A
**Explanation:** 7=rwx (4+2+1), 5=r-x (4+0+1). Pattern: owner-group-others. 755 = owner full access, group/others read+execute.

---

## Q003 [basic] [fill-blank]
**Question:** Find files modified in last 7 days:

```bash
find /home -mtime -__
```

**Answer:** 7
**Explanation:** `-mtime -7` = modified within 7 days. `-mtime +7` = older than 7 days. `-mtime 7` = exactly 7 days ago.

---

## Q004 [intermediate] [multiple-choice]
**Question:** What's the difference between `>` and `>>`?

**Options:**
A) > appends, >> overwrites
B) > overwrites, >> appends
C) No difference
D) > for stdout, >> for stderr

**Answer:** B
**Explanation:** `>` truncates file and writes (destroys existing content). `>>` appends to file (preserves existing content). `2>` redirects stderr.

---

## Q005 [basic] [multiple-choice]
**Question:** Which command shows disk usage by directory?

**Options:**
A) df -h
B) du -sh *
C) ls -lh
D) free -h

**Answer:** B
**Explanation:** `du -sh *` shows size of each item in current directory. `df -h` shows filesystem space (mounted partitions). `free -h` shows RAM usage.

---

## Q006 [intermediate] [fill-blank]
**Question:** Search for text in files recursively:

```bash
grep -__ "error" /var/log/
```

**Answer:** r
**Explanation:** `-r` or `-R` for recursive search through directories. Add `-i` for case-insensitive, `-n` for line numbers, `-v` for inverse match (exclude).

---

## Q007 [gotcha] [multiple-choice]
**Question:** You run `rm -rf /`. What happens?

**Options:**
A) Deletes everything (catastrophic)
B) Requires --no-preserve-root flag
C) Permission denied
D) Only deletes current directory

**Answer:** B
**Explanation:** Modern systems require `rm -rf --no-preserve-root /` to prevent accidents. Without flag, deletion refused. Still, never run this even with flag!

---

## Q008 [basic] [multiple-choice]
**Question:** What does `ps aux` show?

**Options:**
A) Disk partitions
B) Network connections
C) All running processes
D) System logs

**Answer:** C
**Explanation:** `ps aux` lists all processes with detailed info (user, PID, CPU%, MEM%, command). `a` = all users, `u` = user-oriented format, `x` = include processes without TTY.

---

## Q009 [intermediate] [fill-blank]
**Question:** Kill process by name pattern:

```bash
_______ firefox
```

**Answer:** pkill
**Explanation:** `pkill` kills by name/pattern. Alternative: `killall firefox` (exact name only). `kill` requires PID: `kill $(pgrep firefox)`.

---

## Q010 [basic] [multiple-choice]
**Question:** What permission is needed to `cd` into a directory?

**Options:**
A) Read (r)
B) Write (w)
C) Execute (x)
D) Read + Write

**Answer:** C
**Explanation:** Execute (x) permission required to enter directory. Read (r) needed to list contents. Write (w) needed to create/delete files inside.

---

## Q011 [intermediate] [multiple-choice]
**Question:** What does `tail -f /var/log/messages` do?

**Options:**
A) Shows last 10 lines and exits
B) Shows first 10 lines
C) Continuously shows new lines as written
D) Counts lines in file

**Answer:** C
**Explanation:** `-f` follows file, showing new lines in real-time. Essential for log monitoring. Ctrl+C to exit. Alternative: `less +F` (can pause with Ctrl+C).

---

## Q012 [basic] [fill-blank]
**Question:** Change file owner:

```bash
______ user:group /path/file
```

**Answer:** chown
**Explanation:** `chown user:group file` changes owner and group. Can use separately: `chown user file` or `chgrp group file`. Requires root/sudo.

---

## Q013 [gotcha] [scenario]
**Question:** You run `chmod 777 ~/.ssh/id_rsa`. SSH refuses to use key. Why?

**Options:**
A) Key corrupted
B) Permissions too open (world-readable)
C) Wrong key format
D) SSH agent not running

**Answer:** B
**Explanation:** SSH requires private keys be readable ONLY by owner (600 or 400). 777 = everyone can read. Security risk. Fix: `chmod 600 ~/.ssh/id_rsa`.

---

## Q014 [intermediate] [multiple-choice]
**Question:** What does `systemctl status sshd` show?

**Options:**
A) SSH connections
B) Service status (active/inactive/failed)
C) SSH configuration
D) User login history

**Answer:** B
**Explanation:** Shows service state (active/running, inactive/dead, failed), recent logs, PID, memory usage. Part of systemd service management.

---

## Q015 [basic] [fill-blank]
**Question:** Compress directory into tarball:

```bash
tar -____ backup.tar.gz /home/user
```

**Answer:** czf
**Explanation:** `c` create, `z` gzip compress, `f` filename. Order matters: `-czf file.tar.gz source`. Extract: `tar -xzf file.tar.gz`.

---

## Q016 [intermediate] [multiple-choice]
**Question:** How do you check which process is listening on port 8080?

**Options:**
A) netstat -tulpn | grep 8080
B) ps aux | grep 8080
C) lsof :8080
D) top -p 8080

**Answer:** A
**Explanation:** `netstat -tulpn` or `ss -tulpn` shows listening ports with PIDs. Requires root/sudo for PID info. Alternative: `lsof -i :8080`.

---

## Q017 [basic] [multiple-choice]
**Question:** What does `df -h` show?

**Options:**
A) Directory sizes
B) Filesystem space usage (mounted partitions)
C) File permissions
D) Disk hardware info

**Answer:** B
**Explanation:** Shows mounted filesystems with total/used/available space and mount points. `-h` for human-readable. Use `du` for directory sizes.

---

## Q018 [gotcha] [multiple-choice]
**Question:** You set `export PATH=/usr/local/bin`. What happens?

**Options:**
A) Adds /usr/local/bin to PATH
B) Replaces PATH entirely (breaks system)
C) No effect
D) Syntax error

**Answer:** B
**Explanation:** Assignment without `$PATH` destroys existing PATH. Correct: `export PATH=/usr/local/bin:$PATH` (prepend) or `export PATH=$PATH:/usr/local/bin` (append).

---

## Q019 [intermediate] [fill-blank]
**Question:** Check if port 22 is open on remote host:

```bash
nc -zv example.com __
```

**Answer:** 22
**Explanation:** `nc -zv host port` tests connectivity. `-z` scan without data, `-v` verbose. Returns open/closed. Alternative: `telnet host port` (deprecated).

---

## Q020 [basic] [multiple-choice]
**Question:** What does `sudo !!` do?

**Options:**
A) Repeat last command as root
B) Repeat last sudo command
C) Show sudo history
D) Syntax error

**Answer:** A
**Explanation:** `!!` expands to last command. Common pattern: run command, get permission denied, then `sudo !!` to retry as root.

---

## Q021 [intermediate] [multiple-choice]
**Question:** What's the difference between `kill` and `kill -9`?

**Options:**
A) kill -9 is faster
B) kill allows graceful shutdown, kill -9 forces immediate termination
C) No difference
D) kill -9 only works on root processes

**Answer:** B
**Explanation:** `kill` (SIGTERM/15) asks process to terminate gracefully. `kill -9` (SIGKILL) forces immediate kill (can't be caught). Use kill first, -9 as last resort.

---

## Q022 [basic] [fill-blank]
**Question:** Show last 20 lines of file:

```bash
tail -__ /var/log/syslog
```

**Answer:** 20
**Explanation:** `tail -n 20` or `tail -20` shows last 20 lines. Default is 10. Opposite: `head -n 20` for first 20 lines.

---

## Q023 [intermediate] [multiple-choice]
**Question:** How do you redirect stderr to stdout?

**Options:**
A) 2>&1
B) 1>&2
C) 2>1
D) stderr=stdout

**Answer:** A
**Explanation:** `2>&1` redirects file descriptor 2 (stderr) to 1 (stdout). Common: `command > file 2>&1` (both to file). Order matters.

---

## Q024 [gotcha] [scenario]
**Question:** You run `nohup python app.py &`. After logout, process dies. Why?

**Options:**
A) nohup doesn't work with Python
B) Missing output redirection
C) Need to use screen/tmux instead
D) Terminal still attached to process

**Answer:** D
**Explanation:** `&` backgrounds process but keeps terminal attached. Logout sends SIGHUP. Fix: `nohup python app.py > app.log 2>&1 &` or use systemd service.

---

## Q025 [basic] [multiple-choice]
**Question:** What does `uname -a` show?

**Options:**
A) Current user
B) System info (kernel, hostname, architecture)
C) Uptime
D) User list

**Answer:** B
**Explanation:** Shows kernel name, version, hostname, architecture, OS. Useful for checking system details. `uname -r` for kernel version only.

---

## Q026 [intermediate] [fill-blank]
**Question:** Find files larger than 100MB:

```bash
find / -size +____
```

**Answer:** 100M
**Explanation:** `-size +100M` finds files over 100MB. `+` for greater, `-` for less. Units: `k` (KB), `M` (MB), `G` (GB). Example: `-size -1G` (under 1GB).

---

## Q027 [basic] [multiple-choice]
**Question:** How do you check SELinux status?

**Options:**
A) selinux status
B) getenforce
C) sestatus
D) systemctl status selinux

**Answer:** B or C
**Explanation:** `getenforce` shows mode (Enforcing/Permissive/Disabled). `sestatus` shows detailed status. Change mode: `setenforce 0` (permissive) or `setenforce 1` (enforcing).

---

## Q028 [intermediate] [multiple-choice]
**Question:** What does `awk '{print $1}' file.txt` do?

**Options:**
A) Prints first line
B) Prints first column/field of each line
C) Searches for pattern $1
D) Counts characters

**Answer:** B
**Explanation:** `awk` processes text field-by-field. `$1` = first field (default separator: whitespace). `$2` = second field. `$0` = entire line.

---

## Q029 [gotcha] [multiple-choice]
**Question:** You run `cd /tmp && rm -rf *`. Script fails at rm. What happens?

**Options:**
A) cd doesn't execute
B) cd succeeds, rm fails, pwd still /tmp
C) Both fail
D) Directory deleted anyway

**Answer:** B
**Explanation:** `&&` continues only if first command succeeds. `cd` worked, `rm` failed. Current directory changed. Use `cd /tmp || exit` in scripts to fail fast.

---

## Q030 [intermediate] [fill-blank]
**Question:** Replace text in file (in-place):

```bash
sed -__ 's/old/new/g' file.txt
```

**Answer:** i
**Explanation:** `-i` edits file in-place. Without it, prints to stdout. `s/old/new/g`: `s` substitute, `g` global (all occurrences). Add `.bak` for backup: `-i.bak`.