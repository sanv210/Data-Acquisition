
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal, engine, Base
from models import (
    AnalyticalCondition,
    ElementInformation,
    ChannelInformation,
    AttenuatorInformation,
)
from schemas import (
    AnalyticalConditionCreate,
    AnalyticalConditionResponse,
    AnalyticalConditionBulkCreate,
    AnalyticalConditionBulkResponse,
    ElementInformationCreate,
    ElementInformationResponse,
    ElementInformationBulkCreate,
    ElementInformationBulkResponse,
    ChannelInformationCreate,
    ChannelInformationResponse,
    ChannelInformationBulkCreate,
    ChannelInformationBulkResponse,
    AttenuatorInformationCreate,
    AttenuatorInformationResponse,
    AttenuatorInformationBulkCreate,
    AttenuatorInformationBulkResponse,
)

app = FastAPI(
    title="DAQ API",
    description="Data Acquisition Backend API for analytical conditions, elements, attenuators, and channels",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
	"""Create any database tables defined via SQLAlchemy Base subclasses.

	This ensures the DB (created earlier in database.py) has any tables
	needed by the app. For now there are no model classes, so this is
	a safe no-op but useful for future extensions.
	"""
	Base.metadata.create_all(bind=engine)


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.get("/")
def read_root():
	return {"message": "DAQ API running"}


@app.get("/db")
def read_database_name(db: Session = Depends(get_db)):
    """Return the current database name the connection is using.

    This runs a simple SELECT DATABASE() query to verify connectivity
    and show the active DB name (useful to confirm the DB named
    "DAQ project" is in use).
    """
    res = db.execute(text("SELECT DATABASE()"))
    db_name = res.scalar()
    return {"database": db_name}


# ============================================================================
# Analytical Condition Endpoints
# ============================================================================

@app.post("/api/analytical-conditions/bulk", response_model=AnalyticalConditionBulkResponse)
def bulk_create_analytical_conditions(
    bulk_data: AnalyticalConditionBulkCreate,
    db: Session = Depends(get_db)
):
    """
    Bulk create analytical condition records.
    
    Accepts a list of analytical condition objects matching the schema and
    inserts them into the database in a single transaction.
    
    Returns the created records with their assigned IDs and timestamps.
    """
    try:
        created_records = []
        
        for record_data in bulk_data.records:
            # Convert Pydantic model to dict for JSON fields
            db_record = AnalyticalCondition(
                analytical_group=record_data.analytical_group,
                analytical_method=record_data.analytical_method,
                seq=record_data.seq.model_dump(),  # Pydantic v2
                level_out_information=record_data.level_out_information.model_dump(),
            )
            db.add(db_record)
            created_records.append(db_record)
        
        # Commit all records at once
        db.commit()
        
        # Refresh to get IDs and timestamps
        for record in created_records:
            db.refresh(record)
        
        return AnalyticalConditionBulkResponse(
            success=True,
            message=f"Successfully created {len(created_records)} analytical condition(s)",
            count=len(created_records),
            records=[AnalyticalConditionResponse.model_validate(r) for r in created_records]
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating records: {str(e)}")


@app.get("/api/analytical-conditions/bulk", response_model=AnalyticalConditionBulkResponse)
def bulk_read_analytical_conditions(
    analytical_group: Optional[str] = None,
    analytical_method: Optional[str] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Bulk read analytical condition records.
    
    Retrieves all analytical condition records from the database.
    Supports optional filtering by analytical_group and analytical_method.
    
    Query Parameters:
    - analytical_group: Filter by analytical group name (e.g., "LAS 2023")
    - analytical_method: Filter by analytical method (e.g., "integration Mode")
    - limit: Maximum number of records to return
    
    Returns all matching records in the same JSON schema format.
    """
    try:
        query = db.query(AnalyticalCondition)
        
        # Apply filters if provided
        if analytical_group:
            query = query.filter(AnalyticalCondition.analytical_group == analytical_group)
        if analytical_method:
            query = query.filter(AnalyticalCondition.analytical_method == analytical_method)
        
        # Apply limit if provided
        if limit:
            query = query.limit(limit)
        
        # Order by most recent first
        query = query.order_by(AnalyticalCondition.created_at.desc())
        
        records = query.all()
        
        return AnalyticalConditionBulkResponse(
            success=True,
            message=f"Retrieved {len(records)} analytical condition(s)",
            count=len(records),
            records=[AnalyticalConditionResponse.model_validate(r) for r in records]
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading records: {str(e)}")


@app.get("/api/analytical-conditions/{record_id}", response_model=AnalyticalConditionResponse)
def get_analytical_condition_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single analytical condition record by ID.
    
    Returns the complete record including all nested data.
    """
    record = db.query(AnalyticalCondition).filter(AnalyticalCondition.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Analytical condition with ID {record_id} not found")
    
    return AnalyticalConditionResponse.model_validate(record)


@app.delete("/api/analytical-conditions/{record_id}")
def delete_analytical_condition(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a single analytical condition record by ID.
    """
    record = db.query(AnalyticalCondition).filter(AnalyticalCondition.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Analytical condition with ID {record_id} not found")
    
    db.delete(record)
    db.commit()
    
    return {"success": True, "message": f"Deleted analytical condition with ID {record_id}"}


# ============================================================================
# Element Information Endpoints
# ============================================================================

@app.post("/api/element-information/bulk", response_model=ElementInformationBulkResponse)
def bulk_create_element_information(
    bulk_data: ElementInformationBulkCreate,
    db: Session = Depends(get_db)
):
    """
    Bulk create element information records.
    
    Accepts a list of element information objects and inserts them into the database.
    Returns the created records with their assigned IDs and timestamps.
    """
    try:
        created_records = []
        
        for record_data in bulk_data.records:
            db_record = ElementInformation(
                analytical_group=record_data.analytical_group,
                page=record_data.page,
                ch_value=record_data.ch_value,
                elements=[elem.model_dump() for elem in record_data.elements],
            )
            db.add(db_record)
            created_records.append(db_record)
        
        db.commit()
        
        for record in created_records:
            db.refresh(record)
        
        return ElementInformationBulkResponse(
            success=True,
            message=f"Successfully created {len(created_records)} element information record(s)",
            count=len(created_records),
            records=[ElementInformationResponse.model_validate(r) for r in created_records]
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating records: {str(e)}")


@app.get("/api/element-information/bulk", response_model=ElementInformationBulkResponse)
def bulk_read_element_information(
    analytical_group: Optional[str] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Bulk read element information records.
    
    Retrieves all element information records from the database.
    Supports optional filtering by analytical_group.
    """
    try:
        query = db.query(ElementInformation)
        
        if analytical_group:
            query = query.filter(ElementInformation.analytical_group == analytical_group)
        
        if limit:
            query = query.limit(limit)
        
        query = query.order_by(ElementInformation.created_at.desc())
        records = query.all()
        
        return ElementInformationBulkResponse(
            success=True,
            message=f"Retrieved {len(records)} element information record(s)",
            count=len(records),
            records=[ElementInformationResponse.model_validate(r) for r in records]
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading records: {str(e)}")


@app.get("/api/element-information/{record_id}", response_model=ElementInformationResponse)
def get_element_information_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single element information record by ID.
    
    Returns the complete record including all element configurations.
    """
    record = db.query(ElementInformation).filter(ElementInformation.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Element information with ID {record_id} not found")
    
    return ElementInformationResponse.model_validate(record)


# ============================================================================
# Channel Information Endpoints
# ============================================================================

@app.post("/api/channel-information/bulk", response_model=ChannelInformationBulkResponse)
def bulk_create_channel_information(
    bulk_data: ChannelInformationBulkCreate,
    db: Session = Depends(get_db)
):
    """
    Bulk create channel information records.
    
    Accepts a list of channel information objects and inserts them into the database.
    Returns the created records with their assigned IDs and timestamps.
    """
    try:
        created_records = []
        
        for record_data in bulk_data.records:
            db_record = ChannelInformation(
                analytical_group=record_data.analytical_group,
                page=record_data.page,
                channels=[chan.model_dump() for chan in record_data.channels],
            )
            db.add(db_record)
            created_records.append(db_record)
        
        db.commit()
        
        for record in created_records:
            db.refresh(record)
        
        return ChannelInformationBulkResponse(
            success=True,
            message=f"Successfully created {len(created_records)} channel information record(s)",
            count=len(created_records),
            records=[ChannelInformationResponse.model_validate(r) for r in created_records]
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating records: {str(e)}")


@app.get("/api/channel-information/bulk", response_model=ChannelInformationBulkResponse)
def bulk_read_channel_information(
    analytical_group: Optional[str] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Bulk read channel information records.
    
    Retrieves all channel information records from the database.
    Supports optional filtering by analytical_group.
    """
    try:
        query = db.query(ChannelInformation)
        
        if analytical_group:
            query = query.filter(ChannelInformation.analytical_group == analytical_group)
        
        if limit:
            query = query.limit(limit)
        
        query = query.order_by(ChannelInformation.created_at.desc())
        records = query.all()
        
        return ChannelInformationBulkResponse(
            success=True,
            message=f"Retrieved {len(records)} channel information record(s)",
            count=len(records),
            records=[ChannelInformationResponse.model_validate(r) for r in records]
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading records: {str(e)}")


@app.get("/api/channel-information/{record_id}", response_model=ChannelInformationResponse)
def get_channel_information_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single channel information record by ID.
    
    Returns the complete record including all channel configurations.
    """
    record = db.query(ChannelInformation).filter(ChannelInformation.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Channel information with ID {record_id} not found")
    
    return ChannelInformationResponse.model_validate(record)


# ============================================================================
# Attenuator Information Endpoints
# ============================================================================

@app.post("/api/attenuator-information/bulk", response_model=AttenuatorInformationBulkResponse)
def bulk_create_attenuator_information(
    bulk_data: AttenuatorInformationBulkCreate,
    db: Session = Depends(get_db)
):
    """
    Bulk create attenuator information records.
    
    Accepts a list of attenuator information objects and inserts them into the database.
    Returns the created records with their assigned IDs and timestamps.
    """
    try:
        created_records = []
        
        for record_data in bulk_data.records:
            db_record = AttenuatorInformation(
                analytical_group=record_data.analytical_group,
                page=record_data.page,
                left_table=[row.model_dump() for row in record_data.left_table],
                right_table=[row.model_dump() for row in record_data.right_table],
            )
            db.add(db_record)
            created_records.append(db_record)
        
        db.commit()
        
        for record in created_records:
            db.refresh(record)
        
        return AttenuatorInformationBulkResponse(
            success=True,
            message=f"Successfully created {len(created_records)} attenuator information record(s)",
            count=len(created_records),
            records=[AttenuatorInformationResponse.model_validate(r) for r in created_records]
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating records: {str(e)}")


@app.get("/api/attenuator-information/bulk", response_model=AttenuatorInformationBulkResponse)
def bulk_read_attenuator_information(
    analytical_group: Optional[str] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Bulk read attenuator information records.
    
    Retrieves all attenuator information records from the database.
    Supports optional filtering by analytical_group.
    """
    try:
        query = db.query(AttenuatorInformation)
        
        if analytical_group:
            query = query.filter(AttenuatorInformation.analytical_group == analytical_group)
        
        if limit:
            query = query.limit(limit)
        
        query = query.order_by(AttenuatorInformation.created_at.desc())
        records = query.all()
        
        return AttenuatorInformationBulkResponse(
            success=True,
            message=f"Retrieved {len(records)} attenuator information record(s)",
            count=len(records),
            records=[AttenuatorInformationResponse.model_validate(r) for r in records]
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading records: {str(e)}")


@app.get("/api/attenuator-information/{record_id}", response_model=AttenuatorInformationResponse)
def get_attenuator_information_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a single attenuator information record by ID.
    
    Returns the complete record including both left_table and right_table data.
    """
    record = db.query(AttenuatorInformation).filter(AttenuatorInformation.id == record_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail=f"Attenuator information with ID {record_id} not found")
    
    return AttenuatorInformationResponse.model_validate(record)


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

