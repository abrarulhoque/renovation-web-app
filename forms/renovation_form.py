from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SelectField,
    BooleanField,
    TextAreaField,
    DecimalField,
    FileField,
    RadioField,
    FormField,
    FieldList,
)
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange


class PersonalDetailsForm(FlaskForm):
    first_name = StringField("Förnamn / First Name", validators=[Optional()])
    last_name = StringField("Efternamn / Last Name", validators=[Optional()])
    phone = StringField("Telefonnummer / Phone Number", validators=[Optional()])
    email = StringField("E-post / Email", validators=[Optional(), Email()])
    address = StringField("Adress / Address", validators=[Optional()])
    door_code = StringField("Portkod / Door Code", validators=[Optional()])

    # Number of floors
    floor_count = IntegerField(
        "Antal våningar / Number of Floors",
        validators=[Optional(), NumberRange(min=1)],
    )

    # Dwelling type
    dwelling_type = RadioField(
        "Boende / Type of Dwelling",
        choices=[
            ("apartment", "Lägenhet / Apartment"),
            ("house", "Hus / House"),
            ("vacation_home", "Fritidshus / Vacation Home"),
            ("rental", "Hyresrätt / Rental Property"),
            ("commercial", "Lokal / Commercial Property"),
        ],
        validators=[Optional()],
    )

    # Season selection
    season = SelectField(
        "Säsong / Season",
        choices=[("summer", "Sommar / Summer"), ("winter", "Vinter / Winter")],
        validators=[Optional()],
    )

    # Parking and transportation
    parking_distance = SelectField(
        "Parkeringsmöjlighet (avstånd till fastighet) / Parking Availability",
        choices=[
            ("", "Välj... / Select..."),  # Optional: Add a placeholder
            ("bad", "Dålig / Bad"),
            ("ok", "Helt okej / Okay"),
            ("good", "Bra / Good"),
        ],
        validators=[Optional()],
    )
    transport_possibility = SelectField(
        "Transportmöjlighet fram till fastigheten / Transport Possibility",
        choices=[("good", "Bra / Good"), ("poor", "Dålig / Poor")],
        validators=[Optional()],
    )
    parking_fee = DecimalField(
        "Parkeringskostnad / Parking Fee", validators=[Optional()]
    )
    service_car_price = DecimalField(
        "Service bil kostnad / Service Car Cost", validators=[Optional()]
    )
    service_car_days = IntegerField(
        "Service bil antal dagar / Service Car Days",
        validators=[Optional(), NumberRange(min=0)],
    )
    congestion_charge = DecimalField(
        "Trängselskatt / Congestion Charge", validators=[Optional()]
    )
    construction_bag = BooleanField("Byggsäck / Construction Bag")

    # Building access
    has_elevator = SelectField(
        "Hiss / Elevator",
        choices=[
            ("no", "Nej / No"),
            ("small", "Ja, Liten / Yes, Small"),
            ("medium", "Ja, Mellan / Yes, Medium"),
            ("large", "Ja, Stor / Yes, Large"),
        ],
        validators=[Optional()],
    )
    elevator_size = SelectField(
        "Storlek på hiss / Elevator Size",
        choices=[
            ("small", "Liten / Small"),
            ("medium", "Mellan / Medium"),
            ("large", "Stor / Large"),
        ],
        validators=[Optional()],
    )
    good_stairwell_access = BooleanField(
        "Trapphus med god tillgänglighet / Good Stairwell Access"
    )
    indoor_workspace = BooleanField(
        "Möjlighet till arbetsutrymme inomhus / Indoor Workspace Available"
    )
    workspace_distance = DecimalField(
        "Distans till arbetsutrymme / Distance to Workspace (m)",
        validators=[Optional()],
    )
    entrance_distance = DecimalField(
        "Avstånd till ingång / Distance to Entrance (m)", validators=[Optional()]
    )
    floor_protection = IntegerField(
        "Golvskydd / Floor Protection", validators=[Optional()]
    )


