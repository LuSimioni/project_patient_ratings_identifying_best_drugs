import pandera as pa
from pandera.typing import Series


class SchemaCRM(pa.SchemaModel):
    id: Series[int] = pa.Field(
        ge=0,
        le=2,
        nullable=False,
        description=None,
    )
    
    url_drug_name: Series[str] = pa.Field(
        nullable=False,
        description=None,
    )
    
    rating: Series[int] = pa.Field(
        ge=1,
        le=10,
        nullable=False,
        description=None,
    )
    
    effectiveness: Series[str] = pa.Field(
        nullable=False,
        description=None,
    )
    
    side_effects: Series[str] = pa.Field(
        nullable=False,
        description=None,
    )
    
    condition: Series[str] = pa.Field(
        nullable=False,
        description=None,
    )
    
    benefits_review: Series[str] = pa.Field(
        nullable=False,
        description=None,
    )
    
    side_effects_review: Series[str] = pa.Field(
        nullable=False,
        description=None,
    )
    
    comments_review: Series[str] = pa.Field(
        nullable=False,
        description=None,
    )
    
    @pa.check_input
    class Index(pa.Index):
        dtype = "int64"
        ge =0
        nullable = False

    class Config:
        strict = False
        coerce = True