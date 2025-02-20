# Copyright 2019 kubeflow.org.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
from typing import Callable, List, Dict

import kfserving
import numpy as np
import spacy
import alibi
from alibi.utils.download import spacy_model
from alibiexplainer.explainer_wrapper import ExplainerWrapper

logging.basicConfig(level=kfserving.server.KFSERVER_LOGLEVEL)


class AnchorText(ExplainerWrapper):

    def __init__(self, predict_fn: Callable, explainer: alibi.explainers.AnchorText,
                 spacy_language_model: str = 'en_core_web_md', **kwargs):
        self.predict_fn = predict_fn
        self.kwargs = kwargs
        logging.info("Anchor Text args %s", self.kwargs)
        if explainer is None:
            logging.info("Loading Spacy Language model for %s", spacy_language_model)
            spacy_model(model=spacy_language_model)
            self.nlp = spacy.load(spacy_language_model)
            logging.info("Language model loaded")
        self.anchors_text = explainer

    def explain(self, inputs: List) -> Dict:
        if self.anchors_text is None:
            self.anchors_text = alibi.explainers.AnchorText(self.nlp, self.predict_fn)
        # We assume the input has batch dimension but Alibi explainers presently assume no batch
        np.random.seed(0)
        anchor_exp = self.anchors_text.explain(inputs[0], **self.kwargs)
        return anchor_exp
