import argparse
import dxfwrite
from math import sqrt, acosh, cosh, ceil

def main():
    parser = argparse.ArgumentParser(description='Catenary generator', add_help=True)
    parser.add_argument('-o', '--output', nargs='?', type=str, metavar='PATH',
                        required=True,
                        help='Output file path')
    parser.add_argument('-s', '--size', nargs='?', type=float, metavar='DIM',
                        required=True, help='Square dimension')
    parser.add_argument('-r', '--repeats', nargs='?', type=float, metavar='N',
                        required=False, default=1, help='Number of repeats')
    parser.add_argument('--resolution', nargs='?', type=int, metavar='N',
                        required=False, default=100, help='Number of segments per repeat')
    args = parser.parse_args()

    dxf = dxfwrite.DXFEngine()
    drawing = dxf.drawing()
    a = args.size / 2
    d = a * sqrt(2)
    b = a * acosh(sqrt(2))
    def f(x):
        while x < 0:
            x += 2 * b
        while x >= 2 * b:
            x -= 2 * b
        return d - a * cosh((x - b) / a)
    x = [2 * b * i / args.resolution for i in range(int(ceil(args.resolution * args.repeats)))]
    y = list(map(f, x))
    for i in range(1, len(x)):
        drawing.add(dxf.line((x[i-1], y[i-1]), (x[i], y[i])))
    drawing.saveas(args.output)

if __name__ == "__main__":
    main()