import os
import logging
import fitz  # PyMuPDF
from typing import Dict, Any, List
from forms.renovation_form import RenovationForm


class PDFGenerator:
    """
    Service for generating PDF work orders.
    """

    def __init__(
        self,
        base_dir=None,
        template_dir: str = "templates/pdf",
        output_dir: str = "static/generated_docs",
    ):
        """
        Initialize the PDF generator.

        Args:
            base_dir: Optional base directory path. If provided, paths will be absolute.
            template_dir: Directory where PDF templates are stored.
            output_dir: Directory where generated PDFs will be stored.
        """
        self.logger = logging.getLogger(__name__)

        # Set up directories
        if base_dir:
            # Use absolute paths
            self.base_dir = base_dir
            self.template_dir = os.path.join(base_dir, template_dir)
            self.output_dir = os.path.join(base_dir, output_dir)
        else:
            # Use relative paths
            self.base_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            self.template_dir = os.path.join(self.base_dir, template_dir)
            self.output_dir = os.path.join(self.base_dir, output_dir)

        self.logger.debug(f"Base directory: {self.base_dir}")
        self.logger.debug(f"Template directory: {self.template_dir}")
        self.logger.debug(f"Output directory: {self.output_dir}")

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Define template file names
        self.electrician_template = "electriciatian.pdf"
        self.plumber_template = "plumber.pdf"
        self.carpenter_template = "carpenter.pdf"

    def _generate_pdf(
        self, template_name: str, output_path: str, context: Dict[str, Any]
    ) -> str:
        """
        Generate a PDF by adding text onto a template.

        Args:
            template_name: Name of the template file
            output_path: Where to save the resulting PDF
            context: Dictionary of context data

        Returns:
            The path to the generated PDF
        """
        try:
            # Get the full path to the template
            template_path = os.path.join(self.template_dir, template_name)
            self.logger.debug(f"Using template: {template_path}")

            # Open the template
            doc = fitz.open(template_path)
            page = doc[0]  # Assuming we're working with a single page

            # Keep track of position
            y_position = 410  # Adjusted starting Y position below the image/title
            col_width = 250  # Width of each column
            x_positions = [50, 300]  # X positions for 2 columns
            line_height = 25  # Height of each line - increased for better spacing

            # Format items with sequential numbering
            items = []
            item_number = 1

            for key, value in context.items():
                # Skip customer name as it's handled separately
                if key == "customer_name":
                    continue

                # Format the key for display
                display_key = key.replace("_", " ").title()

                # Only include checked items (Yes values or positive numeric values)
                if value == "Yes" or (isinstance(value, (int, float)) and value > 0):
                    # Format checkbox and value
                    checkbox = "☑"
                    display_value = (
                        f": {value}" if isinstance(value, (int, float)) else ""
                    )

                    # Create text for this option with sequential numbering
                    text = f"{item_number}.{display_key}{display_value}"
                    items.append((checkbox, text))
                    item_number += 1
                # Skip "No", "0", "Not specified", and "Unknown" values

            # Add each option as a line of text
            col = 0  # Start with the first column
            for i, (checkbox, text) in enumerate(items):
                # Get position for this item
                x_pos = x_positions[col]

                # Add checkbox first
                page.insert_text(
                    (x_pos, y_position),
                    checkbox,
                    fontsize=12,  # Larger checkbox
                    fontname="helv",
                    color=(0, 0, 0),
                )

                # Add text next to checkbox
                page.insert_text(
                    (x_pos + 20, y_position),  # Offset text from checkbox
                    text,
                    fontsize=11,  # Larger text
                    fontname="helv",
                    color=(0, 0, 0),
                )

                # Update position for next item
                col = (col + 1) % 2
                if col == 0:  # If we're wrapping to the next line
                    y_position += line_height

                # Check if we're near the bottom of the page
                if y_position > 800:
                    # We'll stop here to avoid going off the page
                    # In a real implementation, you might want to add a new page
                    break

            # Save the PDF
            doc.save(output_path)
            self.logger.debug(f"Generated PDF at {output_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate PDF: {str(e)}")

    def generate_electrician_workorder(self, form: RenovationForm) -> str:
        """
        Generate an electrician workorder from the form data.

        Args:
            form: The submitted renovation form

        Returns:
            The path to the generated electrician workorder PDF
        """
        # Extract electrician-relevant data from the form
        context = {
            "customer_name": f"{form.personal_details.first_name.data} {form.personal_details.last_name.data}",
            # Electrical appliances
            "ceiling_lamp": "Yes" if form.appliances.ceiling_lamp.data else "No",
            "wall_socket": "Yes" if form.appliances.wall_socket.data else "No",
            "electric_towel_warmer": (
                "Yes" if form.appliances.electric_towel_warmer.data else "No"
            ),
            "floor_heating": "Yes" if form.appliances.floor_heating.data else "No",
            "washing_machine": "Yes" if form.appliances.washing_machine.data else "No",
            "dryer": "Yes" if form.appliances.dryer.data else "No",
            "sink_outlet": "Yes" if form.appliances.sink_outlet.data else "No",
            "iron_outlet": "Yes" if form.appliances.iron_outlet.data else "No",
            "spotlights_count": form.appliances.spotlights_count.data or 0,
            "ceiling_lowering": (
                "Yes" if form.appliances.ceiling_lowering.data else "No"
            ),
            # Service car information
            "service_car_days": form.personal_details.service_car_days.data or 0,
            "service_car_price": form.personal_details.service_car_price.data or 0,
            # Fuse box information
            "fuse_box_type": form.bathroom_details.fuse_box_type.data
            or "Not specified",
            "has_gfci": "Yes" if form.bathroom_details.has_gfci.data else "No",
            "fuse_box_distance": form.bathroom_details.fuse_box_distance.data
            or "Unknown",
            "junction_box_distance": form.bathroom_details.junction_box_distance.data
            or "Unknown",
            # Floor area
            "floor_area": form.bathroom_details.floor_area.data or 0,
        }

        # Generate a unique filename
        filename = (
            f"electrician_workorder_{form.personal_details.last_name.data.lower()}.pdf"
        )
        output_path = os.path.join(self.output_dir, filename)

        # Generate the PDF using the template
        return self._generate_pdf(self.electrician_template, output_path, context)

    def generate_plumber_workorder(self, form: RenovationForm) -> str:
        """
        Generate a plumber workorder from the form data.

        Args:
            form: The submitted renovation form

        Returns:
            The path to the generated plumber workorder PDF
        """
        # Extract plumber-relevant data from the form
        context = {
            "customer_name": f"{form.personal_details.first_name.data} {form.personal_details.last_name.data}",
            # Bathroom fixtures
            "toilet_relocation": form.bathroom_details.toilet_relocation.data or 0,
            "sink_relocation": form.bathroom_details.sink_relocation.data or 0,
            "shower_relocation": form.bathroom_details.shower_relocation.data or 0,
            "bathtub_relocation": form.bathroom_details.bathtub_relocation.data or 0,
            "towel_warmer_relocation": form.bathroom_details.towel_warmer_relocation.data
            or 0,
            # Relocation count
            "relocation_count": form.bathroom_details.relocation_count.data or "0",
            # Floor drains
            "floor_drain_replacements": form.bathroom_details.floor_drain_replacements.data
            or 0,
            "floor_drain_relocation": form.bathroom_details.floor_drain_relocation.data
            or "0",
            "extra_floor_drain": (
                "Yes" if form.bathroom_details.extra_floor_drain.data else "No"
            ),
            # Construction details
            "floor_penetrations": form.bathroom_details.floor_penetrations.data or "0",
            "wall_penetrations": form.bathroom_details.wall_penetrations.data or "0",
            # Water supply
            "water_shutoff_location": form.bathroom_details.water_shutoff_location.data
            or "Unknown",
            "hidden_pipelines": (
                "Yes" if form.interior_fittings.hidden_pipelines.data else "No"
            ),
            "shown_pipelines": (
                "Yes" if form.interior_fittings.shown_pipelines.data else "No"
            ),
            # Shower/Bath options
            "shower_mixer": "Yes" if form.interior_fittings.shower_mixer.data else "No",
            "shower_corner": (
                "Yes" if form.interior_fittings.shower_corner.data else "No"
            ),
            "hidden_ceiling_shower": (
                "Yes" if form.interior_fittings.hidden_ceiling_shower.data else "No"
            ),
            "bathtub_normal": (
                "Yes" if form.interior_fittings.bathtub_normal.data else "No"
            ),
            "bathtub_long": "Yes" if form.interior_fittings.bathtub_long.data else "No",
            "bathtub_freestanding": (
                "Yes" if form.interior_fittings.bathtub_freestanding.data else "No"
            ),
            "bathtub_built_in": (
                "Yes" if form.interior_fittings.bathtub_built_in.data else "No"
            ),
            "bathtub_wall": "Yes" if form.interior_fittings.bathtub_wall.data else "No",
            # Floor heating
            "save_waterheated_floor": (
                "Yes" if form.interior_fittings.save_waterheated_floor.data else "No"
            ),
            "new_waterheated_floor": (
                "Yes" if form.interior_fittings.new_waterheated_floor.data else "No"
            ),
            # Floor area
            "floor_area": form.bathroom_details.floor_area.data or 0,
        }

        # Generate a unique filename
        filename = (
            f"plumber_workorder_{form.personal_details.last_name.data.lower()}.pdf"
        )
        output_path = os.path.join(self.output_dir, filename)

        # Generate the PDF using the template
        return self._generate_pdf(self.plumber_template, output_path, context)

    def generate_carpenter_workorder(self, form: RenovationForm) -> str:
        """
        Generate a carpenter workorder from the form data.

        Args:
            form: The submitted renovation form

        Returns:
            The path to the generated carpenter workorder PDF
        """
        # Extract carpenter-relevant data from the form
        context = {
            "customer_name": f"{form.personal_details.first_name.data} {form.personal_details.last_name.data}",
            # Door and window work
            "interior_door_casing": (
                "Yes" if form.interior_fittings.interior_door_casing.data else "No"
            ),
            "exterior_door_casing": (
                "Yes" if form.interior_fittings.exterior_door_casing.data else "No"
            ),
            "doorframe_replacement": (
                "Yes" if form.interior_fittings.doorframe_replacement.data else "No"
            ),
            "door_replacement": (
                "Yes" if form.interior_fittings.door_replacement.data else "No"
            ),
            "threshold_replacement": (
                "Yes" if form.interior_fittings.threshold_replacement.data else "No"
            ),
            "window_repainting": (
                "Yes" if form.interior_fittings.window_repainting.data else "No"
            ),
            # Shower/bath enclosures
            "shower_wall": "Yes" if form.interior_fittings.shower_wall.data else "No",
            "glass_block_wall": (
                "Yes" if form.interior_fittings.glass_block_wall.data else "No"
            ),
            "glass_shower_wall": (
                "Yes" if form.interior_fittings.glass_shower_wall.data else "No"
            ),
            "shower_doors": "Yes" if form.interior_fittings.shower_doors.data else "No",
            # Ceiling work
            "ceiling_lowering": (
                "Yes" if form.appliances.ceiling_lowering.data else "No"
            ),
            # Cleaning
            "dismantling_cleaning": (
                "Yes" if form.interior_fittings.dismantling_cleaning.data else "No"
            ),
            # Built-in items
            "built_in_mirror": (
                "Yes" if form.interior_fittings.built_in_mirror.data else "No"
            ),
            "mirror_lighting": (
                "Yes" if form.interior_fittings.mirror_lighting.data else "No"
            ),
            "mirror_cabinet": (
                "Yes" if form.interior_fittings.mirror_cabinet.data else "No"
            ),
            "vanity_unit": "Yes" if form.interior_fittings.vanity_unit.data else "No",
            # Silicone application
            "silicon_application": (
                "Yes" if form.interior_fittings.silicon_application.data else "No"
            ),
            # Floor and wall details
            "wall_tiling_height": form.interior_fittings.wall_tiling_height.data or 0,
            "floor_tile_size": form.tiles_and_painting.floor_tile_size.data
            or "Not specified",
            "wall_tile_size": form.tiles_and_painting.wall_tile_size.data
            or "Not specified",
            # Floor area
            "floor_area": form.bathroom_details.floor_area.data or 0,
        }

        # Generate a unique filename
        filename = (
            f"carpenter_workorder_{form.personal_details.last_name.data.lower()}.pdf"
        )
        output_path = os.path.join(self.output_dir, filename)

        # Generate the PDF using the template
        return self._generate_pdf(self.carpenter_template, output_path, context)

    def generate_all_workorders(self, form: RenovationForm) -> List[str]:
        """
        Generate all three workorder PDFs from the form data.

        Args:
            form: The submitted renovation form

        Returns:
            List of paths to the generated workorder PDFs
        """
        workorders = []

        try:
            # Generate electrician workorder
            electrician_path = self.generate_electrician_workorder(form)
            workorders.append(electrician_path)

            # Generate plumber workorder
            plumber_path = self.generate_plumber_workorder(form)
            workorders.append(plumber_path)

            # Generate carpenter workorder
            carpenter_path = self.generate_carpenter_workorder(form)
            workorders.append(carpenter_path)

            return workorders

        except Exception as e:
            self.logger.error(f"Error generating workorders: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to generate workorders: {str(e)}")
