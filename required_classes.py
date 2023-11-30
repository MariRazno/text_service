import numpy as np
from typing import List


class BertEmbedder:
    def __init__(self, model_path:str, cut_head:bool=False):
        """
            cut_head = True if the model have classifier head
        """
        self.embedder = BertForSequenceClassification.from_pretrained(model_path)
        self.max_length = self.embedder.config.max_position_embeddings
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, max_length=self.max_length)

        if cut_head:
            self.embedder = self.embedder.bert

        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.embedder.to(self.device)

    def __call__(self, text: str):
        encoded_input = self.tokenizer(text, 
                                       return_tensors='pt', 
                                       max_length=self.max_length,
                                       padding=True,
                                       truncation=True).to(self.device)
        model_output = self.embedder(**encoded_input)
        text_embed = model_output.pooler_output[0].cpu()
        return text_embed.tolist()

    def batch_predict(self, texts: List[str]):
        encoded_input = self.tokenizer(texts, 
                                       return_tensors='pt', 
                                       max_length=self.max_length,
                                       padding=True,
                                       truncation=True).to(self.device)
        model_output = self.embedder(**encoded_input)
        texts_embeds = model_output.pooler_output.cpu()
        return texts_embeds

class PredictModel:
    def __init__(self, embedder, classifier, batch_size=8):
        self.batch_size = batch_size
        self.embedder = embedder
        self.classifier = classifier

    def _texts2vecs(self, texts, log=False):
        embeds = []
        batches_texts = np.array_split(texts, len(texts) // self.batch_size)
        if log:
            iterator = tqdm(batches_texts)
        else:
            iterator = batches_texts
        for batch_texts in iterator:
            batch_texts = batch_texts.tolist()
            embeds += self.embedder.batch_predict(batch_texts).tolist()
        embeds = np.array(embeds)
        return embeds

    def fit(self, texts: List[str], labels: List[str], log: bool=False):
        if log:
            print('Start text2vec transform')
        embeds = self._texts2vecs(texts, log)
        if log:
            print('Start classifier fitting')
        self.classifier.fit(embeds, labels)

    def predict(self, texts: List[str], log: bool=False):
        if log:
            print('Start text2vec transform')
        embeds = self._texts2vecs(texts, log)
        if log:
            print('Start classifier prediction')
        prediction = self.classifier.predict(embeds)
        return prediction
    
class CustomXGBoost:
    def __init__(self):
        self.model = xgb.XGBClassifier()
        self.classes_ = None

    def fit(self, X, y):
        self.classes_ = np.unique(y).tolist()
        y = [self.classes_.index(l) for l in y]
        self.model.fit(X, y)

    def predict_proba(self, X):
        pred = self.model.predict_proba(X)
        return pred

    def predict(self, X):
        preds = self.model.predict_proba(X)
        print(np.argmax(preds, axis=1), self.classes_)
        print(preds.shape, preds[:2])
        return self.classes_[np.argmax(preds, axis=1)]

class SimpleModel:
    def __init__(self):
        self.classes_ = None

    def fit(self, X, y):
        self.classes_ = [y[0]]

    def predict_proba(self, X):
        return np.array([[1.0]] * len(X))
