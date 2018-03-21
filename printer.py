from Adafruit_Thermal import Adafruit_Thermal

class Printer(Adafruit_Thermal):

    def format_print(self, message):
        for line in message.split("\n"):
            self._set_heading(line)

            for c in self._parse_line(line):
                if c:
                    self.writeBytes(ord(c))

            self._unset_heading(line)
            self.normal()

        self.feed(3)

    def _set_heading(self, line):
        # lines that start with "#" become headings
        if line.strip().startswith("#"):
            self.doubleHeightOn()

    def _unset_heading(self, line):
        # lines that start with "#" become headings
        if line.strip().startswith("#"):
            self.doubleHeightOff()

    def _parse_line(self, line):
        liter = enumerate(iter(line))
        # We need to check what formatting is being used on this line right now
        line_in_groups = {k: False for k in "*_~"}
        try:
            while True:
                i, c = next(liter)
                if self._is_escape(c):
                    # don't parse the next character
                    i, c = next(liter)
                else:
                    c = self._parse_char(i, line, line_in_groups)
                yield c

        except StopIteration:
            pass

    def _is_escape(self, c):
        return c == "/"

    def _parse_char(self, i, line, line_in_groups):
        SYMBOLS = {
            "*": self.BOLD_MASK,
            "_": self.INVERSE_MASK,
            "~": self.STRIKE_MASK
        }
        is_symbol = False
        for symbol, mask in SYMBOLS.items():
            if self._is_group_start(symbol, i, line, line_in_groups[symbol]):
                self.setPrintMode(mask)
                line_in_groups[symbol] = True
                is_symbol = True
            elif self._is_group_end(symbol, i, line, line_in_groups[symbol]):
                self.unsetPrintMode(mask)
                line_in_groups[symbol] = False
                is_symbol = True

        # If this is a symbol, then we don't actually want to print any character
        if is_symbol:
            return ''
        else:
            return line[i]

    def _is_group_start(self, symbol, i, line, in_group):
        char = line[i]
        if char == symbol and not in_group:
            # We could be at the start of the group
            # It's a group if there's another occurance
            return symbol in line[i+1:]
        return False

    def _is_group_end(self, symbol, i, line, in_group):
        char = line[i]
        return char == symbol and in_group

