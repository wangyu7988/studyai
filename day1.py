from mxnet import nd
import numpy as np

x = nd.arange(12)

print(x)

print(x.shape)


X = x.reshape((3, 4))

print(X)

y = nd.zeros((2, 3, 4))

print(y)

z = nd.ones((3, 4))

print(z)


Y = nd.array([[2, 1, 4, 3], [1, 2, 3, 4], [4, 3, 2, 1]])
print(Y)

Z = nd.random.normal(0, 1, shape=(3, 4))
print(Z)

print(X + Y)

print(X / Y)
print(X == Y)
print(Y.exp())
print(X.sum())
print(nd.dot(X, Y.T))

S = nd.concat(X, Y, dim=0), nd.concat(X, Y, dim=1)
print(S)

print(X.norm().asscalar())

X[1:2, :] = 12
print(X)

Z = Y.zeros_like()
before = id(Z)
Z[:] = X + Y
print(Z)
print(before)

P = np.ones((2, 3))
D = nd.array(P)

print(P, D)
print(D.asnumpy())
