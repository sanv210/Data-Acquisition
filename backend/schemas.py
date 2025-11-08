from typing import List, Literal
from pydantic import BaseModel, Field, constr, field_validator
from datetime import datetime


# ============================================================================
# Nested models for seq field
# ============================================================================

class SeqPurge(BaseModel):
    """Purge sequence configuration"""
    seq1: constr(pattern=r'^[0-9]+$') = Field(..., description="Purge duration (numeric string)")


class SeqSource(BaseModel):
    """Source sequence configuration"""
    seq1: Literal["3 Peak Spark", "Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning", "High Voltage Spark"]
    seq2: Literal["Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning", "High Voltage Spark", "AD OFFSET"]
    seq3: Literal["Lamp", "3 Peak Spark", "Normal Spark", "Combined Spark", "Arclike Spark", "Cleaning"]
    clean: Literal["Cleaning", "High Voltage Spark", "AD OFFSET", "ITG OFFSET", "MAIN OFFSET", "NOISE TEST"]


class SeqPreburn(BaseModel):
    """Preburn sequence configuration"""
    seq1: constr(pattern=r'^[0-9]+$') = Field(..., description="Preburn SEQ1 duration")
    seq2: constr(pattern=r'^[0-9]+$') = Field(..., description="Preburn SEQ2 duration")
    seq3: constr(pattern=r'^[0-9]+$') = Field(..., description="Preburn SEQ3 duration")
    clean: Literal["Pulse"]


class SeqInteg(BaseModel):
    """Integration sequence configuration"""
    seq1: constr(pattern=r'^[0-9]+$') = Field(..., description="Integration SEQ1 duration")
    seq2: constr(pattern=r'^[0-9]+$') = Field(..., description="Integration SEQ2 duration")
    seq3: constr(pattern=r'^[0-9]+$') = Field(..., description="Integration SEQ3 duration")
    clean: Literal["Pulse"]


class SeqClean(BaseModel):
    """Clean sequence configuration"""
    value: constr(pattern=r'^[0-9]+$') = Field(..., description="Clean duration")
    unit: Literal["Pulse"]


class Seq(BaseModel):
    """Complete sequence configuration"""
    purge: SeqPurge
    source: SeqSource
    preburn: SeqPreburn
    integ: SeqInteg
    clean: SeqClean


# ============================================================================
# Nested models for level_out_information field
# ============================================================================

class MonitorElement(BaseModel):
    """Monitor element configuration"""
    element: Literal["None", "FE", "C", "Si", "MN", "P", "S", "V", "CR"]
    value: constr(pattern=r'^[0-9]*\.?[0-9]+$') = Field(..., description="Monitor element value")
    option1: Literal["None", "FE", "C", "Si", "MN", "P", "S", "V", "CR"]
    option2: Literal["None", "FE", "C", "Si", "MN", "P", "S", "V", "CR"]


class LevelOutInformation(BaseModel):
    """Level out information configuration"""
    monitor_element: MonitorElement
    h_level_percent: List[constr(pattern=r'^[0-9]+$')] = Field(
        ..., 
        min_length=9, 
        max_length=9,
        description="High level percentages (9 values)"
    )
    l_level_percent: List[constr(pattern=r'^[0-9]+$')] = Field(
        ..., 
        min_length=9, 
        max_length=9,
        description="Low level percentages (9 values)"
    )


# ============================================================================
# Main analytical condition schemas
# ============================================================================

class AnalyticalConditionBase(BaseModel):
    """Base schema for analytical condition (used for creation)"""
    analytical_group: str = Field(..., description="Analytical group name", examples=["LAS 2023", "SS 2023"])
    analytical_method: Literal["integration Mode", "PDA + Integration"]
    seq: Seq
    level_out_information: LevelOutInformation


class AnalyticalConditionCreate(AnalyticalConditionBase):
    """Schema for creating a new analytical condition"""
    pass


