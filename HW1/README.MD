# Quantum Machine Learning, Homework 1
- Author: NCTU 0712238 Yan-Tong Lin
- Lecturer: Dr. Alexey Melnikov 
- Online Version: https://hackmd.io/d4KVj3YsQuSrRJwCDzly1w
- Warning! the updated ipython notebook (the one for report) is lost, may be at home PC

---

## Note for "Projective simulation for artificial intelligence"
- https://arxiv.org/abs/1104.3787
    - Projective simulation for artificial intelligence
- https://arxiv.org/pdf/1504.02247
    - Projective simulation with generalization


### Model
- Policy
    - $P^{(t)}(a \mid s)$
- How to learn a better policy? By ECM(episodic compositional memory).
- ECM
    - a network of episodes (or clips), which are sequences of remembered percepts and actions.
    - (i) Encounter of percept $s \in S$ which happens with a certain probability $P^{(t)}(s)$. The encounter of percept $s$ triggers the excitation of memory clip $c \in C$ according to a fixed **input-coupler** probability function $I(c \mid s)$.
    - (ii) Random walk through memory/clip space $C$, which is described by conditional probabilities $p^{(t)} (c^{\prime}\mid c)$ of calling/exciting clip $c^{\prime}$ given that $c$ was excited.
    - (iii) Exit of memory through activation of action $a$, described by a fixed **output-coupler** function $O(a =\mid c)$
