def calculate_extra_items_cost(form):
    """Calculate additional costs from extra items."""
    labor_cost = 0
    material_cost = 0
    other_cost = 0

    # Process extra items
    if (
        hasattr(form.additional_notes, "extra_items")
        and form.additional_notes.extra_items.data
    ):
        for item_data in form.additional_notes.extra_items.data:
            if (
                isinstance(item_data, dict)
                and "item" in item_data
                and "cost" in item_data
            ):
                item_name = item_data["item"].lower() if item_data["item"] else ""
                cost = float(item_data["cost"] or 0)

                # Categorize items based on keywords in their names
                if item_name and cost > 0:
                    # Labor related keywords
                    labor_keywords = [
                        "arbete",
                        "labor",
                        "montering",
                        "installation",
                        "service",
                    ]
                    # Material related keywords
                    material_keywords = [
                        "material",
                        "utrustning",
                        "equipment",
                        "supplies",
                        "parts",
                    ]
                    # Other/waste related keywords
                    other_keywords = [
                        "avfall",
                        "waste",
                        "transport",
                        "frakt",
                        "freight",
                        "avgift",
                        "fee",
                    ]

                    # Categorize cost based on item name
                    if any(keyword in item_name for keyword in labor_keywords):
                        labor_cost += cost
                    elif any(keyword in item_name for keyword in material_keywords):
                        material_cost += cost
                    elif any(keyword in item_name for keyword in other_keywords):
                        other_cost += cost
                    else:
                        # Default to material cost if no category is detected
                        material_cost += cost

    return labor_cost, material_cost, other_cost


def calculate_labor_cost(form):
    """Calculate the labor cost for the main option."""
    # Season cost - Fix field name inconsistency, should be using form.personal_details.season
    season_cost = 3000 if form.personal_details.season.data == "winter" else 0

    # General conditions costs
    floor_count = form.personal_details.floor_count.data or 0
    general_costs = floor_count * 100

    # Dwelling type - Add 'commercial' type as per pricing rules
    if form.personal_details.dwelling_type.data in [
        "apartment",
        "rental",
        "commercial",
    ]:
        general_costs += 2000

    # Cost for bringing in materials
    if hasattr(form, "appliances") and form.appliances.bring_in_materials.data:
        general_costs += 500  # Example cost

    # Accessibility costs
    accessibility_labor = 0

    # Parking and transport
    if form.personal_details.parking_distance.data == "bad":
        accessibility_labor += 1000
    elif form.personal_details.parking_distance.data == "ok":
        accessibility_labor += 500  # Example cost for 'ok'
    # No cost for 'good'

    # Fix transport_possibility - 0 for 'good' instead of 500
    if form.personal_details.transport_possibility.data == "poor":
        accessibility_labor += 2000
    elif form.personal_details.transport_possibility.data == "ok":
        accessibility_labor += 500
    # No additional cost for 'good'

    # Elevator
    if form.personal_details.has_elevator.data == "no":
        accessibility_labor += 2000

    # Elevator size
    if form.personal_details.elevator_size.data == "small":
        accessibility_labor += 2000
    elif form.personal_details.elevator_size.data == "medium":
        accessibility_labor += 500

    # Stairwell access
    if not form.personal_details.good_stairwell_access.data:
        accessibility_labor += 2000

    # Indoor workspace
    if not form.personal_details.indoor_workspace.data:
        accessibility_labor += 2000

        # Distance calculations - Fix field name inconsistency
        workspace_distance = float(form.personal_details.workspace_distance.data or 0)
        accessibility_labor += workspace_distance * 480

    # Entrance distance
    entrance_distance = float(form.personal_details.entrance_distance.data or 0)
    accessibility_labor += entrance_distance * 480

    # Floor protection - Fix field name inconsistency to use appliances.floor_covering_time
    protection_labor = 0
    hours = int(form.appliances.floor_covering_time.data or 0)
    protection_labor += hours * 680

    # Bathroom dimensions
    width = float(form.bathroom_details.width.data or 0)
    length = float(form.bathroom_details.length.data or 0)
    height = float(form.bathroom_details.height.data or 0)

    dimension_labor = 40000 + (width * 160) + (length * 160) + (height * 160)

    # Layout modifications
    layout_labor = 0

    # Sketch provided
    if form.bathroom_details.has_sketch.data:
        layout_labor += 500  # Assuming a fixed value

    # Relocations
    relocations = int(form.bathroom_details.relocation_count.data or 0)
    if relocations == 1:
        layout_labor += 3000
    elif relocations == 2:
        layout_labor += 6000
    elif relocations == 3:
        layout_labor += 8000

    # Specific fixture relocations
    if (
        form.bathroom_details.toilet_relocation.data
        and int(form.bathroom_details.toilet_relocation.data) > 0
    ):
        layout_labor += 1000
    if (
        form.bathroom_details.sink_relocation.data
        and int(form.bathroom_details.sink_relocation.data) > 0
    ):
        layout_labor += 1000
    if (
        form.bathroom_details.shower_relocation.data
        and int(form.bathroom_details.shower_relocation.data) > 0
    ):
        layout_labor += 1000
    if (
        form.bathroom_details.bathtub_relocation.data
        and int(form.bathroom_details.bathtub_relocation.data) > 0
    ):
        layout_labor += 1000
    if (
        form.bathroom_details.towel_warmer_relocation.data
        and int(form.bathroom_details.towel_warmer_relocation.data) > 0
    ):
        layout_labor += 1000

    # Add plumbing costs (previously missing)
    plumbing_labor = calculate_plumbing_labor_cost(form)

    # Add electrical costs (previously missing)
    electrical_labor = calculate_electrical_labor_cost(form)

    # Add fixtures costs (previously missing)
    fixtures_labor = calculate_fixtures_labor_cost(form)

    # Add tiling and painting costs (previously missing)
    tiling_labor = calculate_tiling_labor_cost(form)

    # Add extra items labor cost
    extra_labor, _, _ = calculate_extra_items_cost(form)

    # Sum up all labor costs
    total_labor = (
        season_cost
        + general_costs
        + accessibility_labor
        + protection_labor
        + dimension_labor
        + layout_labor
        + plumbing_labor
        + electrical_labor
        + fixtures_labor
        + tiling_labor
        + extra_labor
    )

    # Apply discount
    labor_after_discount = total_labor - 1000

    return labor_after_discount


