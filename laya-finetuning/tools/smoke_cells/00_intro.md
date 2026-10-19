# Plan A: smoke test

Proves the whole pipeline end to end on 20 dummy rows: install, download the English checkpoint, dry-run, train 1 epoch, reload, predict, save to Drive, and (later, on your PC) load it on CPU through `laya_adapter`.
**This tests plumbing only. The numbers mean nothing about quality.**

How to use it: run the cells **top to bottom, one at a time**. Each code cell starts with a comment saying what you should see. If something differs, paste the output back to Claude. After a kernel restart, re-run cell 1 first (it holds the settings), then continue from where you were.

Nothing here overwrites the original checkpoint: training reads a downloaded copy in `/content/work/base-english` and writes to a new folder.
