Commenter 1
Major comment 1 Should use state of the art algorithm instead
Major comment 2 Should include data loading and readout cost
Major comment 3 / 4 Classical algorithm estimation inconsistency problem 
The main text refers to the conjugate gradient (CG) method as the equivalent classical baseline, which requires symmetric positive definite (SPD) systems, as noted in Appendix D. However, the analysis in Appendix D is based on CGNE. 
The classical CG runtime is estimated on a single desktop CPU at 1 GHz / 50 W, while the quantum side uses an optimized fault-tolerant architecture with O(105 ) physical qubits. This is not an apples-to-apples comparison. Appendix D compares against Cholesky decomposition on supercomputers, pushing the crossover to ∼ 2 100, yet this result appears only in the appendix. 
Major comment 5 HHL scaling analysis problem
The probabilistic bound (Eq. B19) used to prove Statement 1 is derived from numerical experiments on “small matrix size” (pg. 17), with the claim that “the error does not depend on n.” This claim is crucial for the entire scaling analysis, yet: (a) Figure 9 lacks axis labels and a description of the experimental setup; (b) the matrix sizes, distributions, and number of samples are not reported; (c) no rigorous justification is given for why small-matrix behavior should extrapolate to larger matrices. This needs to be explained clearly. 
Major comment 6 Assume logarithmic dependence k = s = log N is too optimistic
Commenter 2
Major Comment 1 The manuscript's strongest contribution is the framework, not the specific HHL case study 
Major Comment 2 The energy model needs greater robustness and sensitivity analysis 
Major Comment 3  Practical benchmarking should be more closely tied to scientific computing practice 
Major Comment 4 Clarify audience and manuscript positioning 
Major Comment 5 discussion session deviate from main topic 





Paper revise plan
Framework
Add framework (c2-1)
quantum part: logical complexity scaling + QEC overhead + physical hardware modeling  => function(pp,cq) = time; space; energy
classical part: instruction count scaling + physical hardware modeling = function(pp,cc) = time; space; energy


Quantum complexity scaling analysis:
fix the HHL scaling analysis issues
The probabilistic bound (Eq. B19) is based on small matrix numerical experiments, no justification of why large matrices would be the same. (c1-5)
The assumption of fixed matrix element positions should be removed
The s=k=log(N) is too optimistic, our assumption should tied to real world applications (c1-6 , c2-3)

add the SOTA algorithm (so we have two algorithms, by comparing them we could intuitively see how the algorithm developments affect the end-to-end performance) (c1-1)
For QLSA, we could change the algorithm to the SOTA: “an shortcut to optimal QLSA”, there exists T gate count analysis in Costa, Dalzell, An, and Berry, “Constant Factor Analysis of Optimal Quantum Linear Solvers in Practice” (2026) .
add the input/output overhead (c1-2)
For state preparation, because it goes into the quantum circuit, so we could say it is not the bottleneck and ignore it. For readout, because it goes into the circuit repetition, so it is multiplicative with the QLSA circuit cost and we have to address it. See (https://arxiv.org/abs/2111.10485)

QEC overhead analysis
We don’t have to change this part, but do note that there are many existing software for QEC overhead analysis, for example Qultran, we might verify our part with Qultran.

physical hardware modeling:
Do a more reasonable modeling
We could do something similar to ((https://arxiv.org/pdf/2603.28627, and https://arxiv.org/pdf/2308.08648, https://arxiv.org/abs/2505.15907) or just directly reference their work.
Add sensitivity analysis (c2-2)


classical algorithm scaling counting and physical hardware modeling
address c1-3,c1-4. (basically redo classical part)

real world application
study some applications (c2-3)
for example: elliptic PDE with a specified scalar output 

writing refine
address c2-4, c2-5



chatGPT advise
https://chatgpt.com/c/6a9f0e0b-3b60-83ea-8249-ed6680be5552