def calculate_material_cost(form):
    """Calculate the material cost for the main option."""
    # Base material cost calculation
    width = float(form.bathroom_details.width.data or 0)
    length = float(form.bathroom_details.length.data or 0)
    height = float(form.bathroom_details.height.data or 0)

    basic_materials = 20000 + (width * 10) + (length * 10) + (height * 10)

    # Floor protection material (previously missing)
    floor_area = float(form.bathroom_details.floor_area.data or 0)
    protection_material = floor_area * 50

    # Layout modifications materials (previously missing)
    layout_material = calculate_layout_material_cost(form)

    # Plumbing materials (previously missing)
    plumbing_material = calculate_plumbing_material_cost(form)

    # Electrical materials (previously missing)
    electrical_material = calculate_electrical_material_cost(form)

    # Fixtures materials (previously missing)
    fixtures_material = calculate_fixtures_material_cost(form)

    # Tiling and painting materials (previously missing)
    tiling_material = calculate_tiling_material_cost(form)

    # Add extra items material cost
    _, extra_material, _ = calculate_extra_items_cost(form)

    # Total materials
    total_materials = (
        basic_materials
        + protection_material
        + layout_material
        + plumbing_material
        + electrical_material
        + fixtures_material
        + tiling_material
        + extra_material
    )

    # Apply discount
    material_after_discount = total_materials - 1000

    return material_after_discount


def calculate_waste_cost(form):
    """Calculate the waste handling and other costs for the main option."""
    # Service car
    service_car_cost = 0
    if (
        form.personal_details.service_car_price.data
        and form.personal_details.service_car_days.data
    ):
        service_car_cost = float(form.personal_details.service_car_price.data) * int(
            form.personal_details.service_car_days.data
        )

    # Parking fee
    parking_fee = float(form.personal_details.parking_fee.data or 0)

    # Congestion charge
    congestion_charge = float(form.personal_details.congestion_charge.data or 0)

    # Construction bag
    bag_count = int(form.tiles_and_painting.construction_bag.data or 0)
    bag_cost = bag_count * 1500  # Assuming fixed price

    # Basic waste costs
    floor_area = float(form.bathroom_details.floor_area.data or 0)
    basic_waste = 5000 + floor_area * 200

    # Add extra items other/waste cost
    _, _, extra_other = calculate_extra_items_cost(form)

    # Total other costs
    other_costs = (
        service_car_cost
        + parking_fee
        + congestion_charge
        + bag_cost
        + basic_waste
        + extra_other
    )

    # Apply discount
    other_after_discount = other_costs - 1000

    return other_after_discount


