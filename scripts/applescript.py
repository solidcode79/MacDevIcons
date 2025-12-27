def generate_applescript(run_bin: str) -> str:

    return f'''\
property RUN_BIN : "{run_bin}"

on run
    do shell script RUN_BIN & " &"
end run

on open theFiles
    repeat with f in theFiles
        set p to quoted form of POSIX path of f
        do shell script RUN_BIN & " " & p & " &"
    end repeat
end open
'''