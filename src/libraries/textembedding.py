from fastembed import TextEmbedding
from fastembed.common.model_description import PoolingType, ModelSource
from numpy import ndarray, array, linalg

hugging_face_model = "Salesforce/SFR-Embedding-Code-400M_R"

TextEmbedding.add_custom_model(
    model=hugging_face_model,
    pooling=PoolingType.MEAN,
    normalization=True,
    sources=ModelSource(hf=hugging_face_model),  # hugging face model
    dim=1024,
    model_file="onnx/model.onnx",
)

textembedding = TextEmbedding(hugging_face_model)


def get_embedding(text: str) -> ndarray:
    doc = list(textembedding.embed([text]))

    # normalize result
    vec = array(doc[0])  # convert list to numpy array
    vec = vec / linalg.norm(vec)  # divide by L2 norm
    vec = vec.tolist()

    return vec
