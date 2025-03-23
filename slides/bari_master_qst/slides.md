---
# You can also start simply with 'default'
theme: default
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background: './img/portal.png' #https://cover.sli.dev
# some information about your slides (markdown enabled)
title: Practical Error Correction and Privacy Amplification
info: |
  ## A deck of slides about postprocessing in QKD and practical AC and PA steps
# apply unocss classes to the current slide
class: text-center
# https://sli.dev/features/drawing
drawings:
  persist: false
# slide transition: https://sli.dev/guide/animations.html#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true
---

<style>
body ::deep .slidev-slide__header {
  margin-top: 0 !important;
}
h1 {
  background-color: #2b90b6;
  background-image: linear-gradient(45deg, #4ec5d4 10%, #146b8c 20%);
  background-size: 100%;
  -webkit-background-clip: text;
  -moz-background-clip: text;
  -webkit-text-fill-color: transparent;
  -moz-text-fill-color: transparent;
}
</style>

# Practical Error Correction and Privacy Amplification

#### Marco Cofano - Head of Software LuxQuanta Technologies S.L.


<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon:edit />
  </button>
  <a href="https://github.com/marcocofano/qkd_reconciliation_lectures" target="_blank" alt="GitHub" title="Open in GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---
transition: fade-out
layout: image-right
image: ./img/reconciliation_intro_dark.png
backgroundSize: contain
---

# Information reconciliation in QKD 

<v-clicks>

  - After Quantum comms Alice and Bob share classical correlated strings.
  - Eve has a (quantum) state with some side information (some correlations with Alice and Bob's data)
  - Parameter Estimation: QBER, Excess noise, etc... 

</v-clicks>

---
layout: image-right
image: ./img/reconciliation_intro_dark.png
backgroundSize: contain
---


- Correctness: Some bits are disclosed. Bob tries to guess Alice data from his and the disclosed data
- Security: compute SKR  e.g.: (Devetak-Winter)

<v-click>

$$
  \begin{align}
    r_d = \max\{ 0 , I(A;B) - \chi(A;E) \}   \nonumber  \\
    r_r = \max\{ 0 , I(A;B) - \chi(B;E) \} \, \nonumber 
  \end{align}
$$

</v-click>

<v-click>

  in practice: 

$$
  H_\text{min}(X^{k}| E) \sim h_{min}(\text{QBER})\, 
$$

$$
r = \frac{(N - N_{\text{PE}})h_{\text{min}} - \delta_{\text{leak}}}{N}
$$
  

</v-click>

<v-click>
  Symmetric randomness extraction to eliminate any remaining Side information Eve has

</v-click>


---
transition: fade-out
layout: two-cols-header
---

::header::
# Error Correction / Reconciliation

::footer::
The channel is characterized by the transition probability $P(B|A)$. Two scenarios: 

<img
  class="w-200"
  src="./img/channel.png"
  alt="channel"
  style="display: block; margin: 0 auto;"
/>

In both cases the goal is to have, after some procedure, the same string. 


<v-click>

<div class="text-center">
  <strong>What is the rate at which we can achieve it?</strong>
</div>

</v-click>

<v-click>

Practically: 

If they have a certain number of bits that we can use, how many of those do they need to sacrifice in order to be able to correct the differences

</v-click>


---
transition: fade-out
layout: two-cols-header
---

::header::
# Error correction codes

::footer::

<v-click>

<Definition title="Code">

A <u>code</u> C of length $n$ and cardinality M over a field $\mathbb{F}$ is a collection of M elements from $\mathbb{F}^n$, i.e,

$$
C(n, M) = \{x^{[1]}, \dots, x^{[M]} \}, \quad x^{[m]} \in \mathbb{F}_p, \quad  1\le m\le M.
$$
</Definition>

The elements of the code are called <u>codewords</u> and the parameter $n$ is called <u>codelength</u>. 

</v-click>

<v-click>

<Definition title="Code Rate"> 

The <u>rate</u> of a code $C(n,M)$ is $R=\frac{1}{n}\log_{|\mathbb{F}|}M$. In Shannon terminology it is measured in information symbols per transmitted symbol.
</Definition>

in particular if $M = |\mathbb{F}|^{k}$, then: $R=\frac{k}{n}$

</v-click>
	

---
transition: fade-out
layout: two-cols-header
---

::header::

# MAP decoding

::footer::

<v-click>

- code $C(n,M) = \{x^{[1]}, \dots, x^{[M]}\}$ 
- transition probability $P_{Y|X}(y|x)$
- The source probability: $P_X(x)$
- Y is what the receiver observes
- The probability that we made an error is $1-p_{X|Y}(\hat{x}(Y)|y)$

</v-click>

<v-click>

<Definition title="Maximum a Priori decoder">
$$
\begin{split}
\hat{x}^{MAP}(y) &= argmax_{x \in C} \; p_{X|Y}(x|y) \\
&= argmax_{x \in C} \; p_{Y|X}(y|x)\frac{p_X(x)}{p_Y(y)} \\
\end{split}
$$
</Definition>
If all codewords are equally likely the Maximum a posteriori decoder (MAP) is equal to the Maximum likelihood decoder (ML) because $p_X(x)=1$.

</v-click>
---
transition: fade-out
layout: two-cols-header
---

::header::
# Channel theorems

::footer::

<v-click>

<Theorem  title="Shannon Channel Coding theorem">

There exists a constant C called the Channel Capacity, depending on the transition probability of the channel (parametrized by $\epsilon$), such that if the rate is such that $0 \le r \le C(\alpha)$ then:
$$
\hat{P}^{MAP}_B(n, 2^{[rn]}, \epsilon) \rightarrow 0 \,for \, n \rightarrow 0.
$$
</Theorem>

</v-click>

<v-click>

The converse is also true, namely that if one attempts to decode with a code of rate greater that the Shannon Capacity it will incur in probabilities of error that are bounded away from zero.

</v-click>

<v-click>

The code rate for which (asymptotically) we can expect to decode is:
$$
R < C(\epsilon) = \max_X \left((H(Y) - H(Y|X)\right) = \max_X I(Y;X)
$$

</v-click>

---
transition: fade-out
layout: two-cols-header
---

::header::

# Slepian - Wolf Theorem

---
transition: fade-out
layout: two-cols-header
---

::header::

# Example 1: Uncoded transmission 

::footer::
Suppose that the transmitted bits over the BSC($\epsilon$) are independent and that
$$P \{X_t = +1\} = P \{ X_t = -1\} = \frac{1}{2} $$

We send the data as is. At the receiver, we estimate the transmitted bit X based on the observation Y: 
$$\hat{x}^{\text{MAP}}(y)$$

It is equivalent to maximizing $p_{Y|X}(y|x)$ for the given $x$. 

-  Since $\epsilon$ < 1, we conclude that the optimal estimator is $\hat{x}^{MAP}(y) = y$.

- The probability that the estimate differs from the true value, i.e., $P_b = P \{\hat{x}^{MAP}(Y) \neq X\}$, is equal to $\epsilon$. 

- Code Rate = 1

The probability of error is always bounded away from zero!


---
transition: fade-out
layout: two-cols-header
---

::header::

# Example 2: Repetition code

::footer::

Assume we repeat each bit k times. 

$$(x, \dots, x) \qquad \rightarrow \qquad Y_1 \dots, Y_k$$

The estimator that minimizes the bit-error probability is given by the
majority rule. (Convince yourself)

$$
\hat{x}^{MAP}(y_1, \dots, y_k) = \text{majority of } \{y_1, \dots, y_k \}.
$$

Hence the probability of bit error is given by

$$
P_b = P \{\hat{x}^{MAP}(Y) \neq X\}  = P\{\text{at least } \frac{k}{2} \text{ errors occur} \} = \sum_{i>\frac{k}{2}} \binom{k}{i}\epsilon^i (1-\epsilon)^{k-1}
$$

- rate $\frac{1}{k}$
- For $P_b$ to approach zero we have to choose k larger and larger and as a consequence the rate approaches zero as well.

---
transition: fade-out
layout: two-cols-header
---

::header::
# Linear codes - Hamming


::left::

- We want to send a 4 bits message through a noisy channel. 

- We add three "parity bits" to protect the message bits

$x = (b_1, b_2, b_3, b_4, p_1, p_2, p_3)$

subject to the contraints

$$
\begin{align}
		b_1 + b_3 + b_4 +p_1 = 0 \nonumber \\
		b_1 + b_2 + b_4 +p_2 = 0  \nonumber \\
		b_2 + b_3 + b_4 +p_3 = 0 \nonumber
\end{align}
$$


::right::
<img
  class="w-80 opacity-90"
  src="./img/hamming.png"
  alt="Hamming"
/>


$$
Hx = 0
$$
where H is the parity check matrix:
$$
H = \left[\begin{matrix}
1 & 0 & 1 & 1 & 1 & 0 & 0 \\
1 & 1 & 0 & 1 & 0 & 1 & 0 \\
0 & 1 & 1 & 1 & 0 & 0 & 1
\end{matrix} \right]
$$

<!--
You can have `style` tag in markdown to override the style for the current page.
Learn more: https://sli.dev/features/slide-scope-style
-->

---
transition: fade-out
layout: two-cols-header
---

::header::
# Linear codes - General theory

definition
distance and weight
H and G matrix and their relation
H matrix and cosets, syndrome definition

---
transition: fade-out
layout: two-cols-header
---

::header::
# Linear codes - Complexity Analysis

- Encoder 
- Description
- Decoder

---
transition: fade-out
layout: two-cols-header
---

::header::
# Linear codes - Encoder complexity

---
transition: fade-out
layout: two-cols-header
---

::header::
# Linear codes - Decoder complexity

---
transition: fade-out
layout: two-cols-header
---

::header::
# Linear codes - Performances

---
transition: fade-out
layout: two-cols-header
---

::header::
# Linear codes - Description Complexity Tanner Graph

- tanner graph intro

---
transition: fade-out
layout: two-cols-header
---

::header::
# Regular and irregular codes 

- regular and irregular codes

---
transition: fade-out
layout: two-cols-header
---

::header::
# Low Density Parity Check codes

- LDPC and density
- why is the edge scaling important?


---
transition: fade-out
layout: two-cols-header
---

::header::
# Degree distribution, node perspective


---
transition: fade-out
layout: two-cols-header
---

::header::
# Degree distribution, edge perspective


---
transition: fade-out
layout: two-cols-header
---

::header::
# Degree distribution, examples 

- hamming
- regular
- irregular

---
transition: fade-out
layout: two-cols-header
---

::header::
# Belief Propagation Decoder

- updating probabilities and reformulate in terms of LLRS,
- why logarithms? 
- single variable node as a repetition, Variable node update
- single check node code
- Gallager theorem, 
- Compute the probability updates due to the check constraints
- put together: Sum Product algorithm 

---
transition: fade-out
layout: two-cols-header
---

::header::
# Back to QKD 

- Reconciliation, syndrome decoding. 
- Efficiency of reconciliation $\beta$, $f_{EC}$, $\delta_{\text{leak}}$, BSC case.
- Protocol, PE, choose a matrix, fix a leak, drop in efficiency, see in python code. Alternatives: adaptive EC, puncturing-shortening
- Verification step, hash functions and \epsilon security.

