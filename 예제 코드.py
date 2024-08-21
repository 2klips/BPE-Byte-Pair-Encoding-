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
  
  ## **코드 예제 설명**

# - 어떤 훈련 데이터로부터 각 단어들의 빈도수를 카운터 했다고 가정하자
#   - -> low : 5개, lower : 2개, newest : 6개, widest : 3개
# - 해당 단어 사전에는 단어 4개가 존재하는데, 만약 'lowest'란 단어가 등장하면, 해당 단어는 학습한 적이 없으므로, OOV가 발생할 것이다.

# **BPE 알고리즘 사용**
# - 우선 모든 단어들을 chracter 단위로 분리
#   - -> 'l', 'o', 'w', 'e', 'r', 'n', 'w', 's', 't', 'i', 'd'
# - BPE의 특징은 알고리즘의 동작을 몇 회 반복(iteration)할 것인지를 사용자가 조절 할 수 있다.
#   - 예제에서는 10회로 설정했다.
#       - 1회 : 빈도수가 9로 가장 높은 (e, s)의 쌍을 es로 통합
#       - 2회 : 빈도수가 9로 가장 높은 (es, t)의 쌍을 est로 통합
#       - 3회 : 빈도수가 7로 가장 높은 (l, o)의 쌍을 lo로 통합
#       ....

#       - 최종 단어집합 :
#       l, o, w, e, r, n, w, s, t, i, d ( 기존 단어집합 )<br>
#       es, est, lo, low, ne, new, newest, wi, wid, widest ( BPE를 통해 추가된 단어 집합 )


# **결론**

# - 이제 기존 단어 사전에 없던 단어인 'lowest' 단어가 등장 시, 글자 단위로 분할 후, lowest -> 'low' 와 'est' 단어로 인코딩이 되기 때문에, 단어 집합에 있는 단어로 OOV가 발생하지 않음