# Helper functions for calculating specific parts of labor costs


def calculate_plumbing_labor_cost(form):
    """Calculate plumbing-related labor costs."""
    labor_cost = 0

    # Floor Drain Replacement
    drain_replacements = int(form.bathroom_details.floor_drain_replacements.data or 0)
    if drain_replacements == 1:
        labor_cost += 2500
    elif drain_replacements == 2:
        labor_cost += 4500
    elif drain_replacements == 3:
        labor_cost += 6000

    # Floor Drain Relocation
    drain_relocation = form.bathroom_details.floor_drain_relocation.data or "0"
    if drain_relocation == "1":
        labor_cost += 1000
    elif drain_relocation == "2":
        labor_cost += 2000
    elif drain_relocation == "3":
        labor_cost += 2500

    # Extra Floor Drain
    if form.bathroom_details.extra_floor_drain.data:
        labor_cost += 2500

    # Channel Cutting
    if form.bathroom_details.cut_channels.data:
        labor_cost += 100

    # Other Floor Penetrations
    floor_penetrations = form.bathroom_details.floor_penetrations.data or "0"
    if floor_penetrations == "1":
        labor_cost += 500
    elif floor_penetrations == "2":
        labor_cost += 1000
    elif floor_penetrations == "3":
        labor_cost += 1500

    # Wall Penetrations
    wall_penetrations = form.bathroom_details.wall_penetrations.data or "0"
    if wall_penetrations == "1":
        labor_cost += 2500
    elif wall_penetrations == "2":
        labor_cost += 5000
    elif wall_penetrations == "3":
        labor_cost += 7000

    # Replace Floor Drain Pipes
    if form.bathroom_details.move_drain_pipes.data:
        labor_cost += 2500

    # Water Shutoff Location - Fix field name inconsistency
    water_shutoff = form.appliances.water_shutoff.data or ""
    if "association" in water_shutoff.lower():
        labor_cost += 1000

    # Hidden Pipes
    if form.interior_fittings.hidden_pipelines.data:
        labor_cost += 9000

    # Hidden Ceiling Shower
    if form.interior_fittings.hidden_ceiling_shower.data:
        labor_cost += 8000

    # Concealed Mixers
    mixers_count = int(form.interior_fittings.concealed_mixers_count.data or 0)
    mixers_price = float(form.interior_fittings.concealed_mixers_price.data or 0)
    if mixers_count > 0:
        labor_cost += mixers_count * mixers_price

    # Save Existing Water Floor Heating
    if form.interior_fittings.save_waterheated_floor.data:
        labor_cost += 5000

    # New Water Floor Heating
    if form.interior_fittings.new_waterheated_floor.data:
        floor_area = float(form.bathroom_details.floor_area.data or 0)
        labor_cost += 5000 + floor_area * 2000

    return labor_cost


def calculate_electrical_labor_cost(form):
    """Calculate electrical-related labor costs."""
    labor_cost = 0

    # RCD / Ground Fault Interrupter - Fix field name inconsistency
    if not form.appliances.rcd.data:
        labor_cost += 2000

    # Fusebox Distance - Fix field name inconsistency
    fusebox_distance = form.appliances.fusebox_distance.data or ""
    if fusebox_distance == "up_to_10m":
        labor_cost += 1000
    elif fusebox_distance == "another_floor":
        labor_cost += 2000

    # Junction Box Distance
    if form.appliances.junction_box_distance.data == "far":
        labor_cost += 1000

    # Electric Towel Warmer
    if form.appliances.electric_towel_warmer.data:
        labor_cost += 1500

    # Electric Floor Heating
    if form.appliances.floor_heating.data:
        labor_cost += 7000

    # Washing Machine
    if form.appliances.washing_machine.data:
        labor_cost += 4400

    # Dryer
    if form.appliances.dryer.data:
        labor_cost += 2000

    # Sink Outlet
    if form.appliances.sink_outlet.data:
        labor_cost += 500

    # Iron Outlet
    if form.appliances.iron_outlet.data:
        labor_cost += 500

    # Spotlights
    spotlights_count = int(form.appliances.spotlights_count.data or 0)
    spotlights_price = float(
        form.appliances.spotlights_price_per_unit.data or 500
    )  # Use 500 as default if no price given
    if spotlights_count > 0:
        labor_cost += spotlights_count * spotlights_price

    return labor_cost


