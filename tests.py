#!/usr/bin/env python3

import json
import plaques as plq

mpbase = plq.Plaque(h_abs_size = 20, v_abs_size = 7, fill = plq.CharCell(bgcol = plq.RED, ulined = True, color = plq.BLACK))
mpchild = plq.Plaque(h_rel_size = 0.4, v_rel_size = 0.6, h_rel_pos = 0.5, v_rel_pos = 0.5,
    fill = plq.CharCell(bgcol = plq.BLUE, char = "a", color = plq.BLACK)
    )
#print(json.dumps(mpbase.render(30,30), indent = 4, default = repr))
mpbase.content.append(mpchild)
#print(json.dumps(mpbase.render(30,30), indent = 4, default = repr))
plq.print_plaque(mpbase)
