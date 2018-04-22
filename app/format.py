try:
    from emoji2text import emoji2text
except ImportError:
    # If emoji2text isn't installed, we still want it to work
    emoji2text = lambda x, *_: x

def format(msg, width):
    msg = swap_emoji(msg)
    msg = swap_unicode(msg)
    msg = remove_unknowns(msg)
    msg = break_lines(msg, width)

    return msg

def swap_emoji(msg):
    return emoji2text(msg, '[', ']')

# It's recommended to swap some ascii characters with representative unicode
#  such as opening and closing Quotation marks, or dashes in between words.
# This attempts to revert some of the more common swaps so we can print it.

UNICODE_SWAPS = {
    chr(0x201C): '"',
    chr(0x201D): '"',
    chr(0x2018): "'",
    chr(0x2019): "'",
    chr(0x2010): "-",
    chr(0x2012): "-",
    chr(0x2013): "-"
}

def swap_unicode(msg):
    def generate_fixed_msg(msg, mapping):
        for c in msg:
            try:
                yield mapping[c]
            except KeyError:
                yield c

    return ''.join(generate_fixed_msg(msg, UNICODE_SWAPS))

# Anything outside ASCII range (128) is going to cause problems, so just swap
#  it with a '?'

def remove_unknowns(msg):
    def fill_in_unknowns(msg):
        for c in msg:
            if ord(c) < 128:
                yield c
            else:
                yield '?'
    return ''.join(fill_in_unknowns(msg))

def find_breakpoint(line, width):
    breakpoint = line[:width].rfind(' ')
    if breakpoint != -1:
        return breakpoint
    return width

def break_lines(msg, width):
    def break_line(line, width):
        while len(line) > width:
            breakpoint = find_breakpoint(line, width)
            yield line[:breakpoint]
            line = line[breakpoint + 1:]
        yield line

    return '\n'.join('\n'.join(break_line(l, width)) for l in msg.split('\n'))