def calculate_fixtures_labor_cost(form):
    """Calculate fixtures-related labor costs."""
    labor_cost = 0

    # Ceiling Lowering
    if form.appliances.ceiling_lowering.data:
        width = float(form.bathroom_details.width.data or 0)
        length = float(form.bathroom_details.length.data or 0)
        labor_cost += 2800 + width * length * 0.02

    # Built-in Mirror
    if form.interior_fittings.built_in_mirror.data:
        labor_cost += 2500

    # Build Shower Wall
    if form.interior_fittings.shower_wall.data:
        labor_cost += 12000

    # Glass Block Wall
    if form.interior_fittings.glass_block_wall.data:
        labor_cost += 12000

    # Mount Glass Shower Wall
    if form.interior_fittings.glass_shower_wall.data:
        labor_cost += 500

    # Mount Shower Doors
    if form.interior_fittings.shower_doors.data:
        labor_cost += 1000

    # Shower Drain Type
    shower_drain = form.interior_fittings.shower_drain.data or ""
    if shower_drain == "elongated":
        labor_cost += 2000

    # Bathtub Type
    if form.interior_fittings.bathtub_built_in.data:
        labor_cost += 15000

    # Toilet Type
    if form.interior_fittings.toilet_wall_mounted.data:
        labor_cost += 6500

    # Inner Door Casing Replacement
    if form.interior_fittings.interior_door_casing.data:
        labor_cost += 500

    # Outer Door Casing Replacement
    if form.interior_fittings.exterior_door_casing.data:
        labor_cost += 500

    # Door Frame Replacement
    if form.interior_fittings.doorframe_replacement.data:
        labor_cost += 1000

    # Window Repainting
    if form.interior_fittings.window_repainting.data:
        labor_cost += 500

    # Niches without Spotlight
    niches_count = int(form.interior_fittings.niches_count.data or 0)
    niches_price = float(form.interior_fittings.niches_price.data or 0)
    if niches_count > 0:
        labor_cost += niches_count * niches_price

    return labor_cost


def calculate_tiling_labor_cost(form):
    """Calculate tiling and painting related labor costs."""
    labor_cost = 0

    # Floor Tile Size Deviation
    floor_tile_deviation = form.tiles_and_painting.floor_tile_deviation.data or ""
    if floor_tile_deviation:
        labor_cost += 500

    # Wall Tile Size Deviation
    wall_tile_deviation = form.tiles_and_painting.wall_tile_deviation.data or ""
    if wall_tile_deviation:
        labor_cost += 500

    # Grout Colors - Fix logic (should be count - 1) * price if count > 1
    grout_colors = int(form.tiles_and_painting.grout_colors.data or 0)
    grout_colors_price = float(form.tiles_and_painting.grout_colors_price.data or 0)
    if grout_colors > 1:
        labor_cost += (grout_colors - 1) * grout_colors_price

    # Ceiling Painting Time
    ceiling_hours = float(form.tiles_and_painting.ceiling_painting_hours.data or 0)
    ceiling_price = float(form.tiles_and_painting.ceiling_painting_price.data or 0)
    if ceiling_hours > 0:
        labor_cost += ceiling_hours * ceiling_price

    # Wall Painting Time
    wall_hours = float(form.tiles_and_painting.wall_painting_hours.data or 0)
    wall_price = float(form.tiles_and_painting.wall_painting_price.data or 0)
    if wall_hours > 0:
        labor_cost += wall_hours * wall_price

    return labor_cost


# Helper functions for calculating specific parts of material costs


