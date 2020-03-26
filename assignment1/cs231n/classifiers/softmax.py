from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    num_train = X.shape[0]
    num_classes = W.shape[1]

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################

    for i in range(num_train):
        scores = X[i].dot(W)
        scores -= np.max(scores)
        exp_sum = 0.0

        for j in range(num_classes):
            exp_sum += np.exp(scores[j])

        for k in range(num_classes):
            p = np.exp(scores[k]) / exp_sum

            if k == y[i]:
                loss += -np.log(p)
                dW[:, k] += (p - 1) * X[i]
            else:
                dW[:, k] += p * X[i]

    dW /= num_train
    dW += 2 * reg * W

    loss /= num_train
    loss += reg * np.sum(W * W)
    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    num_train = X.shape[0]

    # forward pass
    scores = X.dot(W)
    # prevent numerical issues
    scores -= np.max(scores)
    exp_scores = np.exp(scores)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    correct_logprobs = -np.log(probs)[range(num_train), y]
    data_loss = np.sum(correct_logprobs) / num_train
    reg_loss = reg * np.sum(W**2)
    loss = data_loss + reg_loss

    # backprop
    dscores = probs
    dscores[range(num_train), y] -= 1
    dW = np.dot(X.T, dscores)
    dW /= num_train
    dW += 2 * reg * W
    return loss, dW
