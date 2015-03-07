#!/usr/bin/env python2.7

from datetime import date, timedelta
import os
from string import Template
import sys


TUESDAY = 1

TEMPLATE = Template("""\
Title: ${title}
Tags: general meeting
Event: ${date} 7:30 pm to 9:00 pm
Speaker: ${speaker}
Location: O'Reilly Media
Author: ${author}


""")


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


def main():
    title = raw_input("What is the title of the talk? ")
    default_talk_date = next_second_tuesday(date.today())
    talk_date = raw_input("What's the date of the talk? [{}] ".format(
        default_talk_date)) or default_talk_date
    speaker = raw_input("Who's the speaker? ")
    author = raw_input("What is *your* name? ")

    s = TEMPLATE.substitute(title=title, date=talk_date, speaker=speaker,
                            author=author)
    filepath = 'content/news/{}-{}.md'.format(
        date.today().strftime('%Y-%m-%d'),
        '-'.join(title.lower().split()),
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
