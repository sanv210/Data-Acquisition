from sqlalchemy import Column, Integer, String, JSON, DateTime, Index
from sqlalchemy.sql import func
from database import Base


class AnalyticalCondition(Base):
    """
    Model for storing analytical condition configurations.
    
    Stores the complete analytical condition schema including:
    - analytical_group: Group identifier
    - analytical_method: Integration Mode or PDA + Integration
    - seq: Nested object with purge, source, preburn, integ, clean sequences
    - level_out_information: Monitor element and level percentages
    """
    __tablename__ = "analytical_conditions"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core fields from the schema
    analytical_group = Column(String(100), nullable=False, index=True)
    analytical_method = Column(String(50), nullable=False)
    
    # Complex nested structures stored as JSON
    # seq contains: purge, source, preburn, integ, clean
    seq = Column(JSON, nullable=False)
    
    # level_out_information contains: monitor_element, h_level_percent, l_level_percent
    level_out_information = Column(JSON, nullable=False)
    
    # Timestamps for audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Composite index for common queries
    __table_args__ = (
        Index('idx_group_method', 'analytical_group', 'analytical_method'),
    )

    def __repr__(self):
        return f"<AnalyticalCondition(id={self.id}, group={self.analytical_group}, method={self.analytical_method})>"


class ElementInformation(Base):
    """
    Model for storing element information configurations.
    
    Stores element data including:
    - analytical_group: Group identifier
    - page: Page identifier (constant: "element_information")
    - ch_value: Channel value
    - elements: Array of element configurations with ranges and properties
    """
    __tablename__ = "element_information"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core fields from the schema
    analytical_group = Column(String(100), nullable=False, index=True)
    page = Column(String(50), nullable=False, default="element_information")
    ch_value = Column(String(10), nullable=False)
    
    # Array of element configurations stored as JSON
    elements = Column(JSON, nullable=False)
    
    # Timestamps for audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Index for common queries
    __table_args__ = (
        Index('idx_elem_group', 'analytical_group'),
    )

    def __repr__(self):
        return f"<ElementInformation(id={self.id}, group={self.analytical_group}, ch_value={self.ch_value})>"


class ChannelInformation(Base):
    """
    Model for storing channel information configurations.
    
    Stores channel data including:
    - analytical_group: Group identifier
    - page: Page identifier (constant: "channel_information")
    - channels: Array of channel configurations with wavelengths and intervals
    """
    __tablename__ = "channel_information"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core fields from the schema
    analytical_group = Column(String(100), nullable=False, index=True)
    page = Column(String(50), nullable=False, default="channel_information")
    
    # Array of channel configurations stored as JSON
    channels = Column(JSON, nullable=False)
    
    # Timestamps for audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Index for common queries
    __table_args__ = (
        Index('idx_chan_group', 'analytical_group'),
    )

    def __repr__(self):
        return f"<ChannelInformation(id={self.id}, group={self.analytical_group})>"


class AttenuatorInformation(Base):
    """
    Model for storing attenuator information configurations.
    
    Stores attenuator data including:
    - analytical_group: Group identifier
    - page: Page identifier (constant: "attenuator_information")
    - left_table: Array of attenuator data for left table
    - right_table: Array of attenuator data for right table
    """
    __tablename__ = "attenuator_information"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Core fields from the schema
    analytical_group = Column(String(100), nullable=False, index=True)
    page = Column(String(50), nullable=False, default="attenuator_information")
    
    # Left and right table data stored as JSON arrays
    left_table = Column(JSON, nullable=False)
    right_table = Column(JSON, nullable=False)
    
    # Timestamps for audit trail
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Index for common queries
    __table_args__ = (
        Index('idx_att_group', 'analytical_group'),
    )

    def __repr__(self):
        return f"<AttenuatorInformation(id={self.id}, group={self.analytical_group})>"
