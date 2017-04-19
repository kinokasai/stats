from sys import path
path.append('.')

from datastructures import SimpleWeb


def creeNanoWeb1():
    n = SimpleWeb(10)
    n.addArc(0,1); n.addArc(0,4)
    n.addArc(1,2)
    n.addArc(2,3); n.addArc(2,4)
    n.addArc(3,9)
    n.addArc(4,2); n.addArc(4,5); n.addArc(4,7)
    n.addArc(5,6)
    n.addArc(6,5); n.addArc(6,7)
    n.addArc(7,8)
    n.addArc(8,7)
    n.addArc(9,2)
    n.updateProbas()
    return n


def creeNanoWeb2():
    n = SimpleWeb(10)
    n.addArc(0,9)
    n.addArc(1,0); n.addArc(1,5)
    n.addArc(2,1); n.addArc(2,4)
    n.addArc(3,2); n.addArc(3,7)
    n.addArc(4,3)
    n.addArc(5,4)
    n.addArc(6,5)
    n.addArc(7,6)
    n.addArc(8,7)
    n.addArc(9,2); n.addArc(9,8)
    n.updateProbas()
    return n


def creeNanoWeb3():
    n = SimpleWeb(10)
    n.addArc(0,0)
    n.addArc(1,2); n.addArc(1,3)
    n.addArc(2,0); n.addArc(2,3)
    n.addArc(3,3)
    n.addArc(4,5)
    n.addArc(5,4)
    n.addArc(6,7)
    n.addArc(7,6); n.addArc(7,8)
    n.addArc(8,8)
    n.addArc(9,1)
    n.updateProbas()
    return n


if __name__ == "__main__":
    n1 = creeNanoWeb1()
    print(n1)
    n1.writeGraph("graphs/nano1.png")
    n2 = creeNanoWeb2()
    print(n1)
    n2.writeGraph("graphs/nano2.png")
    n3 = creeNanoWeb3()
    print(n1)
    n3.writeGraph("graphs/nano3.png")
