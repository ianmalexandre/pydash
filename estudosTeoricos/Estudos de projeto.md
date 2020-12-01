Estudos de projeto
==================

Primeiro artigo - **[A Survey on Bitrate Adaptation Schemes for
Streaming Media Over HTTP](https://aprender3.unb.br/pluginfile.php/597790/mod_resource/content/1/A%20Survey%20on%20Bitrate%20Adaptation%20Schemes%20for%20Streaming%20Media%20Over%20HTTP.pdf)**
------------------------------------------------------------

Este artigo compara os diferentes tipos de implementação de HAS (HTTP adaptative streaming), explicando o seu uso e principais algoritmos utilizados. Para o nosso caso, estamos estudando apenas os casos de algoritmos baseados em clientes. O objetivo almeijado pelo algoritmo é:
* O mínimo de rebuffering possível quando esgota-se o espaço
* Mínimo de tempo de startup
* Um alto bitrate médio, respeitando os limites da rede
* Mínimo de oscilações de qualidade de vídeo

<h3>Adaptação por banda livre disponível</h3>

A banda livre disponível é usualmente calculada tamanho dos segmentos recebidos dividido pelo tempo de transferência. 

<h3>Adaptação por ocupação de buffer</h3>

Leva em consideração o tamanho ocupado do buffer do player. O BOLA é uma implementação que utiliza tal abordagem.

Segundo artigo - [BOLA: Near-Optimal Bitrate Adaptation
for Online Videos](https://aprender3.unb.br/pluginfile.php/597791/mod_resource/content/1/BOLA%20Near-Optimal%20Bitrate%20Adaptation%20for%20Online%20Videos.pdf)
-----------------------------------------------------------------------------------------


