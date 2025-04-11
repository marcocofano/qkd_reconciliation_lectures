---
theme: ../../slidev-theme-lq
title: Practical Error Correction and Privacy Amplification
subtitle: Marco Cofano - Head of Software LuxQuanta Technologies S.L. 
info: "" 
class: text-center
backgroundImg: /portal.png
drawings:
  persist: false
transition: slide-left
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true
layout: cover
---

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
---

::header::
# Information reconciliation in QKD 

::left::
<v-clicks>

- After Quantum comms Alice and Bob share classical correlated strings.
- Eve has a (quantum) state with some side information (some correlations with Alice and Bob's data)
- Parameter Estimation: **QBER**, Excess noise, etc... A and B share and discard some samples
- Correctness: Some bits are disclosed. Bob tries to guess Alice data from his and the disclosed data
- Security: compute SKR  e.g.: (Devetak-Winter)
Symmetric randomness extraction to eliminate any remaining Side information Eve has
</v-clicks>
::right::

![Reconciliation Intro](/reconciliation_intro.png)
<!-- <img src="/reconciliation_intro.png" alt="Reconciliation Intro">  -->
<!-- </img> -->

---
transition: fade-out
---

::header::
# Entropic quantities operational meaning

<Box title="Conditional Probability">

  $P(A|B)$ Probability distribution of A, knowing B's results. "The probability distribution of A's data according to B's knowledge"

</Box>

<Box title="Entropy">

  $H(A)$  Amount of bits we need to convey (describe) A's distribution. Maximum compression possible for A's data

</Box>

---
transition: fade-out

---

::header::
# Entropic quantities operational meaning

<Box title=" Conditional Entropy">

$H(A|B)$  Amount of bits B needs, if he wanted to describe A's distribution, according to Bob. Bob might have more data using his distribution which reveals some info about Alice. If A, B  are decorrelated $H(A|B) = H(A)$

</Box>


<Box title="Mutual Information">

$I(A, B)$ Information gain. Given that Bob has some info on A, he does not need H(A) bits to describe A, he needs H(A|B) bits. He gained

$$
I(A,B) = H(A) - H(A|B)
$$
    bits
</Box>

---
transition: fade-out

---

::header::
# Entropic quantities operational meaning

<Box title=" Conditional Min Entropy">

  $H_{min}(A|B)$ Max amount of random bits one can extract from a sample taken from distribution A, when B has side information.

</Box>
---
transition: fade-out

---

::header::
::left::

Devetak-Winter formula
<v-click>

$$
r_d = \max\{ 0 , \beta I(A;B) - \chi(A;E) \} \\
r_r = \max\{ 0 , \beta I(A;B) - \chi(B;E) \}  
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
  
$$
\delta_{\text{leak}} \ge H(A|B)
$$



</v-click>


::right::

<img src="/reconciliation_intro.png"> 
</img>


---
transition: fade-out

---

::header::
# Error Correction / Reconciliation

::footer::

Two scenarios: 

- Lossy channel
- Asymmetric source coding with side information (only available at decoder) - Slepian Wolf

<img
  class="w-200"
  src="/channel.png"
  alt="channel"
  style="display: block; margin: 1 auto;"
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

---

::header::
# Error Correction / Reconciliation

::footer::

The channel is characterized by the transition probability $P(B|A)$.

BSC channel: 
<img src="/bsc.png" class="block mx-auto"/>


The transition probability is 

$$
P(B|A) = \begin{cases}
P(1|1) = 1 - \epsilon = P(0|0) \\
P(1|0) = \epsilon = P(0|1) \\		
\end{cases}
$$


---
transition: fade-out

---

::header::
# Error correction codes

::footer::

<v-click>

<Definition title="Code">

A <u>code</u> C of length $n$ and cardinality $|C|$ over a field $\mathbb{F}$ is a collection of $|C|$ elements from $\mathbb{F}^n$, i.e,

$$
C(n, M) = \{x^{[1]}, \dots, x^{[M]} \}, \quad x^{[c]} \in \mathbb{F}_p, \quad  1\le c\le |C|.
$$
</Definition>

The elements of the code are called <u>codewords</u> and the parameter $n$ is called <u>codelength</u>. 

</v-click>

<v-click>

<Definition title="Code Rate"> 

The <u>rate</u> of a code $C(n,M)$ is $R=\frac{1}{n}\log_{|\mathbb{F}|}|C|$. In Shannon terminology it is measured in information symbols per transmitted symbol.
</Definition>

in particular if $|C| = |\mathbb{F}|^{m}$, then: $R=\frac{m}{n}$

</v-click>
      
---
transition: fade-out

---

::header::
# Error correction codes



---
transition: fade-out

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

If all codewords are equally likely the Maximum a posteriori decoder (MAP) is equal to the Maximum likelihood decoder (ML) because $p_X(x)=\frac{1}{2}$.

</v-click>
---
transition: fade-out

---

::header::
# Channel theorems

::footer::

<v-click>

<Theorem  title="Shannon Channel Coding">

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

---

::header::

# Slepian - Wolf Distributed Source Coding (1977)

Asymmetric source coding with side information only at the decoder

::footer::


<v-click>

- We have two correlated distributions A and B.
- A is only available at the encoder and B is only available at the decoder. 

</v-click>

<v-click>
<Box>
What is the best compression for A, knowing the correlation between the distributions?
</Box>

</v-click>


<v-click>
If they where uncorrelated it would be H(A), and H(B) resp. But knowing that they are correlated lowers the best encoding for A to:

$$
H(A|B) = H(A) - I(A,B)
$$

Bob only needs this amount of information to decode Alice string. This will produce two identical strings.

</v-click>


<v-click>
<Box>
IN QKD this side info is sacrificed to correct the rest:

$$
\delta_{\text{leak}} \ge H(A|B)
$$

</Box>

</v-click>

---
transition: fade-out

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

---

::header::

# Example 2: Repetition code

::footer::

<v-click>
Assume we repeat each bit k times. 

$$(x, \dots, x) \qquad \rightarrow \qquad Y_1 \dots, Y_k$$

The estimator that minimizes the bit-error probability is given by the
majority rule. (Convince yourself)

$$
\hat{x}^{MAP}(y_1, \dots, y_k) = \text{majority of } \{y_1, \dots, y_k \}.
$$

</v-click>

<v-click>
Hence the probability of bit error is given by

$$
P_b = P \{\hat{x}^{MAP}(Y) \neq X\}  = P\{\text{at least } \frac{k}{2} \text{ errors occur} \} = \sum_{i>\frac{k}{2}} \binom{k}{i}\epsilon^i (1-\epsilon)^{k-1}
$$

- rate $\frac{1}{k}$
- For $P_b$ to approach zero we have to choose k larger and larger and as a consequence the rate approaches zero as well.

</v-click>

---
transition: fade-out

---

::header::
# Repetition Codes - cont'd 

::left::

<Box title="Lossy channel">

$(000)$ and $(111)$ codewords are the correct ones. 
They are maximally distanced so that one error can be corrected. 

</Box>


::right::

<div class="text-center">
<img
class="w-120 opacity-90"
src="/repetition.png"
alt="Repetition codes"
/>
</div>


---
transition: fade-out

---

::header::
# Repetition Codes - cont'd 

::left::

<Box title="Asymmetric source coding problem">

A and B have any 3 bits codes with equal probability, but correlated (that they differ only by one bit)

$$
(000, 111)
(001, 110)
(010, 101)
(100, 011)
$$

- They all differ by 3 bits. So the decoder can, knowing his string, decifer which one A holds. 

- Only reveal which group A is in to B: 2 bits

- Alice and Bob can reconcile 1 bit out of the three they share. 

</Box>

::right::

<div class="text-center">
<img
class="w-120 opacity-90"
src="/repetition.png"
alt="Repetition codes"
/>
</div>

---
transition: fade-out

---

::header::
# Linear codes - Hamming


::left::

<v-click>

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

</v-click>



::right::
<v-click>

<img
class="w-80 opacity-90"
src="/hamming.png"
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
</v-click>

---
transition: fade-out

---


::left::
# Hamming decoding - Exercises

1. Can you reason about the Slepian-Wolf asymmetric source coding point of view, for Hamming Codes.
2. Can you extend the Hamming codes to more bits and different code rates?
Prove that:

- a general Hamming code has n = $2^k - 1$ and the number of systematic bits is: 

$$s = 2^k - k - 1$$

::right::
<div style="display: flex; justify-content: flex-end;">
<img
class="w-80 opacity-90"
src="/hamming.png"
alt="Hamming"
/>
</div>


---
transition: fade-out

---

::header::
# Linear codes - General theory

::footer::
<Definition title="Linear code">

A linear code of length $n$ and dimension $k$ is a linear subspace $C$ with dimension $k$ of the vector space $\mathbb {F}_{q}^{n}$ where $\mathbb {F}_{q}$ is the finite field with $q$ elements.
The vectors in C are called codewords. The size of a code is the number of codewords and equals $q^k$.

</Definition>

<Definition title="Distance">

The (Hamming) distance between two codewords is the number of elements in which they differ

</Definition>


---
transition: fade-out

---

::header::
# Linear codes - H, G matrix, Syndrome

::footer::

<Definition title="G matrix">

  As a linear subspace of $\mathbb{F}_{q}^{n}$, the entire code C may be represented as the span of a set of k codewords. These basis codewords are often collated in the rows of a matrix G known as a $\textbf{generating matrix}$ for the code C. When G has the block matrix form $G=[I_{k}|P]$, where $I_{k}$ denotes the $k\times k$ identity matrix and P is some $k \times (n-k)$ matrix,  it is in **systematic form**.

</Definition>

<Definition title="H matrix">

A matrix H representing a linear function
$$
H :\mathbb {F}_{q}^{n} \to \mathbb {F}_{q}^{n-k},
$$
whose kernel, $\ker H = \{x \in \mathbb{F}^n_q: H x^T = 0\}$  is C is called a check matrix of C.

</Definition>


---
transition: fade-out

---

::header::
# Linear codes - H, G matrix, Syndrome

::footer::


<Definition title="Syndrome">

  Be $x \in \mathbb{F}_{q}^{n}$ 
$$
s = H \,x
$$
</Definition>

<Box title="Properties">

  - G and H are such that GH = 0.
  - There exist the following bijections: $\mathbb{F}_{q}^{n - k} \cong \mathbb{F}_{q}^{n} / im(G) \cong \mathbb{F}_{q}^{n} / \ker H$,
  - The total space $\mathbb{F}_{q}^{n}$ is partitioned into equivalence classes:

  two different codewords $y, y\prime \in \mathbb{F}_{q}^{n}$ that differ by a valid codeword $Gx \in im(G)$, namely $y\prime = y + Gx$ for some $x\in \mathbb{F}_{q}^{k}$ are mapped to the same syndrome by H and so they are in the same equivalence class.

</Box>

---
transition: fade-out

---

::header::
# Linear codes - Complexity Analysis

- Encoder 
- Description
- Decoder

---
transition: fade-out

---

::header::
# Linear codes - Encoder complexity


<v-click>

What is the number of operations needed to perform encoding?

</v-click>


<v-click>
If we encode using the G matrix (or an equivalent algorithm using H directly) we expect 

$$O(n^2)$$

operations.


</v-click>


<v-click>

[Richardson and Urbantke (2001)](https://ieeexplore.ieee.org/document/910579) proved that the optimal Encoding can be achieved in: 

$$O(n) + O(g^2)$$ 

with $g$ possibly small, if we cleverly desing a matrix H such that it is almost upper triangular with only g rows that are complete (have values above diagonal).

</v-click>



::notes::
<v-click>

Richardson, Thomas J, and Rüdiger L Urbanke. “Efficient Encoding of Low-Density Parity-Check Codes.” IEEE TRANSACTIONS ON INFORMATION THEORY. Vol. 47, 2001.

</v-click>


---
transition: fade-out

---

::header::
# Linear codes - Decoder complexity


<v-click>

The MAP decoding problem is, unfortunately, NP-Hard. 

</v-click>



::left::

<v-click>

- Suboptimal, but very good, iterative graph theory solutions.
- Fix Code Rate, for each $\epsilon$,  work at a certain distance to capacity. 
- Efficiency of Error correction ($\beta$, $f_{EC}$) 
$$
1 - R = f_{EC} \; H(A|B) = \delta_{\text{leak}} \\
R = \beta \; I(A,B)
$$
- Waterfall vs Error floor working points. 

Non idealities wrt Shannon Theorem. 
- Non-infinite codes
- non-optimal, iterative decoding (MAP is NP-Hard)

</v-click>


::right::

<v-click>
  
<img
class="w-180"
src="/performance.png"
alt="Hamming"
/>

</v-click>

---
transition: fade-out

---

::header::
# Linear codes - Description Complexity Tanner Graph

<v-click>

the H matrix has $(1 - R)n^2$ entries. For binary matrices, one can cleverly (especially for sparse matrices) reduce the amount of data needed to describe it (and store it)

</v-click>


<v-click>

family of binary matrices with the same Code rate and performances can be described quite easily, through a bipartite graph. 


</v-click>

::left:: 

<v-click>
Tanner graph

- Each variable node (column) is a bit sent in the channel
- Each check node (row) computes the corresponding parity equation
- the edges connect each bit to the PC equations it belongs
- VN and CN have sockets with a number of edges going out

</v-click>

::right::

<v-click>
<img
class="w-70"
src="/tanner.png"
alt="Hamming"
/>

</v-click>

---
transition: fade-out

---

::header::
# hamming code tanner graph 

::left::

$$
\begin{align}
	      b_1 + b_3 + b_4 +p_1 = 0 \nonumber \\
	      b_1 + b_2 + b_4 +p_2 = 0  \nonumber \\
	      b_2 + b_3 + b_4 +p_3 = 0 \nonumber
\end{align}
$$

$$
H = \left[\begin{matrix}
1 & 0 & 1 & 1 & 1 & 0 & 0 \\
1 & 1 & 0 & 1 & 0 & 1 & 0 \\
0 & 1 & 1 & 1 & 0 & 0 & 1
\end{matrix} \right]
$$


<v-click>

$$
R = \frac{n - k}{n} =  \frac{7 - 3}{7} = \frac{4}{7}
$$

- degree of CN = $[4, 4, 4]$
- degree of VN = $[2, 2, 2, 3, 1, 1, 1]$

</v-click>

::right::
<img
class="w-120 block mx-auto opacity-150"
src="/tanner_hamming.png"
alt="Hamming Tanner Graph"
/>

---
transition: fade-out

---

::header::
# Regular and irregular codes 

::left::



Regular codes $C(n, j, l)$

- j edges per VN, l edges per CN
- have a high degree of constraints, (the number of check nodes is inferred from $(n, j, l)$
  
- easy to design. Poorer performance

::right::

Irregular Codes

- relax the constraint on the degree distribution
- can perform better
- harder to design

::footer::

<v-click>

Regular code, Code rate:

The code rate can be completely inferred from the degree distribution. 

For a regular code $C(j, l)$, the number of edges can be computed from VN and CN and need to match:

$$
nj = kl
$$

$$
R = 1 - \frac{k}{n} = 1 - \frac{j}{l}
$$

</v-click>



---
transition: fade-out

---

::header::
# Low Density Parity Check codes

::footer::
They were invented by [Gallager (1963)](https://ieeexplore.ieee.org/document/1057683), with a construction of regular codes that had a low density. 

Regular codes edges scale linearly with the size of the code $n$.  
Gallager introduced an iterative decoder whose main computation depends on the edge count. 

Also irregular codes can be designed so that they are LDPC.

<Box title="Advantages of low density and linear scaling">

- Faster Decoder
- Can perform very close to channel capacity
- Simpler to store (less resources)
- Sparse matrices have optimized algebraic algorithms

</Box>


::notes::

Gallager, R. “Low-Density Parity-Check Codes.” IRE Transactions on Information Theory 8, no. 1 (1962): 21–28. https://doi.org/10.1109/TIT.1962.1057683.

---
transition: fade-out

---

::header::
# Belief Propagation Decoder

::left::

<v-click>

- we input our belief about every bit (Variable Nodes): 

What is $P(B|A = 1)$ compared to $P(B|A=0)$? This will be our message that we send into the graph. 

</v-click>


<v-clicks>

- we repeat this message and send it to each connected CN
- there we update this belief in such a way that the parity  check equations are satisfied. 
- we resend it back to VN where we collect all the different updates for the same bit. We update the bit probability belief from all the edges
- from the current beliefs we extract the bit value, 0 or 1 if the updated probability of being 0 was more that being 1

</v-clicks>

::right::


<img
class="w-120 block mx-auto opacity-150"
src="/tanner_hamming.png"
alt="Hamming Tanner Graph"
/>


<v-click>

- if the guessed bits satisfy the parity check equations we exit, otherwise we continue updating. 

</v-click>

---
transition: fade-out

---

::header::
# Log likelihood
::footer::


$$
P(Y=y | X = 0) 
$$

<Definition title="Log-likelihood">

$$
L(X) = \ln\left(\frac{P(X = 0)}{P(X = 1)}\right), \;

L(X|Y) = \ln\left(\frac{P(X = 0|Y)}{P(X = 1|Y)}\right)
$$

</Definition>

-  logs compress the values. Avoids numerical instabilities in computer code
-  No normalization of probabilities needed
-  They will be easy to compute (linear in the received bits)
-  The multiplications will be substituted by additions (faster on a computer)
-  Log are monotones so: if $L > 0 \rightarrow P(X=0) \ge P(X=1)$
-  The sign of $L$ tells the most probable binary value, the magnitude the reliability of the choice

---
transition: fade-out

---

::header::
# LLR examples

::footer::
<Box title="BSC">

For the BSC of crossover probability $\epsilon$: 
$$
L(Y=\ddot{y}|X) = \ln\left(\frac{1-\epsilon}{\epsilon}\right) \ddot{y}
$$
</Box>


<Box title="BiAWGN">

From a BiAWGN channel with variance $\sigma^2$
$$
L(Y=\ddot{y}|X) = \left(\frac{2}{\sigma^2}\right)\ddot{y}
$$
</Box>


---
transition: fade-out

---

::header::
# LLR examples

::left::

To convert back to probabilities:

$$
L(X) = \ln\left(\frac{P(X = 0)}{P(X = 1)}\right) \\ 
e^{L(X)} = \frac{P(X=0)}{1-P(X=0)} \\
P(X = 0) = \frac{1}{1+e^{-L(X)}}\\
P(X = 1) = \frac{1}{1+e^{L(X)}}
$$

::right::
The expectation value of $\hat{x}$ in terms of the LLR:

$$
E(x) = P(X=0) - P(X=1) \\ 
 =  1 - 2P(X=1) \\
 = \tanh\left(\frac{L(X)}{2}\right)
$$

---
transition: fade-out

---

::header::
# Belief propagation: CN update
This needs a bit more work. 

::footer::

<Theorem title="Gallager">

  Consider a binary sequence such that the probability that the l-th bit is 1 is $P_l$. The probability that the sequence has an even number of 1's is:

$$
P = \frac{1}{2}\left(1 + \prod_{l=1}^{k}(1 - 2P_l)\right)
$$

</Theorem>


---
transition: fade-out

---

::header::
# Belief propagation: CN update

::footer::
Single Check Code

Consider a code with only one parity check and $n$ transmitted bits

The MAP decoder for such a code tells us that, for any message bit:

$$
\hat{x}_1 = \arg \max P(x_1=b|y, \text{even number of 1s})
$$

We can re arrange the formula and use Gallager theorem:

$$
P(x_1=0|y, \text{even number of 1s}) = 
P(x_2, \dots x_n  \text{even number of 1s}| y)  \\
= \frac{1}{2}\left(1 + \prod_{l=2}^{k}(1 - 2P(x_l=1|y_l))\right) \\
= 1 - P(x_1=1|y, \text{even number of 1s})
$$

$$
1 -2P( x_1=1|y, \text{even number of 1s}) = 
\prod_{l=2}^{k}(1 - 2P(x_l=1|y_l))
$$

---
transition: fade-out

---

::header::
# Belief propagation: CN update

::footer::

we can rewrite it in terms of LLRs:

$$
L(x_1|y, \text{even number of 1s}) = 
2\tanh^{-1} \left(\prod_{l=2}^n\tanh\left( \frac{L(x_l|y_l)}{2}\right)\right)
$$

<img src="/CN_update.png" alt="CN update" class="w-100 block mx-auto">


---
transition: fade-out

---

::header::
# Belief propagation: VN update

::left::

- the messages coming from the check nodes update the LLR for each VN
- a VN is like a repetition code of one bit. We send, repeated with uniform probability the same bit
- LLRs update involve summing (Bayes rule with uniform prior).

$$
L(X|y) = L(y|X)
= \sum_{i=1}^n \ln \left(\frac{P(y_i|X=0)}{P(y_i|X=1)}\right) \\
= \sum_{i=1}^n L(y_i|X)
$$

- it can be argued then that the update rule is:

$$
\mu_{i \rightarrow j}^{(l)} = 
L_i + \sum_{j' \in N(i)\setminus\{j\}} \mu_{j' \rightarrow i}^{(l)}.
$$


::right::
<img
  class="w-100"
  src="/VN_update.png"
  alt="VN Update"
  style="display: block; margin: 0 auto;"
/>

- where the sum runs over all incident edges apart from the one under update


---
transition: fade-out

---

::header::
# Belief propagation: Sum Product algorithm

::footer::
We can finally state a complete algorithm for the iterative decoding of a Linear Code. 

<Definition title="Connection Node sets">

Let us define the sets of connections in the bipartite graph representing the LDPC code:

$$
N(i) \qquad \text{Set of check nodes connected to the variable node i.} \\
M(j) \qquad \text{Set of variable nodes connected to the check node j}
$$

</Definition>


---
transition: fade-out

---

::header::
# Belief propagation: Sum product algorithm

::left::
<div class="text-xs">
Step 1: Initialization (Variable Nodes)

Initialize messages from each variable node $i$ to each check node $j \in N(i)$:
$$
\mu_{i \rightarrow j}^{(0)} = L_i,
$$
where $L_i$ is the Log-Likelihood Ratio (LLR) for the received bit associated with node $i$.


Step 2: Check Node Update

Compute the message from each check node $j$ to variable node $i \in M(j)$ at iteration $l$:
$$
\mu_{j \rightarrow i}^{(l)} =
2\,\tanh^{-1}
\left(
\prod_{i' \in M(j)\setminus\{i\}} 
\tanh\left(\frac{\mu_{i' \rightarrow j}^{(l-1)}}{2}
\right)
\right).
$$
</div>

::right::

<div class="text-xs">
Step 3: Variable Node Update

Compute updated messages from each variable node $i$ to each check node $j \in N(i)$:
$$
\mu_{i \rightarrow j}^{(l)} = L_i + \sum_{j' \in N(i)\setminus\{j\}} \mu_{j' \rightarrow i}^{(l)}.
$$

Step 4: Total Final LLR and Check

Compute the final LLR for each variable node $i$:
$$
L_i^{\text{total}} = L_i + \sum_{j \in N(i)} \mu_{j \rightarrow i}^{(l)}.
$$

Estimate transmitted bits $\hat{x}_i$ as:
$$
\hat{x}_i = 
\begin{cases}
    0, & \text{if } L_i^{\text{total}} \geq 0,\\[6pt]
    1, & \text{otherwise.}
\end{cases}
$$

- Continue until $H \,\hat{x}_i = 0$ successful decoding or max iteration
</div>

---
transition: fade-out

---

::header::
# Back to QKD: syndrome decoding

::footer::
We have seen the algorithm for normal error correction. It is not hard to see that the same algorithm would work for syndrome decoding with a very minimal change. 

<Box title="Exercise: SPA Syndrome Decoding">

Can you go through the sketch proof of the SPA algorithm and see what needs to be changed in order for Bob to decode to the syndrome provided by Alice instead of decoding for a valid codeword?

Hint: normal SPA decoding is basically syndrome decoding to the all zero syndrome.

</Box>

---
transition: fade-out

---

::header::
# Back to QKD: syndrome decoding

::footer::
In the context of QKD we would like to perform Slepian Wolf Asymmetric source coding.

This amounts to do Syndrome Decoding instead of adding parity bits and decode to the zero syndrome.


<Box title="Protocol">

  1. Alice and Bob, according to the estimated QBER, select the best matrix and code rate and share this info.
  2. Alice computes the syndrome of her own data and sends it to Bob. (Direct Reconciliation)
  3. Bob Decodes his data to the closest string inside the coset determined by Alice Syndrome.
  4. Bob sends Alice the index of the frames that have been decoded correctly (according to him)
  5. Alice and Bob verify up to a certain probability their EC data, using a hash of their corrected data. (EC verification)
</Box>

---
transition: fade-out

---

::header::
# Cyles, Trees and optimality of the decoder

::footer::

<Box title="SPA Assumptions">

1. it is a bitwise MAP decoding
2. the codebits are independent and identically distributed
3. the messages are independent

</Box>

Critically the 3. is never met.

While computing updates of the messages, the decoders eventually meets some node that was already met before. All practical codes have cycles. 

<Box>

- SPA implements bitwise MAP decoder optimally only for cycle free codes
- Codes without cycles (Tanner graph is a tree) have a lot of weight 2 (= min distance 2) codewords

</Box>


---
transition: fade-out

---

::header::

# Further knowledge

- According to a QBER, we choose a fixed matrix with a certain code rate = certain gap to capacity (efficiency) 
- If the channel QBER is not stable or we do not have enough matrices: adaptive EC, puncturing-shortening
- Verification step, hash functions and $\epsilon$ security. Protocol is secure up to a certain small probability
- Reverse reconciliation: It might be more efficient if Alice tries to guess Bob's data. 
e.g. In CV - QKD with direct reconciliation DR cannot extract secure keys in a scenario where the losses in the channel are more that 3dB (15 km)



---
transition: fade-out

---

::header::

# Reconciliation vs lossy channel in DV

::left::

Quantum channel model:

$$y = x \oplus z$$
the z noise (QBER) is straightforward modeled as a BSC.

1. compute the syndrome s on x and decode y to s
2. generate a random $u \in \mathcal{C}$, i.e. $Hu=0$ and modulate x and send the result to Y. 

$$\alpha = u \oplus x$$

Y uses its data, y to build a virtual received lossy version of the input u: 
$$\alpha \oplus y = u \oplus x \oplus y = u \oplus z$$ 

::right::


![BSC](/bsc.png)

So it is equivalent to a virtual classical lossy (BSC) channel where the noise is the same as the original Quantum QBER, z

if u is chosen random (in the code $\mathcal{C}$) $\alpha$ is leaking the same amount of info as the syndrome


---
transition: fade-out

---

::header::

# Gaussian Modulation

::left::

in CV we can do something similar using a BiAWGN with $SNR = s$ channel instead of BSC. 


For gaussian mod. The Quantum Channel model is the linear:

$$Y = X + Z \qquad \text{where} \qquad Z \sim \mathcal{N}(0, \frac{1}{s})  $$
Technical Problems:
1. states needs to be uniform (they are gaussian)
2. the code needs to be a good partition of the total space

Solution: 
We can use the sign as information and the modulus as side information and transform the virtual channel to a BiAWGN. (i.e. use spherical codes where the inputs are uniform)

::right::

![BiAWGN](/biawgn.png)

<div class="text-center">
<img src="/CV_states.png" class="w-80" style="display: block; margin: 0 auto;">
</div>


---
transition: fade-out
---


::header::

# Multidimensional Reconciliation

::left::

Real channel 
$$
V_B = \frac{T\eta}{2} V_A + \frac{\epsilon}{2} + \nu_{\text{elec}} + 1
$$

$$
y = x + n  \qquad \text{where} \qquad y, x \; \text{gaussian} \\
$$

Virtual channel, generate random  input $u \in \{-1, 1\}$

$$
u \rightarrow u^\prime = u + n^\prime \\
$$

how are the two noises $n$ and $n^\prime$ related?

$$
\alpha = u \,x \quad \text{sent into classical channel}\\ 
u^\prime = \alpha y^{-1} = u x y^{-1} \\
= u (y - n)y^{-1} 
= u - \frac{u}{y} \,n
$$

::right::

Y knows the amplitude of Y so it can renormalize it symbol by symbol. 

This can be done in certain dimensions, i.e. we group symbols in sets and perform multiplications and division in the algebras of:

(1: real,  2: complex, 4: quaternions, 8: octonions)


The noise of the virtual channel is still gaussian, with a small change due to the dimensionality of the space used.

$$
n  \sim \mathcal{N}(0, \sigma^2) \\
n^\prime  \sim \mathcal{N}(0, \frac{\sigma^2}{d})\\
$$

---
transition: fade-out

---

::header::
# Privacy Amplification


::left::
A and B share a string (weak key) from a distribution P(X). Eve has some (quantum) side information. The qc-state is:

$$
\rho_{XE} = \sum_X p_x\ket{x} \bra{x} \otimes \rho^E_x
$$

<Box title="Goal">

Alice and Bob, using the classical channel can achive the same string:

- un-correlated with respect to  Eve's side information 
- uniform over a subset of the original bits (as large as possible, given Eve's side information)

</Box>
  
::right::

<img src="/BB_PA.png">


---
transition: fade-out

---

::header::
# Randomness extraction

<Definition title="Uniform and uncorrelated state">

This state is our goal or ideal state for a randomness extraction.

$$
\rho^{ideal}_{XE} =
\frac{1}{2^n}\mathbb{1}_X \otimes \rho_E
$$

</Definition>

<Definition title="epsilon ignorance">

We have a simple notion of measuring how far we get from this ideal:

$$
||\rho^{real}_{XE}, \rho^{ideal}_{XE}||_1 \le \epsilon
$$

</Definition>

where $||.||_1$ is the Trace distance. 

  
---
transition: fade-out

---

::header::
# No deterministic Randomness Extractors

<Definition title="k-source">

  A k-source is a qc-state of A classical state and E quantum state with side information on A such that:

  $$
  H_{\text{min}}(A|E) \ge k
  $$

</Definition>

<Theorem title="No General Deterministic randomness extractors">

  For any $Ext: \{0,1\}^n \rightarrow \{0, 1\}$ there exists an (n-1)-source X s.t Ext(X) is constant

</Theorem>

---
transition: fade-out

---

::header::
# Seeded extractors 

<Definition title="Weak (strong) seeded extractor">

  A $(k,\epsilon)$-weak seeded extractor is a function:

  $$
  Ext: \{0,1\}^n x \{0,1\}^d  \rightarrow \{0,1\}^m 
  $$

  s.t. for any k-source $\rho_{XE}$

$$
||\rho_{Ext(A,S)E},\frac{1}{2^n}\mathbb{1}_X \otimes \rho_E
 ||_1 \le \epsilon
$$

where S is uniform and not known to E.

It is called a strong extractor if the seed is also known to the Evesdropper

$$
||\rho_{Ext(A,S)E},\frac{1}{2^n}\mathbb{1}_X \otimes \rho_{SE}
 ||_1 \le \epsilon
$$

</Definition>

---
transition: fade-out

---

::header::
# Hashes as Seeded extractors 

We use families of hash functions. We select one hash at random (seed).

Desiderata:

- large m (output)
- small seed d
- small $\epsilon$
- extract $H_{min}(A|E)$

select a linear combination of bits at random (parity bits) and share with Bob the positions (seed)

$$d \sim m\,n$$


---
transition: fade-out

---

::header::
# 2-universal hash functions 

::footer::

<Definition title="2-universal hash function">

$$
\mathcal{F} = \{f: \{0,1\}^n \rightarrow \{0,1\}^m \}
$$

is 2-universal iff:

for any $x \ne x^\prime$  and $z \ne z^\prime$  with $x,x^\prime \in \{0,1\}^n$ and $z,z^\prime \in \{0,1\}^m$

$$
P_{f \in \mathcal{F}}  \left\{ f(x) = z \land f(x^\prime) = z^\prime \right\} = \frac{1}{2^{2m}}
$$

</Definition>


---
transition: fade-out

---

::header::
# Leftover hashing Lemma

::footer::

<Theorem title="Leftover hashing lemma">

Let n and $k \le n$   and arbitrary integer $\epsilon$

The Extractor based on a 2-universal family of hash defined by:

$$
\mathcal{F} = \{f_d: \{0,1\}^n \rightarrow \{0,1\}^m \}
$$

with:

$$ m = k - 2\;\log \frac{1}{\epsilon} $$
is a $(k,\epsilon)$-strong seeded extractor

</Theorem>


---
transition: fade-out

---

::header::
# Privacy Amplification Implementation

::left::

Given that strong seeded extractors allow for the seed to be disclosed we use it to interactively choose the same hash in Alice and Bob

Things to consider for a secure and stable implementation

- Compuitational time
- Short seeds
- Constant time operations
- Numerical stability

[Cryptomite - randomness extraction](https://github.com/CQCL/cryptomite) - Great tool for research in randomness estraction and benchmarking (not extremely fast, python, but quite extensive)


---
transition: fade-out

---

::header::
# Toeplitz matrices 

<Definition title="Toeplitz matrix from seed">

Given a seed vector \( s \) of length \( d \):

$$
s = [s_0, s_1, s_2, \dots, s_{d-1}]
$$

we define the $m \times n$ Toeplitz matrix $T_s$, with $d = m + n - 1$, as follows:

$$
T_s =
\begin{pmatrix}
s_{n-1} & s_{n-2} & s_{n-3} & \dots & s_0 \\
s_{n} & s_{n-1} & s_{n-2} & \dots & s_{1} \\
s_{n+1} & s_{n} & s_{n-1} & \dots & s_{2} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
s_{n+m-2} & s_{n+m-3} & s_{n+m-4} & \dots & s_{m-1}
\end{pmatrix}
$$

</Definition>

Formally, each entry is defined as:

$$
(T_s)_{i,j} = s_{n - 1 + i - j}
$$


---
transition: fade-out

---

::header::
# Toeplitz matrices - Example

::footer::

<Box title="Example Toeplitz">

- Input vector $X$ of length $n = 3$: $X = [x_0, x_1, x_2]^T$.
- Seed vector $S$ of length $d = n + m - 1 = 4$: $S = [s_0, s_1, s_2, s_3]$.
- Output vector length $ m = 2 $.

The Toeplitz matrix constructed from the seed $ S $ is given by:

$$
T_S = \begin{pmatrix}
s_2 & s_1 & s_0 \\
s_3 & s_2 & s_1
\end{pmatrix}
$$

Then, the output vector $Y$ produced by the Toeplitz extractor is:

$$
Y = T_S \cdot X =
\begin{pmatrix}
s_2 & s_1 & s_0 \\
s_3 & s_2 & s_1
\end{pmatrix}
\begin{pmatrix}
x_0 \\ x_1 \\ x_2
\end{pmatrix} =
\begin{pmatrix}
s_2 x_0 + s_1 x_1 + s_0 x_2 \\
s_3 x_0 + s_2 x_1 + s_1 x_2
\end{pmatrix}
$$

</Box>

---
transition: fade-out

---

::header::
# Toeplitz Extractor


<Definition title="Toeplitz extractor">

The Toeplitz extractor $T(X, S) : {0,1}^n \times {0,1}^{n+m-1} \rightarrow {0,1}^{m}$ is built from a seed $S = (S_0, \dots, S_{n+m-2})$. Given the weak input $X = (x_0, \dots, x_n)$ we can extract  $Y = (y_0, \dots, y_{m-1})$ by:

$$
	Y = T(X,S) = T_S\,X
$$

</Definition>

<Theorem title="Toeplitz strong seeded extractor">

The Toeplitz extractor is a strong classical and quantum $(k, n+m-1, \epsilon, n, m)$-seeded randomness extractor, where:

$$
	m \le k - 2\, \log_2\left(\frac{1}{\epsilon}\right)
$$

</Theorem>



---
transition: fade-out

---

::header::
# Toeplitz Extractor - implementation complexity

- It requires in principle $O(n\;m)$ operations, to compute the matrix vector multiplication.
- We can speed up this calculations to $O(n\, \log(n))$

We need to first realize the relation between Toeplitz matrices and convolutions.

For the previous example:

$$
T_S \cdot X = (X * [s_3, s_2, s_1, s_0])_{[2:3]}.
$$



---
transition: fade-out

---

::header::

# FFT Toepliz matrix multiplication with circulant embeddings

<Definition title="Circulant">

A circulant nmatrix $C$ generated from a vector $c = [c_0, c_1, c_2, \dots, c_{n-1}]$ is defined as:

$$
C = \begin{pmatrix}
	c_0 & c_{n-1} & c_{n-2} & \dots & c_1 \\
	c_1 & c_0 & c_{n-1} & \dots & c_2 \\
	c_2 & c_1 & c_0 & \dots & c_3 \\
	\vdots & \vdots & \vdots & \ddots & \vdots \\
	c_{n-1} & c_{n-2} & c_{n-3} & \dots & c_0
\end{pmatrix}
$$

Each row is a circular shift of the preceding row.

</Definition>

---
transition: fade-out

---

::header::

# FFT Toepliz matrix multiplication with circulant embeddings

::footer::

Multiplication of a circulant matrix $C$ by a vector $x$ corresponds exactly to the $\textbf{circular convolution}$ 

$$c \circledast x$$ 

Specifically:

$$
(Cx)_k = (c \circledast x)_k = 
\sum_{j=0}^{n-1} c_j \, x_{(k - j) \bmod n}
$$

---
transition: fade-out

---

::header::

# FFT Toepliz matrix multiplication with circulant embeddings

Circulant and the FFT. 

As usual if you want to compute the convolution it is best to go to Fourier space

- Compute the FFTs of vectors $c$ and $x$:
$$
C(\omega) = \text{FFT}(c), \quad X(\omega) = \text{FFT}(x)
$$

- Multiply these transforms element-wise:
$$
Y(\omega) = C(\omega) \cdot X(\omega)
$$

- Compute the inverse FFT:
$$
y = \text{FFT}^{-1}(Y(\omega))
$$

The vector $y$ obtained is exactly $c \circledast x$.


---
transition: fade-out

---

::header::

# Algebraic point of view of Circulants and FFT

Denote $F_{ij} = w_{ij}$ the matrix representation of the DFT, where $w_{ij}$ are the primitive root of unity. 

One can show that $F$ is exactly the Unitary matrix that diagonalizes $C$:

$$
	F\,C\,F^{-1} = \text{diag}(F\,S)
$$

so that the components of the DFT of the seed are the eigenvalues of C.

from here one can rearrange the last equation:

$$
Y = F^{-1} (\,\text{diag}(FS) \,FX)
$$

which is what we used before.


So, the steps to follow to efficiently compute the Toeplitz hashing are:

---
transition: fade-out

---

::header::

# Toeplitz Hashing


-  Given Toeplitz matrix $T$ of size $m \times n$, embed it into a circulant matrix of size $n+m-1$ (or typically the next power-of-two).
-  Pad both input vectors (seed and data) with zeros to match this size.
-  Perform circular convolution via FFT and extract relevant components from the resulting vector.



The computational complexity reduces from $O(mn)$ to $O((n) \log (n))$.

This is due to the fact that computing the FFT or its inverse can be achieved in $O(n\,\log(n))$, while the scalar multiplication between the vector in Fourier space has a complexity of just $O(n)$.


---
transition: fade-out

---

::header::

# Modified Toeplitz method

[Hayashi and Tsurumaru](https://arxiv.org/abs/1311.5322) found a modification of Toeplitz hashing and proved the leftover hashing lemma for those hashes:

- Including two sources. This can also be seen as including in the LHL a penalty for the seed not being completely random (another $\epsilon_s$) 
- Reduced seed length from $n+m-1 \rightarrow n-1$




::notes::
M. Hayashi and T. Tsurumaru, More Efficient Privacy Amplification With Less Random Seeds via Dual Universal Hash Function, IEEE Transactions on Information Theory, 10.1109/TIT.2016.2526018.


---
transition: fade-out

---

::header::

# Modified Toeplitz method

- Build a toeplitz matrix from the original one: $G_{(m,n)} = [I_m | T_{(m, n-m)}]$

$$
Y_m = G{(m,n)} X_n \\
= [I_{(m,x)}|T_{(m, n-m)}] 
\begin{bmatrix} X_m \\ X_{(n-m)} \end{bmatrix} \\
= I_{(m,m)} X_m \oplus T_{(m,n-m)}X_{n-m} \\
= X_m \oplus Y'_m
$$

Now, the seed to define the toeplitz matrix T has length:

$$
(n-m) + m - 1 = n-1
$$
::notes::
M. Hayashi and T. Tsurumaru, More Efficient Privacy Amplification With Less Random Seeds via Dual Universal Hash Function, IEEE Transactions on Information Theory, 10.1109/TIT.2016.2526018.


---
transition: fade-out

---

::header::

# LuxQuanta's opportunities

- 

