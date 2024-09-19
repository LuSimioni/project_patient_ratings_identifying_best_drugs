from pydantic import BaseModel, PositiveInt


class SchemaDados(BaseModel):

    urlDrugName: str
    rating: PositiveInt
    effectiveness: str
    sideEffects: str
    condition: str
    benefitsReview: str
    sideEffectsReview: str
    commentsReview: str

    