class BathroomDetailsForm(FlaskForm):
    # Bathroom dimensions
    width = DecimalField("Bredd / Width (cm)", validators=[Optional()])
    length = DecimalField("Längd / Length (cm)", validators=[Optional()])
    height = DecimalField("Höjd / Height (cm)", validators=[Optional()])
    floor_area = DecimalField("Golvyta / Floor Area (m²)", validators=[Optional()])

    # Drawings and plans
    has_sketch = BooleanField("Skiss på badrummet / Bathroom Sketch Available")
    sketch_file = FileField("Upload Sketch")
    sketch_files = FieldList(FileField("Upload Additional Sketches"), min_entries=1)
    existing_placements = BooleanField("Befintliga placeringar / Existing Placements")

    # Relocations
    relocation_count = SelectField(
        "Antal omplaceringar / Number of Relocations",
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ],
        validators=[Optional()],
    )
    toilet_relocation = IntegerField(
        "Omplacering av toalett / Toilet Relocation (cm)", validators=[Optional()]
    )
    sink_relocation = IntegerField(
        "Omplacering av tvättställ / Sink Relocation (cm)", validators=[Optional()]
    )
    shower_relocation = IntegerField(
        "Omplacering av dusch / Shower Relocation (cm)", validators=[Optional()]
    )
    bathtub_relocation = IntegerField(
        "Omplacering av badkar / Bathtub Relocation (cm)", validators=[Optional()]
    )
    towel_warmer_relocation = IntegerField(
        "Omplacering av handdukstork / Towel Warmer Relocation (cm)",
        validators=[Optional()],
    )

    # Floor drains
    floor_drain_replacements = IntegerField(
        "Antal byte av golvbrunnar / Floor Drain Replacements", validators=[Optional()]
    )
    floor_drain_relocation = SelectField(
        "Flytt av golvbrunnar / Floor Drain Relocation",
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ],
        validators=[Optional()],
    )
    extra_floor_drain = BooleanField("Utföra en extra golvbrunn / Extra Floor Drain")

    # Construction details
    cut_channels = BooleanField("Spåra golv och väggar / Cut Channels")
    floor_penetrations = SelectField(
        "Andra genomföringar från golvet / Floor Penetrations",
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ],
        validators=[Optional()],
    )
    wall_penetrations = SelectField(
        "Addera genomföringar till väggar / Wall Penetrations",
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ],
        validators=[Optional()],
    )
    move_drain_pipes = BooleanField("Flytt av avloppsrör i golvet / Move Drain Pipes")

    # Utilities
    water_shutoff_location = StringField(
        "Avstängning av vatten finns / Water Shutoff Location", validators=[Optional()]
    )
    fuse_box_type = StringField("Säkringsskåp / Fuse Box Type", validators=[Optional()])
    has_gfci = BooleanField("Jordfelsbrytare / Ground Fault Circuit Interrupter")
    fuse_box_distance = DecimalField(
        "Avstånd till elskåp / Distance to Fuse Box (m)", validators=[Optional()]
    )
    junction_box_distance = DecimalField(
        "Avstånd till kopplingsdosa / Distance to Junction Box (m)",
        validators=[Optional()],
    )


