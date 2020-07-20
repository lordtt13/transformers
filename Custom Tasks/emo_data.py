# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" SemEval-2019 Task 3: EmoContext Contextual Emotion Detection in Text """

from __future__ import absolute_import, division, print_function

import os
import json
import gdown

import nlp


_CITATION = """\
@inproceedings{chatterjee-etal-2019-semeval,
    title = "{S}em{E}val-2019 Task 3: {E}mo{C}ontext Contextual Emotion Detection in Text",
    author = "Chatterjee, Ankush  and
      Narahari, Kedhar Nath  and
      Joshi, Meghana  and
      Agrawal, Puneet",
    booktitle = "Proceedings of the 13th International Workshop on Semantic Evaluation",
    month = jun,
    year = "2019",
    address = "Minneapolis, Minnesota, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/S19-2005",
    doi = "10.18653/v1/S19-2005",
    pages = "39--48",
    abstract = "In this paper, we present the SemEval-2019 Task 3 - EmoContext: Contextual Emotion Detection in Text. Lack of facial expressions and voice modulations make detecting emotions in text a challenging problem. For instance, as humans, on reading {``}Why don{'}t you ever text me!{''} we can either interpret it as a sad or angry emotion and the same ambiguity exists for machines. However, the context of dialogue can prove helpful in detection of the emotion. In this task, given a textual dialogue i.e. an utterance along with two previous turns of context, the goal was to infer the underlying emotion of the utterance by choosing from four emotion classes - Happy, Sad, Angry and Others. To facilitate the participation in this task, textual dialogues from user interaction with a conversational agent were taken and annotated for emotion classes after several data processing steps. A training data set of 30160 dialogues, and two evaluation data sets, Test1 and Test2, containing 2755 and 5509 dialogues respectively were released to the participants. A total of 311 teams made submissions to this task. The final leader-board was evaluated on Test2 data set, and the highest ranked submission achieved 79.59 micro-averaged F1 score. Our analysis of systems submitted to the task indicate that Bi-directional LSTM was the most common choice of neural architecture used, and most of the systems had the best performance for the Sad emotion class, and the worst for the Happy emotion class.",
}
"""

# TODO: Add description of the dataset here
_DESCRIPTION = """\
In this dataset, given a textual dialogue i.e. an utterance along with two previous turns of context, the goal was to infer the underlying emotion of the utterance by choosing from four emotion classes - Happy, Sad, Angry and Others. 
"""

class EmoConfig(nlp.BuilderConfig):
    """BuilderConfig for SQUAD."""

    def __init__(self, **kwargs):
        """BuilderConfig for EmoContext.
    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        super(EmoConfig, self).__init__(**kwargs)

_TEST_URL = "https://drive.google.com/file/d/1Hn5ytHSSoGOC4sjm3wYy0Dh0oY_oXBbb/view?usp=sharing"
_TRAIN_URL = "https://drive.google.com/file/d/12Uz59TYg_NtxOy7SXraYeXPMRT7oaO7X/view?usp=sharing"

class EmoDataset(nlp.GeneratorBasedBuilder):
    """ SemEval-2019 Task 3: EmoContext Contextual Emotion Detection in Text. Version 1.0.0 """

    VERSION = nlp.Version("1.0.0")
    force = False

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "text": nlp.Value("string"),
                    "label": nlp.features.ClassLabel(names=["others", "happy", "sad", "angry"]),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/S19-2005/",
            citation=_CITATION,
        )
    
    def _get_drive_url(self, url):
        base_url = 'https://drive.google.com/uc?id='
        split_url = url.split('/')
        return base_url + split_url[5]
    
    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if(not os.path.exists("emo-train.json") or self.force):
            gdown.download(self._get_drive_url(_TRAIN_URL), "emo-train.json", quiet = True)
        if(not os.path.exists("emo-test.json") or self.force):
            gdown.download(self._get_drive_url(_TEST_URL), "emo-test.json", quiet = True)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={
                    "filepath": "emo-train.json",
                    "split": "train",
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={"filepath": "emo-test.json", "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, 'rb') as f:
            data = json.load(f)
            for id_, text, label in zip(data["text"].keys(), data["text"].values(), data["Label"].values()):
                yield id_, {
                    "text": text,
                    "label": label,
                }
