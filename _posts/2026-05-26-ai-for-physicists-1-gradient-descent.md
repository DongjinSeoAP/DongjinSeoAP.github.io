---
layout: homepage
title: "AI for Physicists 1: Gradient Descent"
date: 2026-05-26
description: "Re-reading gradient descent with a physicist's intuition — potential landscapes, forces, and why it is the starting point of modern ML."
---

<h2 style="margin: 2px 0px -15px;"><u>AI for Physicists 1: Gradient Descent</u></h2>

<br>

<small><em>{{ page.date | date: "%B %d, %Y" }}</em></small>

<br><br>

## Why start with gradient descent?

When a physicist first encounters machine learning, descriptions like "a neural network is a universal function approximator" or "transformers work via attention" tend to hide the essence. ML, in the end, is just **rolling a ball on the landscape of some loss function**. The simplest way to roll that ball is gradient descent, and nearly every modern ML training routine is a variant of it.

In language familiar to physicists — the loss $L(\theta)$ is a **potential** defined over parameter space, and gradient descent solves (noise-free) overdamped Langevin dynamics on it:

$$\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$$

This is the forward Euler discretization of

$$\frac{d\theta}{dt} = -\nabla L(\theta).$$

So **force = $-\nabla L$**, and we are watching a massless particle drift through a viscous medium. The learning rate $\eta$ plays the role of the time step.

## Reading the potential landscape

Physicists are used to drawing potential surfaces. ML lives on the same picture — except the dimension is in the millions. A few non-intuitive things happen up there, and they shape what actually matters in training:

- **Saddle points vastly outnumber local minima.** In high dimensions, the probability that all Hessian eigenvalues share a sign decays exponentially. So the textbook "stuck in a local minimum" story barely happens. The real bottleneck is *slow escape from saddle points*.
- **The loss landscape is highly anisotropic.** Some directions are steep, others are nearly flat. That is exactly a Hessian with large condition number, which is why vanilla gradient descent is so inefficient.

## Momentum: put the mass back in

If vanilla GD is overdamped, then momentum is what you get by **giving the particle mass back**:

$$v_{t+1} = \mu v_t - \eta \nabla L(\theta_t)$$

$$\theta_{t+1} = \theta_t + v_{t+1}$$

Physically this is a discretization of

$$m \ddot{\theta} + \gamma \dot{\theta} = -\nabla L,$$

where $\mu$ encodes the ratio between friction and mass.

Why does it help? On an anisotropic landscape, momentum accumulates along the flat directions, so the particle moves quickly there, while oscillations along the steep directions get damped. The net effect: **robustness to a wide eigenvalue spread**.

## Adam: a per-coordinate adaptive time step

Adam goes one step further. It uses a **different effective learning rate for each coordinate**:

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) \nabla L$$

$$v_t = \beta_2 v_{t-1} + (1-\beta_2) (\nabla L)^2$$

$$\theta_{t+1} = \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$$

The trick is to normalize the gradient by its second moment $v_t$: estimate, per coordinate, "how steep is this direction?" and scale the step inversely. In physicist's terms this is **diagonal preconditioning**. The true inverse Hessian would give you Newton's method, but that is too expensive, so Adam just settles for a diagonal approximation.

## Stochastic gradient descent: thermal noise

In practice we never compute the gradient over the whole dataset; we estimate it from a small batch:

$$\nabla L(\theta) \approx \nabla L_{\text{batch}}(\theta).$$

This is a **noisy gradient**. The noise acts like thermal noise — it shakes the particle out of narrow minima. So SGD comes with a built-in **annealing** effect. Recent work links the structure of this noise tightly to generalization (the running intuition: SGD implicitly prefers flat minima).

## Wrapping up

- GD is the discretization of overdamped gradient flow.
- Momentum adds mass.
- Adam is diagonal preconditioning.
- SGD's stochasticity behaves like thermal noise.

These four ideas cover almost all of modern deep learning training. In the next post I will look at backpropagation — through a lens physicists already know well: the **adjoint method**.

<br>

---

<small>← [Back to Blog]({{ '/blog/' | relative_url }})</small>