class AppliancesForm(FlaskForm):
    ceiling_lamp = BooleanField("Taklampa/takdosa / Ceiling Lamp")
    wall_socket = BooleanField("Vägguttag / Wall Socket")
    electric_towel_warmer = BooleanField("El handdukstork / Electric Towel Warmer")
    floor_heating = BooleanField("El-golvvärme / Electric Floor Heating")
    washing_machine = BooleanField("Tvättmaskin / Washing Machine")
    dryer = BooleanField("Torktumlare / Tumble Dryer")
    sink_outlet = BooleanField("El i tvättställ/kommod / Sink Cabinet Outlet")
    iron_outlet = BooleanField("Extra uttag för strykjärn / Iron Outlet")
    spotlights_count = IntegerField(
        "Spotlights (antal) / Spotlights (quantity)", validators=[Optional()]
    )
    spotlights_price_per_unit = DecimalField(
        "Pris per spotlight / Price per Spotlight", validators=[Optional()]
    )
    ceiling_lowering = BooleanField("Taksänkning / Ceiling Lowering")

    # Additional fields from rows 28-49
    # good_stairwell = BooleanField( # Removed duplicate
    #     "Trapphus med god tillgänglighet / Staircase with good accessibility"
    # )
    etablering = BooleanField("Etablering / Establishment")
    flytspackling = BooleanField("Flytspackling / Floor leveling compound")
    bring_in_materials = BooleanField(
        "Ta in byggmaterial / Bring in Building Materials"
    )
    workspace_distance_if_no = DecimalField(
        "Distans till närmaste arbetsutrymme om nej / Distance to the nearest workspace if no",
        validators=[Optional()],
    )
    workspace_distance_from_entry = DecimalField(
        "Avstånd till arbetsutrymme från närmaste ingång / Distance to workspace from nearest entry",
        validators=[Optional()],
    )
    floor_covering_time = IntegerField(
        "Arbetstid för golvbeläggning / Working time for floor covering",
        validators=[Optional()],
    )
    floor_covering_material = StringField(
        "Materialkrav för golvbeläggning / Material requirements for floor covering",
        validators=[Optional()],
    )
    floor_drain_count = IntegerField(
        "Antal golvbrunnsbyten / Number of floor drain replacements",
        validators=[Optional()],
    )
    floor_drain_relocation = SelectField(
        "Flytt av golvbrunnar / Relocation of floor drains",
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ],
        validators=[Optional()],
    )
    additional_floor_drain = BooleanField(
        "Installera en extra golvbrunn / Install an additional floor drain"
    )
    marking_floors_walls = BooleanField(
        "Markering av golv och väggar / Marking floors and walls"
    )
    floor_penetrations = SelectField(
        "Andra genomföringar från golvet / Other penetrations from the floor",
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ],
        validators=[Optional()],
    )
    wall_penetrations_relocation = SelectField(
        "Flytt av genomföringar till väggar / Relocation of penetrations to walls",
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
        ],
        validators=[Optional()],
    )
    drain_pipes_replacement = BooleanField(
        "Byte av avloppsrör i golvet / Replacement of drain pipes in the floor"
    )
    water_shutoff = SelectField(
        "Vattenavstängning finns / Water shut-off is available",
        choices=[
            ("bathroom", "I badrummet / In the bathroom"),
            ("outside", "Utanför badrummet / Outside of the bathroom"),
            ("villa_basement", "Villan källare / Villa basement"),
            (
                "association_basement",
                "Föreningens källare / The association's basement",
            ),
        ],
        validators=[Optional()],
    )
    fuse_box = SelectField(
        "Säkringsskåp / Fuse box",
        choices=[
            ("old", "Gamla säkringar / Old fuses"),
            ("modern", "Moderna säkringar / Modern fuses"),
            ("none", "Finns inte / Doesn't exist"),
        ],
        validators=[Optional()],
    )
    rcd = BooleanField("Jordfelsbrytare / Residual current device (RCD)")
    fusebox_distance = SelectField(
        "Avstånd från säkringsskåp till badrum / Distance from fusebox to bathroom",
        choices=[
            ("up_to_5m", "Upp till fem meter / Up to five meters"),
            ("up_to_10m", "Upp till tio meter / Up to ten meters"),
            ("another_floor", "Annan våning / Another floor"),
        ],
        validators=[Optional()],
    )
    junction_box_distance = SelectField(
        "Avståndet mellan närmaste kopplingsdosa till badrummet / Distance from Nearest Junction Box to Bathroom",
        choices=[
            ("", "Välj... / Select..."),  # Optional: Add a placeholder
            ("close", "I närliggande vägg / In Nearby Wall"),
            ("far", "Långt bort / Far Away"),
        ],
        validators=[Optional()],
    )


