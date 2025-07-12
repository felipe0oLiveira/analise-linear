# Análise Linear Matricial de Pórtico Plano

Este trabalho apresenta uma análise matricial detalhada de um pórtico hiperestático (uma estrutura com mais restrições do que o necessário para o equilíbrio estático), com o objetivo de compreender seu comportamento sob diferentes tipos de carregamento.

A metodologia central envolve a discretização do pórtico em elementos de barra, para os quais são calculadas as matrizes de rigidez local. Essas matrizes, que representam a resistência de cada elemento à deformação, são determinadas com base nas propriedades do material (módulo de elasticidade, área da seção transversal, momento de inércia) e nas dimensões geométricas de cada barra.

Para integrar o comportamento de cada elemento no sistema global, são utilizadas matrizes de rotação, que transformam as rigidezes locais para um sistema de coordenadas global, considerando a orientação de cada barra no espaço. A partir dessas matrizes locais e de rotação, é montada a matriz de rigidez global da estrutura, que descreve a rigidez total do pórtico.

Com a matriz de rigidez global estabelecida e os carregamentos aplicados (distribuídos e concentrados), o sistema de equações é resolvido para determinar os deslocamentos nodais (movimentos em cada ponto de conexão da estrutura) e as reações de apoio. A solução numérica obtida através do código Python foi validada por comparação com resultados de softwares comerciais de análise estrutural, como Ftool e Smath Solver.

O trabalho também inclui uma análise aprofundada dos esforços internos (forças normais, cortantes e momentos fletores) em cada barra, bem como a visualização da estrutura deformada em relação à sua configuração original. Os resultados permitem identificar as barras mais rígidas, entender as interações entre os graus de liberdade e confirmar que os deslocamentos são pequenos, o que é característico de estruturas com alta rigidez. Em suma, o estudo oferece uma compreensão abrangente do comportamento do pórtico sob carga, validada por diferentes abordagens computacionais.

**OBS:** Este trabalho foi realizado em colaboração com uma aluna de Engenharia Civil da UEFS. 