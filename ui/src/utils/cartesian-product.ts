export function cartesianProduct<X, Y>(a: X[], b: Y[]): Array<[X, Y]> {
    return a.flatMap(x => b.map(y => [x, y] satisfies [X, Y]));
}
