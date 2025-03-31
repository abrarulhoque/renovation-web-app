import unittest
from unittest.mock import MagicMock
from calculations.cost_calculations import (
    calculate_labor_cost,
    calculate_material_cost,
    calculate_waste_cost,
    calculate_total,
    calculate_rot_deduction,
)


class MockForm:
    """A mock form object that simulates the structure of RenovationForm."""

    def __init__(self):
        # Create mock sections with data attributes
        self.personal_details = MagicMock()
        self.bathroom_details = MagicMock()
        self.appliances = MagicMock()
        self.interior_fittings = MagicMock()
        self.tiles_and_painting = MagicMock()
        self.additional_notes = MagicMock()

        # Set default values to prevent NoneType errors
        self._set_default_values()

    def _set_default_values(self):
        """Set default values for all form fields."""
        # Personal details defaults
        self.personal_details.season.data = "summer"
        self.personal_details.floor_count.data = 0
        self.personal_details.dwelling_type.data = "house"
        self.personal_details.parking_distance.data = "good"
        self.personal_details.transport_possibility.data = "good"
        self.personal_details.parking_fee.data = "0"
        self.personal_details.service_car_price.data = "0"
        self.personal_details.service_car_days.data = "0"
        self.personal_details.congestion_charge.data = "0"
        self.personal_details.has_elevator.data = "large"
        self.personal_details.elevator_size.data = "large"
        self.personal_details.good_stairwell_access.data = True
        self.personal_details.indoor_workspace.data = True
        self.personal_details.workspace_distance.data = "0"
        self.personal_details.entrance_distance.data = "0"

        # Bathroom details defaults
        self.bathroom_details.width.data = "0"
        self.bathroom_details.length.data = "0"
        self.bathroom_details.height.data = "0"
        self.bathroom_details.floor_area.data = "0"
        self.bathroom_details.has_sketch.data = False
        self.bathroom_details.relocation_count.data = "0"
        self.bathroom_details.toilet_relocation.data = "0"
        self.bathroom_details.sink_relocation.data = "0"
        self.bathroom_details.shower_relocation.data = "0"
        self.bathroom_details.bathtub_relocation.data = "0"
        self.bathroom_details.towel_warmer_relocation.data = "0"
        self.bathroom_details.floor_drain_replacements.data = "0"
        self.bathroom_details.floor_drain_relocation.data = "0"
        self.bathroom_details.extra_floor_drain.data = False
        self.bathroom_details.cut_channels.data = False
        self.bathroom_details.floor_penetrations.data = "0"
        self.bathroom_details.wall_penetrations.data = "0"
        self.bathroom_details.move_drain_pipes.data = False

        # Appliances defaults
        self.appliances.floor_covering_time.data = "0"
        self.appliances.water_shutoff.data = "bathroom"
        self.appliances.rcd.data = True
        self.appliances.fusebox_distance.data = "up_to_5m"
        self.appliances.junction_box_distance.data = "up_to_5m"
        self.appliances.electric_towel_warmer.data = False
        self.appliances.floor_heating.data = False
        self.appliances.washing_machine.data = False
        self.appliances.dryer.data = False
        self.appliances.sink_outlet.data = False
        self.appliances.iron_outlet.data = False
        self.appliances.spotlights_count.data = "0"
        self.appliances.ceiling_lowering.data = False

        # Interior fittings defaults
        self.interior_fittings.built_in_mirror.data = False
        self.interior_fittings.shower_wall.data = False
        self.interior_fittings.glass_block_wall.data = False
        self.interior_fittings.glass_shower_wall.data = False
        self.interior_fittings.shower_doors.data = False
        self.interior_fittings.shower_drain.data = "normal"
        self.interior_fittings.bathtub_built_in.data = False
        self.interior_fittings.toilet_wall_mounted.data = False
        self.interior_fittings.interior_door_casing.data = False
        self.interior_fittings.exterior_door_casing.data = False
        self.interior_fittings.doorframe_replacement.data = False
        self.interior_fittings.window_repainting.data = False
        self.interior_fittings.hidden_pipelines.data = False
        self.interior_fittings.hidden_ceiling_shower.data = False
        self.interior_fittings.save_waterheated_floor.data = False
        self.interior_fittings.new_waterheated_floor.data = False
        self.interior_fittings.concealed_mixers_count.data = "0"
        self.interior_fittings.concealed_mixers_price.data = "0"
        self.interior_fittings.niches_count.data = "0"
        self.interior_fittings.niches_price.data = "0"

        # Tiles and painting defaults
        self.tiles_and_painting.floor_tile_deviation.data = ""
        self.tiles_and_painting.wall_tile_deviation.data = ""
        self.tiles_and_painting.grout_colors.data = "0"
        self.tiles_and_painting.grout_colors_price.data = "0"
        self.tiles_and_painting.ceiling_painting_hours.data = "0"
        self.tiles_and_painting.ceiling_painting_price.data = "0"
        self.tiles_and_painting.paint_ceiling.data = False
        self.tiles_and_painting.ceiling_area.data = "0"
        self.tiles_and_painting.ceiling_area_price.data = "0"
        self.tiles_and_painting.wall_painting_hours.data = "0"
        self.tiles_and_painting.wall_painting_price.data = "0"
        self.tiles_and_painting.paint_walls.data = False
        self.tiles_and_painting.wall_area.data = "0"
        self.tiles_and_painting.wall_area_price.data = "0"
        self.tiles_and_painting.construction_bag.data = "0"