class InteriorFittingsForm(FlaskForm):
    built_in_mirror = BooleanField("Inbyggd spegel i väggen / Built-in Mirror")
    mirror_lighting = BooleanField("Spegel med belysning / Mirror with Lighting")
    mirror_cabinet = BooleanField(
        "Spegelskåp med belysning och uttag / Mirror Cabinet with Lighting"
    )
    vanity_unit = BooleanField("Tvättställ med kommod / Sink with Vanity")
    shower_mixer = BooleanField("Duschblandare med handdusch / Shower Mixer")
    shower_corner = BooleanField("Duschhörna med tak- och handdusch / Shower Corner")
    shower_wall = BooleanField("Sätta upp en vägg som duschvägg / Shower Wall")
    glass_block_wall = BooleanField(
        "Sätta upp en fast duschvägg av glasblock / Glass Block Wall"
    )
    glass_shower_wall = BooleanField(
        "Montering av en glas-duschvägg / Glass Shower Wall"
    )
    shower_doors = BooleanField("Montering av duschdörrar / Shower Doors")

    # Add drain type from row 73
    shower_drain = SelectField(
        "Golvbrunn i dusch / Floordrain in shower",
        choices=[
            ("normal", "Normal / Normal"),
            ("elongated", "Avlång / Elongated"),
        ],
        validators=[Optional()],
    )

    # Bathtub options - converted to individual toggle buttons
    # bathtub_normal = BooleanField("Badkar normal / Bathtub normal") # Removed
    # bathtub_long = BooleanField("Badkar avlång / Bathtub long") # Removed
    bathtub_freestanding = BooleanField("Badkar fristående / Bathtub freestanding")
    bathtub_built_in = BooleanField("Badkar inbyggt / Bathtub built-in")
    # bathtub_wall = BooleanField("Badkar vägg / Bathtub wall-mounted") # Removed

    # Toilet options - converted to individual toggle buttons
    toilet_freestanding = BooleanField("Toalett fristående / Toilet freestanding")
    toilet_wall_mounted = BooleanField("Toalett väggmonterad / Toilet wall-mounted")

    # Add rows 76-92
    silicon_application = BooleanField("Silikondragning / Silicon application")
    interior_door_casing = BooleanField(
        "Byte av dörrfoder invändigt / Replacement of interior door casing"
    )
    exterior_door_casing = BooleanField(
        "Byte av dörrfoder utvändigt / Replacement of exteriour door casing"
    )
    doorframe_replacement = BooleanField("Byte av dörrkarm / Replacement of doorframe")
    door_replacement = BooleanField("Byte av dörrblad / Replacement of door")
    threshold_replacement = BooleanField(
        "Byte/uppfräschning av tröskel / Replacement and refurbishment of the threshold"
    )
    window_repainting = BooleanField("Fönster ommålning / Window repainting")
    hidden_pipelines = BooleanField("Dolda rördragningar / Hidden pipelines")
    shown_pipelines = BooleanField("Utanpåliggande rördragningar / Shown pipelines")
    hidden_ceiling_shower = BooleanField("Dold takdusch / Hidden ceilingshower")
    save_waterheated_floor = BooleanField(
        "Räddning av befintlig vattenburen golvvärme / Saving of present waterheated floor"
    )
    new_waterheated_floor = BooleanField(
        "Läggning av ny vattenburen golvvärme / Installation of new waterheated floor"
    )
    dismantling_cleaning = BooleanField(
        "Avetablering och grovstädning / Dismantling and rough cleaning"
    )
    wall_tiling_height = IntegerField(
        "Höjd på plattsättning på väggarna / Height of tiling on the walls (cm)",
        validators=[Optional()],
    )
    concealed_mixers_count = IntegerField(
        "Antal dolda blandare / Number of concealed mixers", validators=[Optional()]
    )
    concealed_mixers_price = DecimalField(
        "Pris per enhet / Price per unit", validators=[Optional()]
    )
    niches_count = IntegerField(
        "Antal nischer / Number of niches", validators=[Optional()]
    )
    niches_price = DecimalField(
        "Pris per enhet / Price per unit", validators=[Optional()]
    )


