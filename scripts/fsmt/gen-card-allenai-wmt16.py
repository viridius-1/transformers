#!/usr/bin/env python

# Usage:
# ./gen-card-allenai-wmt16.py

import os
from pathlib import Path

def write_model_card(model_card_dir, src_lang, tgt_lang, model_name):

    texts = {
        "en": "Machine learning is great, isn't it?",
        "ru": "Машинное обучение - это здорово, не так ли?",
        "de": "Maschinelles Lernen ist großartig, nicht wahr?",
    }

    # BLUE scores as follows:
    # "pair": [fairseq, transformers]
    scores = {
        "wmt16-en-de-dist-12-1": [28.3, 27.52],
        "wmt16-en-de-dist-6-1": [27.4, 27.11],
        "wmt16-en-de-12-1": [26.9, 25.75],
    }
    pair = f"{src_lang}-{tgt_lang}"

    readme = f"""
---
language:
- {src_lang}
- {tgt_lang}
thumbnail:
tags:
- translation
- wmt16
- allenai
license: Apache 2.0
datasets:
- http://www.statmt.org/wmt16/ ([test-set](http://matrix.statmt.org/test_sets/newstest2016.tgz?1504722372))

metrics:
- http://www.statmt.org/wmt16/metrics-task.html
---

# FSMT

## Model description

This is a ported version of fairseq-based [wmt16 transformer](https://github.com/jungokasai/deep-shallow/) for {src_lang}-{tgt_lang}.

For more details, please, see [Deep Encoder, Shallow Decoder: Reevaluating the Speed-Quality Tradeoff in Machine Translation](https://arxiv.org/abs/2006.10369).

All 3 models are available:

* [wmt16-en-de-dist-12-1](https://huggingface.co/allenai/wmt16-en-de-dist-12-1)
* [wmt16-en-de-dist-6-1](https://huggingface.co/allenai/wmt16-en-de-dist-6-1)
* [wmt16-en-de-12-1](https://huggingface.co/allenai/wmt16-en-de-12-1)

```
@misc{{kasai2020deep,
    title={{Deep Encoder, Shallow Decoder: Reevaluating the Speed-Quality Tradeoff in Machine Translation}},
    author={{Jungo Kasai and Nikolaos Pappas and Hao Peng and James Cross and Noah A. Smith}},
    year={{2020}},
    eprint={{2006.10369}},
    archivePrefix={{arXiv}},
    primaryClass={{cs.CL}}
}}
```

## Intended uses & limitations

#### How to use

```python
from transformers.tokenization_fsmt import FSMTTokenizer
from transformers.modeling_fsmt import FSMTForConditionalGeneration
mname = "allenai/{model_name}"
tokenizer = FSMTTokenizer.from_pretrained(mname)
model = FSMTForConditionalGeneration.from_pretrained(mname)

input = "{texts[src_lang]}"
input_ids = tokenizer.encode(input, return_tensors="pt")
outputs = model.generate(input_ids)
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded) # {texts[tgt_lang]}

```

#### Limitations and bias


## Training data

Pretrained weights were left identical to the original model released by allenai. For more details, please, see the [paper](https://arxiv.org/abs/2006.10369).

## Eval results

Here are the BLEU scores:

model   | fairseq | transformers
-------|---------|----------
{model_name}  | {scores[model_name][0]} | {scores[model_name][1]}

The score is slightly below the score reported in the paper, as the researchers don't use `sacrebleu` and measure the score on tokenized outputs. `transformers` score was measured using `sacrebleu` on detokenized outputs.

The score was calculated using this code:

```bash
git clone https://github.com/huggingface/transformers
cd transformers
export PAIR={pair}
export DATA_DIR=data/$PAIR
export SAVE_DIR=data/$PAIR
export BS=8
export NUM_BEAMS=5
mkdir -p $DATA_DIR
sacrebleu -t wmt16 -l $PAIR --echo src > $DATA_DIR/val.source
sacrebleu -t wmt16 -l $PAIR --echo ref > $DATA_DIR/val.target
echo $PAIR
PYTHONPATH="src:examples/seq2seq" python examples/seq2seq/run_eval.py allenai/{model_name} $DATA_DIR/val.source $SAVE_DIR/test_translations.txt --reference_path $DATA_DIR/val.target --score_path $SAVE_DIR/test_bleu.json --bs $BS --task translation --num_beams $NUM_BEAMS
```

"""
    model_card_dir.mkdir(parents=True, exist_ok=True)
    path = os.path.join(model_card_dir, "README.md")
    print(f"Generating {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(readme)

# make sure we are under the root of the project
repo_dir = Path(__file__).resolve().parent.parent.parent
model_cards_dir = repo_dir / "model_cards"

for model_name in ["wmt16-en-de-dist-12-1", "wmt16-en-de-dist-6-1", "wmt16-en-de-12-1"]:
    model_card_dir = model_cards_dir / "allenai" / model_name
    write_model_card(model_card_dir, src_lang="en", tgt_lang="de", model_name=model_name)