class TestCostCalculations(unittest.TestCase):
    """Tests for the cost calculation functions."""

    def setUp(self):
        """Set up a mock form for testing."""
        self.form = MockForm()

    def test_season_cost(self):
        """Test season-related cost calculation."""
        self.form.personal_details.season.data = "summer"
        summer_cost = calculate_labor_cost(self.form)

        self.form.personal_details.season.data = "winter"
        winter_cost = calculate_labor_cost(self.form)

        # Winter should have an additional 3000 fee
        self.assertEqual(winter_cost - summer_cost, 3000)

    def test_dwelling_type_cost(self):
        """Test dwelling type cost calculation (including commercial)."""
        # Base case
        self.form.personal_details.dwelling_type.data = "house"
        base_cost = calculate_labor_cost(self.form)

        # Test all types that should incur 2000 fee
        for dwelling_type in ["apartment", "rental", "commercial"]:
            self.form.personal_details.dwelling_type.data = dwelling_type
            type_cost = calculate_labor_cost(self.form)
            self.assertEqual(
                type_cost - base_cost, 2000, f"Failed for type: {dwelling_type}"
            )

    def test_transport_possibility_cost(self):
        """Test transport possibility cost calculation."""
        # Base case (good = 0)
        self.form.personal_details.transport_possibility.data = "good"
        good_cost = calculate_labor_cost(self.form)

        # Ok = 500
        self.form.personal_details.transport_possibility.data = "ok"
        ok_cost = calculate_labor_cost(self.form)
        self.assertEqual(ok_cost - good_cost, 500)

        # Poor = 2000
        self.form.personal_details.transport_possibility.data = "poor"
        poor_cost = calculate_labor_cost(self.form)
        self.assertEqual(poor_cost - good_cost, 2000)

    def test_grout_colors_calculation(self):
        """Test grout colors calculation using (count-1) * price formula."""
        self.form.tiles_and_painting.grout_colors.data = "1"
        self.form.tiles_and_painting.grout_colors_price.data = "500"
        base_material = calculate_material_cost(self.form)

        # Set to 3 colors (should add (3-1)*500 = 1000)
        self.form.tiles_and_painting.grout_colors.data = "3"
        new_material = calculate_material_cost(self.form)

        # Should be 1000 more than base cost (2 extra colors * 500)
        self.assertEqual(new_material - base_material, 1000)

    def test_rot_deduction(self):
        """Test ROT deduction calculation."""
        # Set bathroom dimensions to create significant labor cost
        self.form.bathroom_details.width.data = "200"
        self.form.bathroom_details.length.data = "200"
        self.form.bathroom_details.height.data = "250"

        # Calculate labor after discount and ROT deduction
        labor_cost = calculate_labor_cost(self.form)
        rot_deduction = calculate_rot_deduction(self.form)

        # ROT should be 30% of labor cost after discount, max 50000
        expected_rot = min(labor_cost * 0.3, 50000)
        self.assertEqual(rot_deduction, expected_rot)

    def test_ceiling_painting_material(self):
        """Test ceiling painting material calculation."""
        # Setup basic form
        self.form.tiles_and_painting.paint_ceiling.data = True
        self.form.tiles_and_painting.ceiling_area.data = "10"
        self.form.tiles_and_painting.ceiling_area_price.data = "200"

        material_cost = calculate_material_cost(self.form)

        # Disable ceiling painting and check difference
        self.form.tiles_and_painting.paint_ceiling.data = False
        base_material_cost = calculate_material_cost(self.form)

        # Should be 2000 difference (10m² * 200 SEK/m²)
        self.assertEqual(material_cost - base_material_cost, 2000)


if __name__ == "__main__":
    unittest.main()
