---
layout: homepage
title: "물리학자를 위한 AI 1: Gradient Descent"
date: 2026-05-26
description: "물리학자의 직관으로 gradient descent를 다시 보기 — potential landscape, force, 그리고 왜 이게 ML의 출발점인가."
---

<h2 style="margin: 2px 0px -15px;"><u>물리학자를 위한 AI 1: Gradient Descent</u></h2>

<br>

<small><em>{{ page.date | date: "%B %d, %Y" }}</em></small>

<br><br>

## 왜 gradient descent부터?

머신러닝을 처음 접하는 물리학자에게 "neural network는 universal function approximator다", "transformer는 attention mechanism으로..." 같은 설명은 본질을 가린다고 생각한다. ML이라는 것은 결국 **어떤 손실 함수의 landscape 위에서 공을 굴리는 것**이다. 그 공을 굴리는 가장 기본적인 방식이 gradient descent이고, 거의 모든 modern ML training은 이것의 변형이다.

물리학자에게 친숙한 언어로 다시 쓰면 — 손실 함수 $L(\theta)$는 parameter 공간 위에 정의된 **potential**이고, gradient descent는 그 위에서 overdamped Langevin dynamics (without noise)를 푸는 것이다.

$$\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)$$

이건

$$\frac{d\theta}{dt} = -\nabla L(\theta)$$

의 forward Euler discretization이다. 즉 **force = $-\nabla L$** 이고, mass가 없는 입자가 viscous medium에서 움직이는 그림이다. learning rate $\eta$는 시간 간격.

## Potential landscape로 보기

물리에서 우리는 potential surface를 자주 그린다. ML에서도 마찬가지로 — 다만 dimension이 백만 차원이라는 점이 다르다. 이 고차원에서 일어나는 직관적이지 않은 현상들이 ML의 실제 문제다:

- **Saddle point가 local minimum보다 압도적으로 많다.** 차원이 높을수록 eigenvalue가 전부 같은 부호일 확률이 지수적으로 감소한다. 그래서 일반적으로 "local minima에 갇힌다"는 그림은 실제 ML training에서는 거의 일어나지 않는다. 진짜 문제는 saddle point에서의 slow escape다.
- **Loss landscape는 매우 anisotropic하다.** 어떤 방향은 가파르고, 어떤 방향은 거의 평평하다. 이는 Hessian의 condition number가 크다는 뜻이고, vanilla gradient descent가 비효율적인 이유다.

## Momentum: mass를 다시 넣자

Vanilla GD가 overdamped라면, momentum은 **mass**를 다시 추가하는 것이다:

$$v_{t+1} = \mu v_t - \eta \nabla L(\theta_t)$$

$$\theta_{t+1} = \theta_t + v_{t+1}$$

물리적으로는

$$m \ddot{\theta} + \gamma \dot{\theta} = -\nabla L$$

의 discretization으로 볼 수 있다. $\mu$는 friction과 mass의 비율로 해석된다.

왜 이게 도움이 되는가? Anisotropic landscape에서, 평평한 방향으로는 momentum이 누적되어 빠르게 이동하고, 가파른 방향에서는 oscillation이 damping된다. 즉 **eigenvalue spread에 대한 robustness**가 생긴다.

## Adam: per-coordinate adaptive timestep

Adam은 한 단계 더 나아간다. 각 coordinate마다 **다른 effective learning rate**를 쓰는 것:

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) \nabla L$$

$$v_t = \beta_2 v_{t-1} + (1-\beta_2) (\nabla L)^2$$

$$\theta_{t+1} = \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$$

이건 second moment $v_t$로 gradient를 normalize하는 것 — coordinate별로 "이 방향이 얼마나 가파른가"를 추정하고, 그에 반비례하게 step size를 조정한다. 물리학자 식으로는 **diagonal preconditioning**이다. 진짜 Hessian의 inverse를 쓰면 Newton method가 되겠지만, 그건 너무 비싸니까 diagonal approximation으로 대충 한다.

## Stochastic gradient descent: thermal noise

실제로는 한 번에 전체 데이터의 gradient를 계산하지 않고, 작은 batch로 추정한다:

$$\nabla L(\theta) \approx \nabla L_{\text{batch}}(\theta)$$

이건 **noisy gradient**다. 이 noise는 thermal noise처럼 작용해서, 좁은 minimum에서 입자를 흔들어 빠져나오게 한다. 즉 SGD는 자동으로 **annealing** 효과를 가진다. 최근에는 이 noise structure가 generalization과 깊이 관련 있다는 연구들이 많다 (SGD가 implicit하게 flat minimum을 찾는다는 결과들).

## 정리

- GD는 overdamped gradient flow의 discretization이다.
- Momentum은 mass를 추가한 것이다.
- Adam은 diagonal preconditioning이다.
- SGD의 stochasticity는 thermal noise처럼 작용한다.

이 네 가지가 modern deep learning training의 거의 모든 것이다. 다음 글에서는 backpropagation을 — physicists에게 친숙한 **adjoint method**의 관점에서 — 다뤄볼 예정이다.

<br>

---

<small>← [Back to Blog]({{ '/blog/' | relative_url }})</small>
