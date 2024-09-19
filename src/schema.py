import pandera as pa
from pandera.typing import Series


class ProdutoSchema(pa.SchemaModel):
    id: Series[int]  
    url_drug_name: Series[str]
    rating: Series[int] = pa.Field(ge=1, le=10)
    effectiveness: Series[str]
    side_effects: Series[str]
    condition: Series[str] = pa.Field(nullable=True)
    benefits_review: Series[str] = pa.Field(nullable=True)
    side_effects_review: Series[str] = pa.Field(nullable=True)
    comments_review: Series[str] = pa.Field(nullable=True)

    class Config:
        coerce = True
        strict = True
    