def calculate_layout_material_cost(form):
    """Calculate layout-related material costs."""
    material_cost = 0

    # Relocations
    relocations = int(form.bathroom_details.relocation_count.data or 0)
    if relocations == 1:
        material_cost += 500
    elif relocations == 2:
        material_cost += 1000
    elif relocations == 3:
        material_cost += 1500

    # Specific Fixture Relocations
    if (
        form.bathroom_details.toilet_relocation.data
        and int(form.bathroom_details.toilet_relocation.data) > 0
    ):
        material_cost += 500
    if (
        form.bathroom_details.sink_relocation.data
        and int(form.bathroom_details.sink_relocation.data) > 0
    ):
        material_cost += 500
    if (
        form.bathroom_details.shower_relocation.data
        and int(form.bathroom_details.shower_relocation.data) > 0
    ):
        material_cost += 500
    if (
        form.bathroom_details.bathtub_relocation.data
        and int(form.bathroom_details.bathtub_relocation.data) > 0
    ):
        material_cost += 1000
    if (
        form.bathroom_details.towel_warmer_relocation.data
        and int(form.bathroom_details.towel_warmer_relocation.data) > 0
    ):
        material_cost += 400

    return material_cost


def calculate_plumbing_material_cost(form):
    """Calculate plumbing-related material costs."""
    material_cost = 0

    # Floor Drain Replacement
    drain_replacements = int(form.bathroom_details.floor_drain_replacements.data or 0)
    if drain_replacements == 1:
        material_cost += 500
    elif drain_replacements == 2:
        material_cost += 1000
    elif drain_replacements == 3:
        material_cost += 1200

    # Floor Drain Relocation
    drain_relocation = form.bathroom_details.floor_drain_relocation.data or "0"
    if drain_relocation == "1":
        material_cost += 500
    elif drain_relocation == "2":
        material_cost += 1000
    elif drain_relocation == "3":
        material_cost += 1500

    # Extra Floor Drain
    if form.bathroom_details.extra_floor_drain.data:
        material_cost += 1000

    # Other Floor Penetrations
    floor_penetrations = form.bathroom_details.floor_penetrations.data or "0"
    if floor_penetrations == "1":
        material_cost += 500
    elif floor_penetrations == "2":
        material_cost += 1000
    elif floor_penetrations == "3":
        material_cost += 1500

    # Wall Penetrations
    wall_penetrations = form.bathroom_details.wall_penetrations.data or "0"
    if wall_penetrations == "1":
        material_cost += 1500
    elif wall_penetrations == "2":
        material_cost += 2500
    elif wall_penetrations == "3":
        material_cost += 4000

    # Replace Floor Drain Pipes
    if form.bathroom_details.move_drain_pipes.data:
        material_cost += 1000

    # Hidden Pipes
    if form.interior_fittings.hidden_pipelines.data:
        material_cost += 3000

    # Hidden Ceiling Shower
    if form.interior_fittings.hidden_ceiling_shower.data:
        material_cost += 2500

    # Concealed Mixers - Fix logic to match frontend
    mixers_count = int(form.interior_fittings.concealed_mixers_count.data or 0)
    if mixers_count > 0:
        material_cost += 2500  # Fixed cost, not per count

    # Save Existing Water Floor Heating
    if form.interior_fittings.save_waterheated_floor.data:
        material_cost += 1000

    # New Water Floor Heating
    if form.interior_fittings.new_waterheated_floor.data:
        material_cost += 10000

    return material_cost


def calculate_electrical_material_cost(form):
    """Calculate electrical-related material costs."""
    material_cost = 0

    # RCD / Ground Fault Interrupter
    if not form.appliances.rcd.data:
        material_cost += 500

    # Fusebox Distance
    fusebox_distance = form.appliances.fusebox_distance.data or ""
    if fusebox_distance == "up_to_10m":
        material_cost += 500
    elif fusebox_distance == "another_floor":
        material_cost += 1000

    # Junction Box Distance
    if form.appliances.junction_box_distance.data == "far":
        material_cost += 500

    # Electric Towel Warmer
    if form.appliances.electric_towel_warmer.data:
        material_cost += 500

    # Electric Floor Heating
    if form.appliances.floor_heating.data:
        floor_area = float(form.bathroom_details.floor_area.data or 0)
        material_cost += floor_area * 1000

    # Washing Machine
    if form.appliances.washing_machine.data:
        material_cost += 1000

    # Dryer
    if form.appliances.dryer.data:
        material_cost += 500

    # Sink Outlet
    if form.appliances.sink_outlet.data:
        material_cost += 500

    # Iron Outlet
    if form.appliances.iron_outlet.data:
        material_cost += 500

    # Spotlights
    spotlights_count = int(form.appliances.spotlights_count.data or 0)
    if spotlights_count > 0:
        material_cost += spotlights_count * 300

    return material_cost