class TilesAndPaintingForm(FlaskForm):
    floor_tile_size = StringField(
        "Storlek golvplattor / Floor Tile Size", validators=[Optional()]
    )
    floor_tile_deviation = StringField(
        "Avvikelse i storlek för golvplattor / Floor Tile Size Deviation",
        validators=[Optional()],
    )
    wall_tile_size = StringField(
        "Väggplattor / Wall Tile Size", validators=[Optional()]
    )
    wall_tile_deviation = StringField(
        "Avvikelse i storlek för väggplattor / Wall Tile Size Deviation",
        validators=[Optional()],
    )
    grout_colors = IntegerField(
        "Antal färger fog / Number of Grout Colors", validators=[Optional()]
    )
    grout_colors_price = DecimalField(
        "Pris per enhet / Price per unit", validators=[Optional()]
    )
    ceiling_painting_hours = DecimalField(
        "Arbetstid målning av tak / Ceiling Painting Hours", validators=[Optional()]
    )
    ceiling_painting_price = DecimalField(
        "Pris per timme / Price per hour", validators=[Optional()]
    )
    paint_ceiling = BooleanField("Målning av tak / Paint Ceiling")
    ceiling_area = DecimalField("Antal kvm / Area in sqm", validators=[Optional()])
    ceiling_area_price = DecimalField(
        "Pris per enhet / Price per unit", validators=[Optional()]
    )
    wall_painting_hours = DecimalField(
        "Arbetstid målning av okaklade väggar / Wall Painting Hours",
        validators=[Optional()],
    )
    wall_painting_price = DecimalField(
        "Pris per timme / Price per hour", validators=[Optional()]
    )
    paint_walls = BooleanField("Målning av okaklade väggar / Paint Walls")
    wall_area = DecimalField("Antal kvm / Area in sqm", validators=[Optional()])
    wall_area_price = DecimalField(
        "Pris per enhet / Price per unit", validators=[Optional()]
    )
    cleanup = BooleanField("Avetablering och grovstädning / Post construction cleaning")
    construction_bag = IntegerField(
        "Byggsäck / Construction Bag (Antal säckar)", validators=[Optional()]
    )
    season = SelectField(
        "Säsong / Season",
        choices=[
            ("summer", "Sommar / Summer"),
            ("winter", "Vinter / Winter"),
        ],
        validators=[Optional()],
    )
    project_notes = TextAreaField(
        "Projektanteckningar / Project Notes", validators=[Optional()]
    )


class ExtraItemForm(FlaskForm):
    item = StringField("Artikel / Item", validators=[Optional()])
    cost = DecimalField("Kostnad / Cost (SEK)", validators=[Optional()])


class AdditionalNotesForm(FlaskForm):
    extra_items = FieldList(FormField(ExtraItemForm), min_entries=1)
    notes = TextAreaField(
        "Noteringar för diverse arbete / Additional Notes", validators=[Optional()]
    )
    output_format = SelectField(
        "Utdataformat / Output Format",
        choices=[
            ("quotation", "Offert / Quotation"),
            ("workorder", "Arbetsorder / Work Order"),
        ],
        validators=[Optional()],
    )


class RenovationForm(FlaskForm):
    personal_details = FormField(PersonalDetailsForm)
    bathroom_details = FormField(BathroomDetailsForm)
    appliances = FormField(AppliancesForm)
    interior_fittings = FormField(InteriorFittingsForm)
    tiles_and_painting = FormField(TilesAndPaintingForm)
    additional_notes = FormField(AdditionalNotesForm)

    # Add a method to set default values for required fields
    def set_defaults(self):
        """Set default values for required fields to ensure validation passes"""
        # Personal details defaults
        if not self.personal_details.first_name.data:
            self.personal_details.first_name.data = "Default"
        if not self.personal_details.last_name.data:
            self.personal_details.last_name.data = "User"
        if not self.personal_details.email.data:
            self.personal_details.email.data = "default@example.com"
        if not self.personal_details.phone.data:
            self.personal_details.phone.data = "1234567890"
        if not self.personal_details.address.data:
            self.personal_details.address.data = "Default Address"
        if not self.personal_details.service_car_price.data:
            self.personal_details.service_car_price.data = 0
        if not self.personal_details.service_car_days.data:
            self.personal_details.service_car_days.data = 0

        # Bathroom details defaults
        if not self.bathroom_details.width.data:
            self.bathroom_details.width.data = 200
        if not self.bathroom_details.length.data:
            self.bathroom_details.length.data = 200
        if not self.bathroom_details.height.data:
            self.bathroom_details.height.data = 240
        if not self.bathroom_details.floor_area.data:
            self.bathroom_details.floor_area.data = 4.0
        if not self.bathroom_details.relocation_count.data:
            self.bathroom_details.relocation_count.data = "0"
