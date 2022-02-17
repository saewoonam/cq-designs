def write_svg(part, name, direction):
    with open(f'./svg/{name}','w') as f:
        f.write(part.toSvg(opts={"projectionDir": direction,
                              "showHidden": False,
                              "height": 800,
                              "width": 800,}))