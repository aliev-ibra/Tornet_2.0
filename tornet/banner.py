#!/usr/bin/python
red = "\033[91m"
white = "\033[97m"
reset = "\033[0m"

def print_banner():
    banner = f"""
{white} +-------------------------------------------------------+
{white} |{red} ████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗████████╗{white} |
{white} |{red} ╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝╚══██╔══╝{white} |
{white} |{red}    ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   {white} |
{white} |{red}    ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   {white} |
{white} |{red}    ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗   ██║   {white} |
{white} |{red}    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   {white} |
{white} +--------------------({red}ALIEV{white})---------------------------+
{white} +--------------({red}Improved by Ibrahim Aliyev{white})--------------------+
{reset}
"""
    print(banner)

if __name__ == "__main__":
    print_banner()