def calculate_fixtures_material_cost(form):
    """Calculate fixtures-related material costs."""
    material_cost = 0

    # Ceiling Lowering
    if form.appliances.ceiling_lowering.data:
        material_cost += 1200

    # Build Shower Wall
    if form.interior_fittings.shower_wall.data:
        material_cost += 2500

    # Glass Block Wall
    if form.interior_fittings.glass_block_wall.data:
        material_cost += 4000

    # Bathtub Type
    if form.interior_fittings.bathtub_built_in.data:
        material_cost += 2000

    # Toilet Type
    if form.interior_fittings.toilet_wall_mounted.data:
        material_cost += 2000

    # Inner Door Casing Replacement
    if form.interior_fittings.interior_door_casing.data:
        material_cost += 250

    # Outer Door Casing Replacement
    if form.interior_fittings.exterior_door_casing.data:
        material_cost += 250

    # Door Frame Replacement
    if form.interior_fittings.doorframe_replacement.data:
        material_cost += 1000

    # Window Repainting
    if form.interior_fittings.window_repainting.data:
        material_cost += 250

    return material_cost


def calculate_tiling_material_cost(form):
    """Calculate tiling and painting related material costs."""
    material_cost = 0

    # Floor Tile Size Deviation
    floor_tile_deviation = form.tiles_and_painting.floor_tile_deviation.data or ""
    if floor_tile_deviation:
        material_cost += 500

    # Wall Tile Size Deviation
    wall_tile_deviation = form.tiles_and_painting.wall_tile_deviation.data or ""
    if wall_tile_deviation:
        material_cost += 500

    # Grout Colors - Fix logic (should be count - 1) * price if count > 1
    grout_colors = int(form.tiles_and_painting.grout_colors.data or 0)
    grout_colors_price = float(form.tiles_and_painting.grout_colors_price.data or 0)
    if grout_colors > 1:
        material_cost += (grout_colors - 1) * grout_colors_price

    # Ceiling Painting Material - Add calculation that was missing in frontend
    if form.tiles_and_painting.paint_ceiling.data:
        ceiling_area = float(form.tiles_and_painting.ceiling_area.data or 0)
        ceiling_area_price = float(form.tiles_and_painting.ceiling_area_price.data or 0)
        material_cost += ceiling_area * ceiling_area_price

    # Wall Painting Material
    if form.tiles_and_painting.paint_walls.data:
        wall_area = float(form.tiles_and_painting.wall_area.data or 0)
        wall_area_price = float(form.tiles_and_painting.wall_area_price.data or 0)
        material_cost += wall_area * wall_area_price

    return material_cost


def calculate_discount(form):
    """Calculate any discount for the main option."""
    # Total discount is 3000 SEK (1000 for each category)
    return 3000


def calculate_total(form):
    """Calculate the total cost for the main option."""
    # Get labor and material costs
    labor = calculate_labor_cost(form)
    material = calculate_material_cost(form)
    waste = calculate_waste_cost(form)

    # ROT deduction is calculated based on labor after discount
    rot_deduction = calculate_rot_deduction(form)

    # Apply ROT deduction to labor
    labor_after_rot = labor - rot_deduction

    return labor_after_rot + material + waste


def calculate_rot_deduction(form):
    """Calculate the ROT deduction for the main option."""
    # ROT should be calculated on labor after discount
    labor = calculate_labor_cost(form)
    # ROT deduction is 30% of labor cost, max 50,000 SEK
    return min(float(labor) * 0.3, 50000)


