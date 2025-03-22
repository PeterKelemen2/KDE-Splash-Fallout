from enum import Enum
import os
import platform
import subprocess


class Info(Enum):
    LINUX = 1
    KERNEL = 2
    DE = 3
    BASH = 4
    PHYS_MEM = 5


def get_linux_version():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.strip().split("=")[1].strip('"')
    except FileNotFoundError:
        return "Unknown"


def get_kernel_version():
    return platform.release()


def get_desktop_environment():
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "Unknown")
    session = os.environ.get("XDG_SESSION_DESKTOP", "Unknown")
    window_manager = os.environ.get("XDG_SESSION_TYPE", "Unknown")

    return f"Session: {session}, WM: {window_manager}"


def get_bash_version():
    try:
        result = subprocess.run(["bash", "--version"], capture_output=True, text=True)
        return result.stdout.split()[3]  # Get only the version number
    except FileNotFoundError:
        return "Bash not found"


def get_total_memory_proc():
    with open("/proc/meminfo") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                return f"{int(line.split()[1]) // 1024}M"  # Convert kB to MB


def get_system_info():
    system_info = {
        Info.LINUX: get_linux_version(),
        Info.KERNEL: get_kernel_version(),
        Info.DE: get_desktop_environment(),
        Info.BASH: get_bash_version(),
        Info.PHYS_MEM: get_total_memory_proc(),
    }

    return system_info


def create_terminal_string(same_length=False, tab=False, tab_length = 4):
    sys_info = get_system_info()
    terminal_string = ""

    tab_string = "" + (" " * tab_length) if tab else ""
    lines = [
        f"******** {sys_info.get(Info.LINUX).upper()} ********",
        "",
        f"{tab_string}COPYRIGHT 2075 ROBCO(R)",
        f"{tab_string}KERNEL {sys_info.get(Info.KERNEL).upper()}",
        f"{tab_string}BASH VERSION {sys_info.get(Info.BASH).upper()}",
        f"{tab_string}{sys_info.get(Info.PHYS_MEM).upper()} RAM SYSTEM",
        f"{tab_string}{sys_info.get(Info.DE).upper()}",
        f"{tab_string}NO HOLOTAPE FOUND",
        f"{tab_string}LOAD ROM(1): DEITRIX 303",
        "",
        ""
    ]

    if same_length:
        max_length = max(len(line) for line in lines)
        padded_lines = [line.ljust(max_length) for line in lines]

        terminal_string = "\n".join(padded_lines)
    else:
        terminal_string = "\n".join(lines)

    return terminal_string
