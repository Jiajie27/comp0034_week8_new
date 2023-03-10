import sys
from flask import render_template, current_app as app
from paralympic_app import db
from paralympic_app.models import Region, Event
from .schemas import RegionSchema, EventSchema

regions_schema = RegionSchema(many=True)
regions_schema = RegionSchema()
events_schema = EventSchema(many=True)
events_schema = EventSchema()

@app.route("/")
def index():
    """Creates a homepage for the paralympic app"""
    return render_template("index.html")

@app.get("/noc")
def noc():
    """Returns a list of NOC region codes and their details in JSON."""
    # Select all the regions using Flask-SQLAlchemy
    all_regions = db.session.execute(db.select(Region)).scalars()
    print(all_regions, file=sys.stderr)
    # Get the data using Marshmallow schema (returns JSON)
    result = regions_schema.dump(all_regions)
    # Return the data
    return result


@app.get("/event/<int:event_id>")
def event_id(event_id):
    """Returns the details for a specified event id"""
    event = db.session.execute(
        db.select(Event).filter_by(event_id=event_id)
    ).scalar_one_or_none()
    return events_schema.dump(event)