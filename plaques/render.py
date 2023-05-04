    def ansi_transition(self, other: "CharCell") -> str:
        """Change style and color between `self` and `other`.

        Return a sequence of ANSI SGR escape codes necessary to transition
        from the colors and styles of CharCell `self` to the colors and
        styles of CharCell `other`. The codes are to be printed in between
        the characters form char attributes of the CharCells.

        If the CharCell colors and styles are the same, an empty string is
        returned.

        See en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
        for details.
        """
        _escseq = "\033["
        if self.color != other.color:
            _colorcode = other.color if other.color else "n"
            #return to normal color if the next char's color is unspecified
            _escseq = _escseq + "3" + str(self.COLORNUM[_colorcode]) + ";"
        if self.bgcol != other.bgcol:
            _bgcolcode = other.bgcol if other.bgcol else "n" #see above
            _escseq = _escseq + "4" + str(self.COLORNUM[_bgcolcode]) + ";"
        if self.bold != other.bold:
            _escseq = _escseq + "1;" if other.bold else _escseq + "21;"
        if self.ulined != other.ulined:
            _escseq = _escseq + "4;" if other.bold else _escseq + "24;"
        if self.italic != other.italic:
            _escseq = _escseq + "3;" if other.bold else _escseq + "23;"
        if _escseq == "\033[": #if no colors and styles were changed,
            return ""          #return an empty string
        return _escseq[:-1] + "m" #replace the trailing semicolon with SGR `m`
