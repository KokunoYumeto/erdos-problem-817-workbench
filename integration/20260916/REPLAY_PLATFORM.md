# Replay platform note

The delivered replay commands and their existing CI were verified on Linux.
On native Windows, some inherited Path.write_text calls emit CRLF while the
byte-reference receipts use LF. The integration review preserved this failure,
then reran the unchanged mathematical producer and auditor code and checked exact
parsed values and the explicit line-ending transport. Ordinary and optimized
runs agreed. The sources are not silently rewritten here, and the original
unmodified full byte replay is not claimed to pass on Windows. See the review
for the precise files and checks. Use Linux/WSL for the original byte replay.
