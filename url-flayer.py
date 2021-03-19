#!/usr/bin/env python3
'''
From: https://realpython.com/python-concurrency/#asyncio-version
'''
import argparse
import asyncio
import fileinput
import os
import re
import sys
import time

# pip3 install aiohttp
import aiohttp

parser = argparse.ArgumentParser(description=('https://github.com/scott-be/url-flayer'),
                                usage=f'usage: {sys.argv[0]} [options] domains.txt')

def print_banner():
    # TODO Fix
    banner = r'''
   |\                     /)
 /\_\\__               (_//
|   `>\-`     _._       //`)
 \ /` \\  _.-`:::`-._  //
  `    \|`    :::    `|/
        |     :::     |
        |.....:::.....|
        |:::::::::::::|
        |     :::     |
        \     :::     /
         \    :::    /
          `-. ::: .-'
           //`:::`\\
          //   '   \\
         |/         \\
 _     _ ______  _       _______ _
(_)   (_|_____ \(_)     (_______) |
 _     _ _____) )_       _____  | | _____ _   _ _____  ____
| |   | |  __  /| |     |  ___) | |(____ | | | | ___ |/ ___)
| |___| | |  \ \| |_____| |     | |/ ___ | |_| | ____| |
 \_____/|_|   |_|_______)_|      \_)_____|\__  |_____)_|
                                         (____/
'''

    print(banner)

def main(args):
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(check_urls(args))
    duration = time.time() - start_time
    print(f'\nCompleted in {duration} seconds')


async def send_request(session, url, success_only, no_error, pattern):
    try:
        async with session.head(url) as response:
            # Send GET if recive '405 Method Not Allowed'
            if response.status == 405:
                response = await session.get(url)

            if 200 <= response.status < 300:
                print(f'{tc.ITEM} {response.status:<16}{url}')

                if pattern:
                    await find_pattern(session, url, pattern)
            elif success_only:
                print(f'{tc.WARN} {response.status:<16}{url}')
    except asyncio.TimeoutError as e:
        if no_error:
            pass
        else:
            print(f'{tc.ERROR} {"Timeout":<16}{url}')
    except aiohttp.client_exceptions.InvalidURL as e:
        if no_error:
            pass
        else:
            print(f'{tc.ERROR} {"InvalidURL":<16}{url}')
    except aiohttp.client_exceptions.ClientConnectorError as e:
        if no_error:
            pass
        else:
            print(f'{tc.ERROR} {"ConnectorError":<16}{url}')
    except Exception as e:
        if no_error:
            pass
        else:
            print('Exception:', type(e).__name__)

async def find_pattern(session, url, pattern):
    try:
        async with session.get(url) as response:
            if re.search(pattern,  await response.text(), re.IGNORECASE):
                print(f'{tc.GREEN}{"Pattern match!":<16}{url}{tc.RST}')
    except Exception as e:
        print('Exception:', type(e).__name__)


async def check_urls(args):
    path = args.path.lstrip('/')
    timeout = aiohttp.ClientTimeout(total=args.timeout)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        tasks = []

        # Check for stdin
        if sys.stdin.isatty() and not args.domainfile:
            parser.print_help()
            sys.exit(1)

        for domain in fileinput.input(files=args.domainfile):
            url = os.path.join(domain.strip(), path).rstrip('/')
            task = asyncio.ensure_future(send_request(session, url, args.success_only, args.no_error, args.pattern))
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)

class tc:
    '''
    Class for terminal colors
    '''
    RED     = "\033[1;31m"
    GREEN   = "\033[0;32m"
    YELLOW  = "\033[0;33m"
    BLUE    = "\033[1;34m"
    MAGENTA = "\033[1;35m"
    CYAN    = "\033[1;36m"
    RST     = "\033[0;0m"
    BOLD    = "\033[;1m"
    REVERSE = "\033[;7m"
    BULLET  = f"{BLUE}[*]{RST}"
    ITEM    = f"{GREEN}[-]{RST}"
    WARN    = f"{YELLOW}[!]{RST}"
    ERROR   = f"{RED}[!]{RST}"

if __name__ == "__main__":
    # Parse Arguments
    print_banner()
    parser.add_argument('-p', type=str, dest='path', metavar='PATH', default='', help='path to append to URL')
    parser.add_argument('-t', type=float, dest='timeout', metavar='TIMEOUT', default=5, help='number of seconds to wait')
    parser.add_argument('--pattern', type=str, dest='pattern', metavar='REGEX', default='', help='optional regex pattern to search for in 2xx response')
    parser.add_argument('--success', dest='success_only', help='only print 2xx status codes', action='store_false')
    parser.add_argument('--noerror', dest='no_error', help='don\'t print errors', action='store_true')
    parser.add_argument('domainfile', metavar='FILE', nargs='*', help='domain file(s) to read from. stdin is used if empty')

    args = parser.parse_args()
    main(args)
