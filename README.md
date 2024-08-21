# **BPE ( Byte Pair Encoding )**
## **Neural Machine Translation of Rare Words with Subword Units**
https://arxiv.org/pdf/1508.07909
### ( Subword Units를 활용한 희귀 단어의 신경만 기계 번역 )

저자: **Rico Sennrich** and **Barry Haddow** and **Alexandra Birch** <br>
University of Edinburgh <br>Jun 10 2016

--------------------------------

#### 1994년 Philip Gage이 제안한 **데이터 압축 알고리즘** 을 자연어 처리의 분리 알고리즘으로 응용
[BPE 데이터알고리즘 (A New Algorithm for Data Compression)](http://www.pennelynn.com/Documents/CUJ/HTML/94HTML/19940045.HTM)
- 데이터의 크기를 줄이기 위한 압축 알고리즘
- 자주 발생하는 비트 패턴을 짧은 표현으로 대체, 일반적인 바이트 쌍을 단일 바이트로 대체 하는 것
    - ex ) 원래 입력 데이터 문자열: ABABCABCD
    - -> 쌍 AB를 사용하지 않은 X로 변경: XXCXCD
    - -> 쌍 XC를 사용하지 않은 Y로 변경: XYYD
- 가장 큰 장점은 이렇게 데이터를 압축한다 해도 데이터 크기가 증가하지 않으며, 압축 및 확장 알고리즘 모두 메모리가 매우 적게 사용된다.

--------------------------------

## 자연어 처리에서의 BPE :
- 기존 NMT 모델은 고정된 어휘로 작업하기 때문에, 번역 작업에서는 희귀단어에 대해 OOV 문제가 빈번하게 발생한다. 번역 작업에서는 개방형 어휘가 필요하기 때문에 BPE 알고리즘을 참고하여, 적용
- 서브워드 분리(subword segmentation) 알고리즘
- 글자(charcter) 단위에서 점차적으로 단어 집합을 만들어 내는, "Bottom up" 방식의 접근

--------------------------------

# **논문 요약**

### **초론**
- 기존 NMT의 문제점 설명. 번역 작업에는 개방형 어휘가 필요하다.
- 문제점을 보완하기 위해, N-gram과 바이트 쌍 인코딩 알고리즘(BPE)를 사용
- 보완한 모델을 통해 영어 > 독일어 / 영어 > 러시아어 번역 작업에서 BLEU 점수가 각각 1.1 , 1.3까지 향상됨

※ BLEU(Bilingual Evaluation Understudy) : 기계 번역 시스템의 성능을 평가하는 데 사용되는 대표적인 자동 평가 척도. 번역된 텍스트의 품질을 측정하기 위해 인간 번역과 기계 번역 간의 유사성을 비교하는 방식으로 동작

### **소개**
- 신경망 기계 번역 NMT 한계점 설명 ( 위와 같음 )
- 본 논문의 주요 기여
    - 서브워드 유닛을 통해 (희귀) 단어를 인코딩하여 개방형 어휘 신경망 기계 번역이 가능함을 입증
        - 중국어 번역(하위 단어 단위로 인코딩)방식을 통해 해당 방식이 더 간단하고 효과적이라는 것을 알게됨
    - BPE을 단어 세분화 작업에 적응시켜, 가변 길이 문자 시퀀스를 통해 고정 크기 어휘를 사용하여 개방형 어휘를 표현할 수 있음을 확인
 
 --------------------------------

### **2. NMT(Neural Machine Translation)**
Bahdanau et al.(2015)의 신경만 기계 번역 아키텍쳐 NMT에 대한 요약이므로 생략

### **3. Subword Translation**
- 기존 NMT로 OOV가 발생하는 아래 단어들도 서브워드 유닛을 사용해서 번역이 가능하다.
  - named entities, 동일한 알파벳을 공유하는 고유 명사 ( 언어가 다른 경우, 전사나 음역이 필요 )
  - 동족어 및 외래어 : 각 언어 간에 규칙적으로 다를 수 있으므로, 문자 수준의 번역 규칙으로 충분
  - 형태소가 복잡한 단어: 복합, 부착 또는 굴절을 통해 형성된 여러 형태소를 개별적으로 번역하여 번역할 수 있다.


