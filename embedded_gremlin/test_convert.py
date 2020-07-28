#
#  Copyright (c) 2020 IBM Corp.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import unittest

import spacy

_SPACY_LANGUAGE_MODEL = spacy.load("en_core_web_sm")

from text_extensions_for_pandas.io import make_tokens_and_features
from embedded_gremlin.convert import token_features_to_traversal


_TEST_TEXT = "Item's for < $100 & change"
_TEST_TOKS = make_tokens_and_features(_TEST_TEXT, _SPACY_LANGUAGE_MODEL)


class ConvertTest(unittest.TestCase):
    def test_token_features_to_traversal(self):
        g = token_features_to_traversal(_TEST_TOKS)
        result = g.V().has("tag", "NNP").as_("src").toList()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "v[0]")