def calculate_labor_cost_option1(form):
    """Calculate the labor cost for option 1."""
    # Option 1: Simpler renovation
    base_cost = 24500

    if form.bathroom_details.floor_area.data:
        base_cost += float(form.bathroom_details.floor_area.data) * 800

    # Add extra items labor cost
    extra_labor, _, _ = calculate_extra_items_cost(form)
    base_cost += extra_labor

    # Apply discount
    labor_after_discount = base_cost - 1000

    return labor_after_discount


def calculate_material_cost_option1(form):
    """Calculate the material cost for option 1."""
    base_cost = 20000

    if form.bathroom_details.floor_area.data:
        base_cost += float(form.bathroom_details.floor_area.data) * 1500

    # Add extra items material cost
    _, extra_material, _ = calculate_extra_items_cost(form)
    base_cost += extra_material

    # Apply discount
    material_after_discount = base_cost - 1000

    return material_after_discount


def calculate_waste_cost_option1(form):
    """Calculate the waste handling cost for option 1."""
    base_cost = 4000

    if form.bathroom_details.floor_area.data:
        base_cost += float(form.bathroom_details.floor_area.data) * 150

    # Add extra items other/waste cost
    _, _, extra_other = calculate_extra_items_cost(form)
    base_cost += extra_other

    # Apply discount
    waste_after_discount = base_cost - 1000

    return waste_after_discount


def calculate_discount_option1(form):
    """Calculate any discount for option 1."""
    # Total discount is 3000 SEK (1000 for each category)
    return 3000


def calculate_total_option1(form):
    """Calculate the total cost for option 1."""
    labor = calculate_labor_cost_option1(form)
    material = calculate_material_cost_option1(form)
    waste = calculate_waste_cost_option1(form)

    # ROT deduction is applied after the discount
    rot_deduction = calculate_rot_deduction_option1(form)
    labor_after_rot = labor - rot_deduction

    return labor_after_rot + material + waste


def calculate_rot_deduction_option1(form):
    """Calculate the ROT deduction for option 1."""
    labor = calculate_labor_cost_option1(form)
    # ROT deduction is 30% of labor cost, max 50,000 SEK
    return min(float(labor) * 0.3, 50000)


def calculate_labor_cost_option2(form):
    """Calculate the labor cost for option 2."""
    # Option 2: Water-heated floor
    base_cost = 38500

    if form.bathroom_details.floor_area.data:
        base_cost += float(form.bathroom_details.floor_area.data) * 1200

    # Add extra items labor cost
    extra_labor, _, _ = calculate_extra_items_cost(form)
    base_cost += extra_labor

    # Apply discount
    labor_after_discount = base_cost - 1000

    return labor_after_discount


def calculate_material_cost_option2(form):
    """Calculate the material cost for option 2."""
    base_cost = 30000

    if form.bathroom_details.floor_area.data:
        base_cost += float(form.bathroom_details.floor_area.data) * 2500

    # Add extra items material cost
    _, extra_material, _ = calculate_extra_items_cost(form)
    base_cost += extra_material

    # Apply discount
    material_after_discount = base_cost - 1000

    return material_after_discount


def calculate_waste_cost_option2(form):
    """Calculate the waste handling cost for option 2."""
    base_cost = 6000

    if form.bathroom_details.floor_area.data:
        base_cost += float(form.bathroom_details.floor_area.data) * 250

    # Add extra items other/waste cost
    _, _, extra_other = calculate_extra_items_cost(form)
    base_cost += extra_other

    # Apply discount
    waste_after_discount = base_cost - 1000

    return waste_after_discount


def calculate_discount_option2(form):
    """Calculate any discount for option 2."""
    # Total discount is 3000 SEK (1000 for each category)
    return 3000


def calculate_total_option2(form):
    """Calculate the total cost for option 2."""
    labor = calculate_labor_cost_option2(form)
    material = calculate_material_cost_option2(form)
    waste = calculate_waste_cost_option2(form)

    # ROT deduction is applied after the discount
    rot_deduction = calculate_rot_deduction_option2(form)
    labor_after_rot = labor - rot_deduction

    return labor_after_rot + material + waste


def calculate_rot_deduction_option2(form):
    """Calculate the ROT deduction for option 2."""
    labor = calculate_labor_cost_option2(form)
    # ROT deduction is 30% of labor cost, max 50,000 SEK
    return min(float(labor) * 0.3, 50000)