- 해당 논문에서는 독일어를 기준으로, 100개의 독일어 희귀단어를 분석하여, 대부분의 단어들이 영어로 더 작은 단위로 나누어 번역할 수 있음을 확인

### 결론
희귀 단어들을 Subword Unit으로 표현해서 개방형 어휘 번역이 가능함을 확인함
해당 방법이 단순한 NMT의 백오프 번역 모델을 사용하는 것보다 더 간단하고 효과적임을 입증

## **BPE 알고리즘 설명 및 예시**

파이썬 코드로 논문에 설명되어 있다.<br>
<br>
<img src='https://drive.google.com/uc?export=download&id=160yceCoUWt4ricIy0WH0VZESbqtfJLlj' width="" height ="" />


 --------------------------------

```
import re, collections

def get_stats(vocab):
  pairs = collections.defaultdict(int)
  for word, freq in vocab.items():
    symbols = word.split()
    for i in range(len(symbols)-1):
      pairs[symbols[i], symbols[i+1]] += freq
  print('현재 pair들의 빈도수 :', dict(pairs)) # 프린트문 추가
  return pairs

def merge_vocab(pair, v_in):
  v_out = {}
  bigram = re.escape(' '.join(pair))
  p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
  for word in v_in:
    w_out = p.sub(''.join(pair), word)
    v_out[w_out] = v_in[word]
  return v_out

vocab = {'l o w': 5,
     'l o w e r': 2,
     'n e w e s t': 6,
     'w i d e s t':3}

num_merges = 10   # 동작 횟수
for i in range(num_merges):
  pairs = get_stats(vocab)
  best = max(pairs, key=pairs.get)
  vocab = merge_vocab(best, vocab)

  # 결과 확인을 위해 프린트문 추가'
  print('[dictionary update!]')
  print(best[0] + best[1])
  print(best)
  print(vocab)
  print('--------------------------------------------------------------')
```

## **코드 예제 설명**

- 어떤 훈련 데이터로부터 각 단어들의 빈도수를 카운터 했다고 가정하자
  - -> low : 5개, lower : 2개, newest : 6개, widest : 3개
- 해당 단어 사전에는 단어 4개가 존재하는데, 만약 'lowest'란 단어가 등장하면, 해당 단어는 학습한 적이 없으므로, OOV가 발생할 것이다.

**BPE 알고리즘 사용**
- 우선 모든 단어들을 chracter 단위로 분리
  - -> 'l', 'o', 'w', 'e', 'r', 'n', 'w', 's', 't', 'i', 'd'
- BPE의 특징은 알고리즘의 동작을 몇 회 반복(iteration)할 것인지를 사용자가 조절 할 수 있다.
  - 예제에서는 10회로 설정했다.
      - 1회 : 빈도수가 9로 가장 높은 (e, s)의 쌍을 es로 통합
      - 2회 : 빈도수가 9로 가장 높은 (es, t)의 쌍을 est로 통합
      - 3회 : 빈도수가 7로 가장 높은 (l, o)의 쌍을 lo로 통합
      ....

      - 최종 단어집합 :
      l, o, w, e, r, n, w, s, t, i, d ( 기존 단어집합 )<br>
      es, est, lo, low, ne, new, newest, wi, wid, widest ( BPE를 통해 추가된 단어 집합 )


**결론**

- 이제 기존 단어 사전에 없던 단어인 'lowest' 단어가 등장 시, 글자 단위로 분할 후, lowest -> 'low' 와 'est' 단어로 인코딩이 되기 때문에, 단어 집합에 있는 단어로 OOV가 발생하지 않음

### **평가 및 분석**
대충 훨씬 좋긴 하더라 하는 내용

<img src='https://drive.google.com/uc?export=download&id=1qv4OOna3s9cyiyo3P4JZVrAa8i7ubCCZ' width="" height ="" /><br>

### **결론**

- 서브워드 유닛을 활용한 NMT 모델은 단순하고 효과적이며, 희귀 단어와 미지의 단어를 더 잘 처리할 수 있다.
- BPE를 사용한 단어 세분화는 개방형 어휘 번역을 가능하게 하며, 이는 기존의 방법보다 더 나은 성능을 보여줌, 이러한 접근 방식은 NMT 모델의 번역 품질을 향상시키고, 더 넓은 범위의 단어를 처리할 수 있게함

















