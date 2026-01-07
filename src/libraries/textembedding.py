from fastembed import TextEmbedding
from fastembed.common.model_description import PoolingType, ModelSource
from numpy import ndarray, array, linalg

TextEmbedding.add_custom_model(
    model="Salesforce/SFR-Embedding-Code-400M_R",
    pooling=PoolingType.MEAN,
    normalization=True,
    sources=ModelSource(hf="Salesforce/SFR-Embedding-Code-400M_R"), #hugging face model
    dim=1024,
    model_file="onnx/model.onnx",
)

textembedding = TextEmbedding("Salesforce/SFR-Embedding-Code-400M_R")


def get_embedding(text: str) -> ndarray:
    doc = list(textembedding.embed([text]))

    # normalize result
    vec = array(doc[0])  # convert list to numpy array
    vec = vec / linalg.norm(vec)  # divide by L2 norm
    vec = vec.tolist()

    return vec
