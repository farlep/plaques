import plaques

a = plaques.CharCell(bgcol = "r", ulined = True, italic = True)
b = plaques.CharCell(char = "B", italic = True, color = "g")
c = plaques.CharCell(char = "c", bold = True, italic = False)
print(a)
print(b)
print(c)
print(a.overlay(b))
print(a.overlay(c))
