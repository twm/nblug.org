#!/usr/bin/env python2.7

import argparse
from datetime import date, timedelta
import os
from string import Template, ascii_letters, digits
import sys


TUESDAY = 1

TEMPLATE = Template("""\
Tags: general meeting
Event: ${date} 7:00 pm to 8:30 pm
Speaker: ${speaker}
Location: Sonic
Author: ${author}

${body}
""")

parser = argparse.ArgumentParser()
parser.add_argument('--hackfest', default=False, action='store_true', help="Prefill as a hackfest.")


def sanitize(s):
    """
    Produce a URL-safe version of a string.
    """
    safe = ascii_letters + digits + "_-"
    return "-".join("".join(c if c in safe else " " for c in s).lower().split())


def next_second_tuesday(today):
    """
    >>> next_second_tuesday(date(2015, 3, 1))
    '2015-03-10'
    >>> next_second_tuesday(date(2014, 10, 20))
    '2014-11-11'
    >>> next_second_tuesday(date(2014, 11, 11))
    '2014-11-11'
    >>> next_second_tuesday(date(2014, 12, 29))
    '2015-01-13'
    """
    d = today.replace(day=1)
    tuesdays = 0
    while True:
        if d.weekday() == TUESDAY:
            tuesdays += 1
        if tuesdays >= 2:
            break
        d = d + timedelta(days=1)
    if d < today:
        while d.month == today.month:
            d = d + timedelta(days=1)
        tuesdays = 0
        while True:
            if d.weekday() == TUESDAY:
                tuesdays += 1
            if tuesdays >= 2:
                break
            d = d + timedelta(days=1)
    return d.isoformat()


def prompt(query, default=""):
    if default:
        suffix = " [{}] ".format(default)
    else:
        suffix = " "
    return raw_input(query + suffix) or default


def get_gecos():
    try:
        import pwd
    except ImportError:
        return ""

    try:
        passwd = pwd.getpwuid(os.getuid())
    except KeyError:
        return ""

    return passwd[4].split(',')[0]


def main():
    is_hackfest = parser.parse_args().hackfest

    talk_date = prompt(
        "What's the date of the talk?",
        default=next_second_tuesday(date.today()),
    )
    if is_hackfest:
        title = "Lightning Talks & Hackfest"
        speaker = "Everyone"
        body = (
            "**Lightning Talks:** Have something you would like to present, but don't have enough material for a full talk?  Here's your chance.  Talk about anything Linux related.\n"
            "\n"
            "**Hackfest:** Bring your hardware or software project to get help with it or just to show it off. A mix of free tech support, show-and-tell, and idle chat.\n"
        )
    else:
        title = prompt("What is the title of the talk?")
        speaker = prompt("Who's the speaker?")
        body = ""

    author = prompt("What is *your* name?", default=get_gecos())

    lines = ['Title: {}'.format(title)]
    if is_hackfest:
        # There are a number of posts with the title of hackfest, so we must
        # give new ones a unique slug to avoid collision.
        lines.append(date.today().strftime('Slug: hackfest-%Y-%m'))
    lines.append(TEMPLATE.substitute(date=talk_date, speaker=speaker, author=author, body=body))
    s = '\n'.join(lines)
    filepath = 'content/news/{}-{}.md'.format(
        date.today().strftime('%Y-%m-%d'),
        sanitize(title),
    )
    if os.path.exists(filepath):
        print("Can't create file; would overwrite {}".format(filepath))
        sys.exit(1)
    with open(filepath, 'w') as f:
        f.write(s)

    editor = os.environ.get('EDITOR', 'vim') or 'vim'
    args = [editor, filepath]
    if 'vim' in editor:
        # Automatically jump to the last line if we know it's vim.
        args += ['+{}'.format(len(s.splitlines()))]

    sys.stdout.flush()  # Always flush before exec.
    os.execvp(editor, args)


if __name__ == '__main__':
    main()