class AnalyticalConditionResponse(AnalyticalConditionBase):
    """Schema for analytical condition response (includes DB fields)"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)


class AnalyticalConditionBulkCreate(BaseModel):
    """Schema for bulk creating analytical conditions"""
    records: List[AnalyticalConditionCreate] = Field(..., description="List of analytical conditions to create")


class AnalyticalConditionBulkResponse(BaseModel):
    """Schema for bulk operation response"""
    success: bool
    message: str
    count: int
    records: List[AnalyticalConditionResponse]


# ============================================================================
# Element Information Schemas
# ============================================================================

class Element(BaseModel):
    """Schema for individual element configuration"""
    ele_name: str = Field(..., description="Element name/symbol (e.g., Fe, C, Si)")
    analytical_range_min: constr(pattern=r'^[0-9]*\.?[0-9]+$') = Field(..., description="Minimum analytical range")
    analytical_range_max: constr(pattern=r'^[0-9]*\.?[0-9]+$') = Field(..., description="Maximum analytical range")
    asterisk: str = Field(..., description="Asterisk marker (typically '*' or empty)")
    chemic_ele: str = Field(..., description="Chemical element identifier")
    element: str = Field(..., description="Element display name")


class ElementInformationBase(BaseModel):
    """Base schema for element information"""
    analytical_group: str = Field(..., description="Analytical group name", examples=["LAS 2023", "SS 2023"])
    page: Literal["element_information"] = "element_information"
    ch_value: constr(pattern=r'^[0-9]+$') = Field(..., description="Channel value")
    elements: List[Element] = Field(..., description="Array of element configurations")


class ElementInformationCreate(ElementInformationBase):
    """Schema for creating element information"""
    pass


class ElementInformationResponse(ElementInformationBase):
    """Schema for element information response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ElementInformationBulkCreate(BaseModel):
    """Schema for bulk creating element information"""
    records: List[ElementInformationCreate] = Field(..., description="List of element information records")


class ElementInformationBulkResponse(BaseModel):
    """Schema for bulk element information response"""
    success: bool
    message: str
    count: int
    records: List[ElementInformationResponse]


# ============================================================================
# Channel Information Schemas
# ============================================================================

class Channel(BaseModel):
    """Schema for individual channel configuration"""
    ele_name: str = Field(..., description="Element name/symbol for this channel")
    w_lengh: constr(pattern=r'^[0-9]*\.?[0-9]*\+?[0-9]*$') = Field(..., description="Wavelength")
    seq: constr(pattern=r'^[0-9]+$') = Field(..., description="Sequence number (1, 2, or 3)")
    w_no: str = Field(..., description="Wave number (can be empty)")
    interval_element: str = Field(..., description="Interval reference element")
    interval_value: constr(pattern=r'^[0-9]*\.?[0-9]+$') = Field(..., description="Interval value")


class ChannelInformationBase(BaseModel):
    """Base schema for channel information"""
    analytical_group: str = Field(..., description="Analytical group name", examples=["LAS 2023", "SS 2023"])
    page: Literal["channel_information"] = "channel_information"
    channels: List[Channel] = Field(..., description="Array of channel configurations")


class ChannelInformationCreate(ChannelInformationBase):
    """Schema for creating channel information"""
    pass


class ChannelInformationResponse(ChannelInformationBase):
    """Schema for channel information response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChannelInformationBulkCreate(BaseModel):
    """Schema for bulk creating channel information"""
    records: List[ChannelInformationCreate] = Field(..., description="List of channel information records")


class ChannelInformationBulkResponse(BaseModel):
    """Schema for bulk channel information response"""
    success: bool
    message: str
    count: int
    records: List[ChannelInformationResponse]


# ============================================================================
# Attenuator Information Schemas
# ============================================================================

class AttenuatorRow(BaseModel):
    """Schema for individual attenuator row in left or right table"""
    element: str = Field(..., description="Element symbol (e.g., FE, C, SI)")
    ele_value: constr(pattern=r'^[0-9]*\.?[0-9]*\+?[0-9]*$') = Field(..., description="Element wavelength or value")
    att_value: constr(pattern=r'^[0-9]+$') = Field(..., description="Attenuator value")


class AttenuatorInformationBase(BaseModel):
    """Base schema for attenuator information"""
    analytical_group: str = Field(..., description="Analytical group name", examples=["LAS 2023", "SS 2023"])
    page: Literal["attenuator_information"] = "attenuator_information"
    left_table: List[AttenuatorRow] = Field(..., description="Left table attenuator data")
    right_table: List[AttenuatorRow] = Field(..., description="Right table attenuator data")


class AttenuatorInformationCreate(AttenuatorInformationBase):
    """Schema for creating attenuator information"""
    pass


class AttenuatorInformationResponse(AttenuatorInformationBase):
    """Schema for attenuator information response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttenuatorInformationBulkCreate(BaseModel):
    """Schema for bulk creating attenuator information"""
    records: List[AttenuatorInformationCreate] = Field(..., description="List of attenuator information records")


class AttenuatorInformationBulkResponse(BaseModel):
    """Schema for bulk attenuator information response"""
    success: bool
    message: str
    count: int
    records: List[AttenuatorInformationResponse]
