on run argv
	set trk to add_track(item 1 of argv)
	tell application "Music"
		set played count of trk to item 2 of argv
	end tell
end run

on add_track(t)
	set t to (POSIX path of ((path to me as text) & "::")) & t
	tell application "Music"
		return add t
	end tell
end add_track