![](https://i.imgur.com/spXS0Eu.png)
- percepts and actions as product of features
![](https://i.imgur.com/Rb3yR92.png)
- clips are remembered percect/action time-sequences, in the following we consider clips with length 1 for simplicity
![](https://i.imgur.com/q3tKcep.png)
- emotions are remembered rewards
![](https://i.imgur.com/hr1soRp.png)
- true reward function $\Lambda : S \times A \to I \in \mathbb{R}$
![](https://i.imgur.com/JB8ZAlU.png)
![](https://i.imgur.com/z3Hsoyf.png)


### An Instance of Update Rules
- frequency rule
    - here $s, a$ can be replaced by $c_i, c_j$ to be more general
    - $h^{(1)}(s,a) = 1 \forall s \in S, a \in A$
    - $P^{(n)}(a \mid s ) = \frac{h^{(n)}(s,a)}{h^{(n)}(s)}$ where $h^{(n)}(s) = \sum_a h^{(n)}(s,a)$
        - can use softmax to avoid a negative probability
    - let $\lambda^{(n)} = \Lambda(s^{(n)}, a^{(n)})$
    - $h^{(n+1)}(s,a) = h^{(n)}(s,a) + \lambda^{(n)} \delta(s, s^{n})\delta(a, a^{n}) - \gamma(h^{(n)}(s,a)-1))$
        - the $\gamma$ part means forgetting part (decay to uniform)
            - not used for non-changing MDPs
        - $\delta$ is the delta function (to decide whether the $s,a$ pair is the current pair)
- to model delayed reward: **glow**
    - $h^{(n+1)}(s,a) = h^{(n)}(s,a) + \lambda^{(n)} g^{(n+1)}(s, a) - \gamma(h^{(n)}(s,a)-1))$
        - $g^{(n+1)}(s, a) = 1$ if $s, a$ was traversed at time step $n$
        - $g^{(n+1)}(s, a) = (1-\eta)g^{(n)}(s, a)$ otherwise
    - consider delayed reward $100$ at time step $3$ when $a,b$ is traversed, the edge $c, d$ was traversed earlier in time step $1$ with $\eta=0.1$ then edge $c, d$ by definition will be rewarded with increase in $h$ value by $0.9^2 \times 100$
- choose of meta-params
    - $\gamma$ is not required for non-chaning environment (e.g. MDP)
    - In theory, we can choose proper $\eta$ to make the policy to converge to optimal

### Reflection time $R$
- here $\to$ means activate with prob
- if $R=1$
    - $\mu(s) \xrightarrow[]{p} \mu(a)$
- if $R>1$
    - same as $\mu(s) \xrightarrow[]{p}  \mu(a)$
    - but if the emotion assigned to $\mu(s), \mu(a)$ is not good enough, repeat til the $R_{th}$ time

### Efficiency, the Learning Time / Maximal Efficiency Trade-off
![](https://i.imgur.com/i3OoqUI.png =60%x)
![](https://i.imgur.com/t59HIos.png =60%x)


---

## Q1
Go through the material which we considered during the lectures. Think of what is not clear and ask questions.

## A1 
- I go see the original paper for a more rigorous description instead. A note is shown above. If I made any mistake in my note, please let me know. Thanks!
- The equation 5 in the paper "Projective simulation with generalization" is different from the one in the slide by $\lambda^{t}$ or $\lambda^{t+1}$, is there a reason to define them differently?
- The definition of glow seems confusing at the first glace, I think that adding the time step (i.e. $g^{(n+1)}(s, a) = 1$ if $s, a$ was traversed "at time step $n$") will make it more clear.

---

## Q2 + Q3
Let us consider the projective simulation (PS) agent.
The agent has a memory construction with only percept clips and action clips. No other clips are created in the PS memory. The learning algorithm is such that it is the simplest (the first rule that we studied): there is no forgetting, and there is no glow.

![](https://i.imgur.com/FOQJd8i.png)


1. How this will this agent perform in an environment described by the following MDP?
2. How will the h-values change in time?
3. What are the asymptotic h-values at t=infinity?
4. What are the asymptotic probabilities of all the actions?
5. Will all agents behave the same, or some agents will have a preference towards a particular action?

Answer the same questions as above given that the h-values are not initialized as h(0)=1 at time step t=0, but h(0)=1 for action a1 and h(0)=2 for action a2.

## A2 + A3, a DP solution using jyputer notebook
![](https://i.imgur.com/4O4G1hR.png)


1. According to the model description and I will discuss how its $h$ value changes as time goes to infinity
2. The dynamic programming transition shows it
    - $P(a,b) = \frac{a-1}{a+b-1}P(a-1, b) + \frac{b-1}{a+b-1}P(a, b-1)$
3. What are the asymptotic h-values at t=infinity?
    - the figure clearly shows the two cases
    - case 1
        - any $h$ value pairs are equally possible
        - $[h_0] = \frac12 n+1$
    - case 2
        - A $h$ value pair with lower $h(0)$ is more possible 
        - $[h_0] = \frac13 n +1$
4. What are the asymptotic probabilities of all the actions?
    - case 1
        - $\frac{1}{2}, \frac{1}{2}$
    - case 2
        - $\frac{1}{3}, \frac{2}{3}$
5. Will all agents behave the same, or some agents will have a preference towards a particular action?
    - Agents will have their preferences, with uniform prob in case 1, and with higher prob to prefer action 2 in case 2

---


## Q4
Consider the grid-world problem.
![](https://i.imgur.com/cwIUQLW.png)
Program PS agent in this environment (the same maze as in the presentation slides containing 54 positions). Use glow in this environment and no forgetting. Which meta parameter do you find to be optimal?
Use any programming language you prefer.



## A4
- The optimal can be defined on ourself. (confirmed with Dr. Alexey Melnikov )
- In this case, my observation is that agents with different $\eta$s in certain range all converge to $\eta$ as the number of trials grow.
- For the observation, I would define the optimal as "the $\eta$ that converges to the optimal policy with high probability with the least number of trials"
- In practice, I plot a $\text{number of trials - average steps}$ graph to show which value among $\{0.01, 0.1, 0.2, 0.3\}$ is optimal
    - ![](https://i.imgur.com/RBvFOUA.png)
        - note: the population is set to 50
    - By the graph, it seems that $\eta=0.1,0.2$ are good
    - My observation is that agents with larger $\eta$ converge to smaller value, but takes more trials.
- Also, an example of the policy (from its h-values) of an $\eta=0.2$ agent after 100 trials. Please note that the policy is optimal in the agent's mind does not means that it acted optimally during the training process.
    - ![](https://i.imgur.com/S7cJ73k.png)


---

## Notes
- Sicne I was at a conference (TAAI2020) from 12/3-5, I handed in the homework after the deadline. However, I completed all Q1-3 without any reference to the the lecture video on 12/4. And I consulted with the lecturer to make sure the "optimal" in Q4 is defined by ourself and gave the "definition of my own" and came up with "how to program it" independently, before seeing the video.
- For the answer to question 4, one more thing I can to is to focus on the region $[0.1, 0.3]$ with more population and see which value actually yields optimal result (14 steps) with high probability. But since the computational cost is high for my computer and the core of the method is catched, I will omit this part.
- To see my answer with code, please refer to the other file that is generated from jupyter notebook.